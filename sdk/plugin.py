"""Plugin base classes and lifecycle contracts.

The SDK exposes five base classes plugin authors can extend:

* :class:`Plugin` – the generic base every plugin derives from.
* :class:`BackgroundPlugin` – plugins with a long-running background loop.
* :class:`UIPlugin` – plugins contributing PySide6 widgets.
* :class:`ToolPlugin` – plugins exposing invocable tools.
* :class:`WorkflowPlugin` – plugins orchestrating multi-step workflows.

Each base class defines a clear, ordered lifecycle:

``UNLOADED → INITIALIZED → STARTED → (running) → STOPPED``

Errors during any phase transition move the plugin to ``FAILED`` and abort
further lifecycle progression. The lifecycle is driven by
:class:`PluginRuntime`, which composes rather than inherits the plugin so
plugin classes stay narrowly focused on business behavior.
"""

from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from enum import StrEnum
from typing import TYPE_CHECKING, Any

from sdk.errors import PluginLifecycleError
from sdk.manifest import PluginMetadata

if TYPE_CHECKING:  # avoid runtime dependency for headless SDK use
    from PySide6.QtWidgets import QWidget

    from sdk.context import PluginContext


class PluginLifecycleState(StrEnum):
    """Canonical plugin lifecycle states."""

    UNLOADED = "unloaded"
    INITIALIZED = "initialized"
    STARTED = "started"
    STOPPED = "stopped"
    FAILED = "failed"


_TERMINAL_STATES: frozenset[PluginLifecycleState] = frozenset(
    {PluginLifecycleState.STOPPED, PluginLifecycleState.FAILED}
)


class Plugin(ABC):
    """Base class every plugin extends.

    Subclasses must implement :meth:`metadata` and are expected to override
    the lifecycle hooks that are relevant to them. All hooks default to
    no-ops so plugins only implement the behaviour they need.

    Note:
        ``Plugin`` intentionally does not declare ``__slots__``. Subclasses
        commonly extend the plugin with domain state (workers, caches, Qt
        widgets), and enforcing slots at the base would force every plugin
        author to duplicate slot declarations without meaningful memory
        savings.
    """

    def __init__(self) -> None:
        """Create an unloaded plugin."""
        self._context: PluginContext | None = None
        self._state: PluginLifecycleState = PluginLifecycleState.UNLOADED
        self._state_lock = threading.RLock()

    # -- Public read-only accessors --------------------------------------------------

    @property
    def context(self) -> PluginContext:
        """Return the attached plugin context.

        Raises:
            PluginLifecycleError: If accessed before :meth:`_attach_context`
                has been called by the runtime.
        """
        if self._context is None:
            raise PluginLifecycleError(
                "Plugin context is unavailable before initialization"
            )
        return self._context

    @property
    def state(self) -> PluginLifecycleState:
        """Return the current lifecycle state."""
        with self._state_lock:
            return self._state

    # -- Lifecycle hooks --------------------------------------------------------------

    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Return the plugin's validated metadata."""

    def on_initialize(self) -> None:
        """Called once, after the context has been attached.

        Override to perform one-time setup that does not require the plugin
        to be running (e.g. reading configuration, registering resources).
        """

    def on_start(self) -> None:
        """Called when the plugin transitions from ``INITIALIZED`` to ``STARTED``.

        Override to begin normal operation. Long-running work belongs in a
        worker started here (see :class:`BackgroundPlugin`).
        """

    def on_stop(self) -> None:
        """Called when the plugin transitions from ``STARTED`` to ``STOPPED``.

        Override to release resources and stop background work. Must be
        idempotent.
        """

    def on_shutdown(self) -> None:
        """Called once, after the plugin has been fully stopped.

        Override to release resources that outlive normal operation (e.g.
        subscriptions attached at initialization time).
        """

    # -- Framework-facing internal helpers (single-underscore, host use only) --------

    def _attach_context(self, context: PluginContext) -> None:
        """Bind the context; called exactly once by :class:`PluginRuntime`.

        Raises:
            PluginLifecycleError: If the context has already been attached.
        """
        with self._state_lock:
            if self._context is not None:
                raise PluginLifecycleError("Plugin context has already been attached")
            self._context = context

    def _set_state(self, state: PluginLifecycleState) -> None:
        """Update the lifecycle state; internal helper for :class:`PluginRuntime`."""
        with self._state_lock:
            self._state = state


