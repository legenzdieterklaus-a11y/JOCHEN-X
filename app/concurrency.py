"""Thread-management infrastructure that keeps the UI thread responsive.

This module provides cooperative cancellation, a bounded background worker pool
built on :class:`PySide6.QtCore.QThreadPool`, timeout handling, graceful
shutdown, and a UI dispatcher that marshals callables back onto the thread that
created it. Background work never blocks the UI thread, and results are delivered
both via Qt signals (for UI consumers) and a thread-safe handle (for headless
callers and tests).
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Callable
from typing import Any, TypeVar

from PySide6.QtCore import QObject, QRunnable, Qt, QThreadPool, Signal, Slot

T = TypeVar("T")

TaskCallable = Callable[["CancellationToken"], Any]


class TaskCancelledError(Exception):
    """Raised inside a worker to signal cooperative cancellation."""


class CancellationToken:
    """Thread-safe cooperative cancellation flag with completion callbacks."""

    def __init__(self) -> None:
        """Create an un-cancelled token."""
        self._event = threading.Event()
        self._lock = threading.RLock()
        self._callbacks: list[Callable[[], None]] = []

    @property
    def is_cancelled(self) -> bool:
        """Return whether cancellation has been requested."""
        return self._event.is_set()

    def cancel(self) -> None:
        """Request cancellation and fire registered callbacks exactly once."""
        with self._lock:
            if self._event.is_set():
                return
            self._event.set()
            callbacks = tuple(self._callbacks)
            self._callbacks.clear()
        for callback in callbacks:
            callback()

    def register(self, callback: Callable[[], None]) -> None:
        """Register a callback fired on cancellation (immediately if already cancelled)."""
        with self._lock:
            if not self._event.is_set():
                self._callbacks.append(callback)
                return
        callback()

    def raise_if_cancelled(self) -> None:
        """Raise :class:`TaskCancelledError` if cancellation was requested."""
        if self._event.is_set():
            raise TaskCancelledError()

    def wait(self, timeout: float | None = None) -> bool:
        """Block until cancelled or ``timeout`` elapses; return the cancelled flag."""
        return self._event.wait(timeout)


class WorkerSignals(QObject):
    """Qt signals emitted by a background task for UI-thread consumers."""

    result = Signal(object)
    error = Signal(object)
    cancelled = Signal()
    finished = Signal()


class TaskHandle:
    """Thread-safe handle to a submitted background task."""

    def __init__(self, token: CancellationToken, signals: WorkerSignals) -> None:
        """Create a handle bound to a cancellation token and signal object."""
        self._token = token
        self._signals = signals
        self._done = threading.Event()
        self._result: Any = None
        self._error: BaseException | None = None
        self._cancelled = False

    @property
    def signals(self) -> WorkerSignals:
        """Return the Qt signals for connecting UI callbacks."""
        return self._signals

    @property
    def token(self) -> CancellationToken:
        """Return the cancellation token controlling this task."""
        return self._token

    @property
    def is_done(self) -> bool:
        """Return whether the task has finished, failed, or been cancelled."""
        return self._done.is_set()

    @property
    def is_cancelled(self) -> bool:
        """Return whether the task ended through cancellation."""
        return self._cancelled

    def cancel(self) -> None:
        """Request cooperative cancellation of the task."""
        self._token.cancel()

    def wait(self, timeout: float | None = None) -> bool:
        """Block until the task completes or ``timeout`` elapses."""
        return self._done.wait(timeout)

    def result(self) -> Any:
        """Return the task result, raising the stored error or cancellation.

        Raises:
            TaskCancelledError: If the task was cancelled.
            BaseException: The original error raised inside the worker.
            RuntimeError: If the task has not completed yet.
        """
        if not self._done.is_set():
            raise RuntimeError("Task has not completed")
        if self._cancelled:
            raise TaskCancelledError()
        if self._error is not None:
            raise self._error
        return self._result

    def _set_result(self, value: Any) -> None:
        self._result = value
        self._done.set()

    def _set_error(self, error: BaseException) -> None:
        self._error = error
        self._done.set()

    def _set_cancelled(self) -> None:
        self._cancelled = True
        self._done.set()


class _Task(QRunnable):
    """Runnable adapter executing a task callable with cancellation semantics."""

    def __init__(
        self,
        function: TaskCallable,
        handle: TaskHandle,
        logger: logging.Logger,
        on_finished: Callable[[TaskHandle], None],
    ) -> None:
        super().__init__()
        self._function = function
        self._handle = handle
        self._logger = logger
        self._on_finished = on_finished

    @Slot()
    def run(self) -> None:
        """Execute the task, delivering outcome via handle and signals."""
        signals = self._handle.signals
        try:
            if self._handle.token.is_cancelled:
                self._handle._set_cancelled()
                signals.cancelled.emit()
                return
            value = self._function(self._handle.token)
            self._handle._set_result(value)
            signals.result.emit(value)
        except TaskCancelledError:
            self._handle._set_cancelled()
            signals.cancelled.emit()
        except Exception as error:  # boundary: worker errors must not crash the pool
            self._logger.error("worker.failed", exc_info=error, extra={"context": {"type": type(error).__name__}})
            self._handle._set_error(error)
            signals.error.emit(error)
        finally:
            signals.finished.emit()
            self._on_finished(self._handle)


class WorkerPool:
    """Bounded background worker pool with cancellation and timeout support."""

    def __init__(self, *, max_workers: int | None = None, logger: logging.Logger | None = None) -> None:
        """Create the pool.

        Args:
            max_workers: Optional maximum concurrent worker threads.
            logger: Optional logger for diagnostics.
        """
        self._logger = logger or logging.getLogger("jochen_x.workers")
        self._pool = QThreadPool()
        if max_workers is not None:
            if max_workers < 1:
                raise ValueError("max_workers must be positive")
            self._pool.setMaxThreadCount(max_workers)
        self._lock = threading.RLock()
        self._handles: set[TaskHandle] = set()
        self._timers: dict[TaskHandle, threading.Timer] = {}

    @property
    def max_workers(self) -> int:
        """Return the maximum number of concurrent worker threads."""
        return self._pool.maxThreadCount()

    def active_count(self) -> int:
        """Return the number of currently active worker threads."""
        return self._pool.activeThreadCount()

    def submit(
        self,
        function: TaskCallable,
        *,
        token: CancellationToken | None = None,
        timeout: float | None = None,
    ) -> TaskHandle:
        """Submit ``function`` for background execution.

        Args:
            function: Callable receiving a cancellation token and returning a value.
            token: Optional externally owned cancellation token.
            timeout: Optional cooperative timeout in seconds; on expiry the token
                is cancelled so a cooperative task can stop promptly.

        Returns:
            A :class:`TaskHandle` for awaiting or cancelling the task.
        """
        resolved_token = token or CancellationToken()
        handle = TaskHandle(resolved_token, WorkerSignals())
        with self._lock:
            self._handles.add(handle)
            if timeout is not None:
                if timeout <= 0:
                    raise ValueError("timeout must be positive")
                timer = threading.Timer(timeout, self._on_timeout, args=(handle,))
                timer.daemon = True
                self._timers[handle] = timer
                timer.start()
        self._pool.start(_Task(function, handle, self._logger, self._complete))
        return handle

    def shutdown(self, *, timeout: float | None = 5.0) -> bool:
        """Cancel outstanding work and wait for the pool to drain.

        Args:
            timeout: Maximum seconds to wait for workers to finish; ``None`` waits
                indefinitely.

        Returns:
            ``True`` if all workers finished within the timeout.
        """
        with self._lock:
            handles = tuple(self._handles)
            timers = tuple(self._timers.values())
        for timer in timers:
            timer.cancel()
        for handle in handles:
            handle.cancel()
        milliseconds = -1 if timeout is None else int(timeout * 1000)
        drained = self._pool.waitForDone(milliseconds)
        self._logger.info("workers.shutdown", extra={"context": {"drained": drained}})
        return drained

    def _on_timeout(self, handle: TaskHandle) -> None:
        """Cancel a task whose cooperative timeout has elapsed."""
        if not handle.is_done:
            self._logger.warning("worker.timeout")
            handle.cancel()

    def _complete(self, handle: TaskHandle) -> None:
        """Release bookkeeping for a finished task."""
        with self._lock:
            self._handles.discard(handle)
            timer = self._timers.pop(handle, None)
        if timer is not None:
            timer.cancel()


class UiDispatcher(QObject):
    """Marshals callables onto the thread that constructed the dispatcher.

    Construct this on the UI thread. :meth:`post` may then be called from any
    background thread; the callable runs on the UI thread via a queued signal,
    guaranteeing the UI is only ever touched from the UI thread.
    """

    _dispatch = Signal(object)

    def __init__(self, parent: QObject | None = None, logger: logging.Logger | None = None) -> None:
        """Create the dispatcher and wire the internal queued invocation slot."""
        super().__init__(parent)
        self._logger = logger or logging.getLogger("jochen_x.ui")
        self._dispatch.connect(self._invoke, Qt.ConnectionType.QueuedConnection)

    def post(self, callback: Callable[[], None]) -> None:
        """Schedule ``callback`` to run on the dispatcher's thread."""
        self._dispatch.emit(callback)

    def wrap(self, callback: Callable[..., None]) -> Callable[..., None]:
        """Return a callable that posts ``callback`` (with bound args) to the UI thread."""
        def dispatched(*args: Any, **kwargs: Any) -> None:
            self.post(lambda: callback(*args, **kwargs))

        return dispatched

    @Slot(object)
    def _invoke(self, callback: Callable[[], None]) -> None:
        """Execute a posted callback, guarding against callback failures."""
        try:
            callback()
        except Exception as error:  # boundary: keep the UI event loop alive
            self._logger.error("ui.dispatch_failed", exc_info=error, extra={"context": {"type": type(error).__name__}})