class BackgroundPlugin(Plugin):
    """Base class for plugins that run background work.

    Subclasses implement :meth:`run_background` and optionally override
    :meth:`request_stop` to short-circuit long-blocking operations. The
    runtime spawns a dedicated daemon thread when the plugin starts and
    joins it when the plugin stops.
    """

    _STOP_TIMEOUT_SECONDS = 5.0
    """Default cooperative stop timeout when joining the background thread."""

    def __init__(self) -> None:
        """Create the background plugin."""
        super().__init__()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    @abstractmethod
    def run_background(self, stop_event: threading.Event) -> None:
        """Perform the plugin's long-running work.

        Args:
            stop_event: Set by the runtime when a stop has been requested;
                implementations must check it cooperatively.
        """

    def request_stop(self) -> None:
        """Signal that :meth:`run_background` should return promptly."""
        self._stop_event.set()

    def on_start(self) -> None:
        """Start the background thread."""
        super().on_start()
        self._stop_event.clear()
        thread = threading.Thread(
            target=self._run_background_safe,
            name=f"plugin-{self.metadata().identifier}",
            daemon=True,
        )
        self._thread = thread
        thread.start()

    def on_stop(self) -> None:
        """Signal, wait for, and release the background thread."""
        self.request_stop()
        thread = self._thread
        if thread is not None:
            thread.join(timeout=self._STOP_TIMEOUT_SECONDS)
        self._thread = None
        super().on_stop()

    def _run_background_safe(self) -> None:
        """Guard :meth:`run_background` so exceptions are logged, not lost."""
        logger = self.context.logger
        try:
            self.run_background(self._stop_event)
        except Exception as error:  # boundary: worker errors must not kill the process
            logger.error("plugin.background_failed", exc=error)


class UIPlugin(Plugin):
    """Base class for plugins that contribute a PySide6 widget.

    Widget instantiation is intentionally deferred to :meth:`create_widget`
    so plugin loading remains headless and the actual widget is built on
    the UI thread when the host is ready to display it.
    """

    @abstractmethod
    def create_widget(self, parent: QWidget | None = None) -> QWidget:
        """Create and return the plugin's top-level PySide6 widget.

        Args:
            parent: Optional parent widget assigned by the host.

        Returns:
            A newly-created :class:`PySide6.QtWidgets.QWidget` instance.
        """


class ToolPlugin(Plugin):
    """Base class for plugins that expose an invocable tool.

    Tools are stateless single-shot operations. Long-running work should
    still use worker threads coordinated by the plugin's context.
    """

    @abstractmethod
    def execute(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        """Invoke the tool with a JSON-friendly request.

        Args:
            request: Input mapping supplied by the caller.

        Returns:
            The tool's response mapping.
        """


class WorkflowPlugin(Plugin):
    """Base class for plugins that orchestrate multi-step workflows.

    Workflows may run synchronously (returning a final result) or asynchronously
    by scheduling steps through the plugin context. The base class specifies
    only the synchronous entry point; async orchestration remains a plugin
    concern.
    """

    @abstractmethod
    def workflows(self) -> tuple[str, ...]:
        """Return the identifiers of workflows this plugin can run."""

    @abstractmethod
    def run(
        self, workflow: str, arguments: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        """Run the workflow identified by ``workflow``.

        Args:
            workflow: A workflow identifier returned by :meth:`workflows`.
            arguments: JSON-friendly input arguments.

        Returns:
            A JSON-friendly mapping representing the workflow result.
        """


class PluginRuntime:
    """Composed runtime that drives a :class:`Plugin` through its lifecycle.

    The runtime is intentionally not a subclass of :class:`Plugin`: it owns
    the transitions, enforces ordering, catches errors, and reports state
    without polluting plugin implementations with framework concerns.
    """

    def __init__(
        self,
        plugin: Plugin,
        *,
        on_state_change: Callable[[Plugin, PluginLifecycleState], None] | None = None,
    ) -> None:
        """Create the runtime bound to ``plugin``.

        Args:
            plugin: The plugin instance to drive.
            on_state_change: Optional callback invoked on every successful
                state transition.
        """
        self._plugin = plugin
        self._on_state_change = on_state_change
        self._lock = threading.RLock()
        self._context: PluginContext | None = None

    @property
    def plugin(self) -> Plugin:
        """Return the driven plugin instance."""
        return self._plugin

    @property
    def state(self) -> PluginLifecycleState:
        """Return the plugin's current lifecycle state."""
        return self._plugin.state

    def initialize(self, context: PluginContext) -> None:
        """Attach ``context`` and invoke :meth:`Plugin.on_initialize`."""
        with self._lock:
            if self._plugin.state is not PluginLifecycleState.UNLOADED:
                raise PluginLifecycleError(
                    f"Cannot initialize plugin in state {self._plugin.state.value!r}"
                )
            self._plugin._attach_context(context)
            self._context = context
            try:
                self._plugin.on_initialize()
            except Exception as error:
                self._transition(PluginLifecycleState.FAILED)
                raise PluginLifecycleError(
                    f"on_initialize failed for {self._plugin.metadata().identifier!r}: {error}"
                ) from error
            self._transition(PluginLifecycleState.INITIALIZED)

    def start(self) -> None:
        """Invoke :meth:`Plugin.on_start` and transition to ``STARTED``."""
        with self._lock:
            if self._plugin.state is not PluginLifecycleState.INITIALIZED:
                raise PluginLifecycleError(
                    f"Cannot start plugin in state {self._plugin.state.value!r}"
                )
            try:
                self._plugin.on_start()
            except Exception as error:
                self._transition(PluginLifecycleState.FAILED)
                raise PluginLifecycleError(
                    f"on_start failed for {self._plugin.metadata().identifier!r}: {error}"
                ) from error
            self._transition(PluginLifecycleState.STARTED)

    def stop(self) -> None:
        """Invoke :meth:`Plugin.on_stop` and transition to ``STOPPED``."""
        with self._lock:
            current = self._plugin.state
            if current in _TERMINAL_STATES:
                return
            if current is PluginLifecycleState.UNLOADED:
                # Nothing was started; simply mark the plugin stopped so the
                # host can dispose of the runtime uniformly.
                self._transition(PluginLifecycleState.STOPPED)
                return
            try:
                self._plugin.on_stop()
            except Exception as error:
                self._transition(PluginLifecycleState.FAILED)
                raise PluginLifecycleError(
                    f"on_stop failed for {self._plugin.metadata().identifier!r}: {error}"
                ) from error
            self._transition(PluginLifecycleState.STOPPED)

    def shutdown(self) -> None:
        """Invoke :meth:`Plugin.on_shutdown` and dispose of the context.

        Safe to call multiple times; subsequent calls are no-ops.
        """
        with self._lock:
            context = self._context
            self._context = None
            if self._plugin.state is not PluginLifecycleState.STOPPED:
                self.stop()
            try:
                self._plugin.on_shutdown()
            except Exception as error:  # boundary: shutdown must not raise
                if context is not None:
                    context.logger.error("plugin.shutdown_failed", exc=error)
            if context is not None:
                context.events.dispose()

    def _transition(self, state: PluginLifecycleState) -> None:
        """Record a new lifecycle state and notify observers."""
        self._plugin._set_state(state)
        if self._on_state_change is not None:
            try:
                self._on_state_change(self._plugin, state)
            except Exception:  # observer errors must never affect the plugin
                pass


__all__ = [
    "BackgroundPlugin",
    "Plugin",
    "PluginLifecycleState",
    "PluginRuntime",
    "ToolPlugin",
    "UIPlugin",
    "WorkflowPlugin",
]
