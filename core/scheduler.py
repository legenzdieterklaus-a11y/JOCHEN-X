"""Explicitly started task scheduler with cancellation, retry, and timeouts."""
from __future__ import annotations
import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import timedelta
@dataclass(frozen=True, slots=True)
class Schedule: delay: timedelta=timedelta(); interval: timedelta|None=None; retries: int=0; timeout: float|None=None
class TaskScheduler:
    def __init__(self) -> None: self._tasks: set[asyncio.Task[None]]=set()
    def schedule(self, callback: Callable[[], Awaitable[None]], schedule: Schedule) -> Callable[[], None]:
        async def runner() -> None:
            first = True
            while True:
                await asyncio.sleep((schedule.delay if first else schedule.interval or timedelta()).total_seconds())
                first = False
                for attempt in range(schedule.retries+1):
                    try:
                        await asyncio.wait_for(callback(), schedule.timeout); break
                    except Exception:
                        if attempt == schedule.retries: raise
                if schedule.interval is None: return
        task=asyncio.create_task(runner()); self._tasks.add(task); task.add_done_callback(self._tasks.discard)
        return task.cancel
    async def shutdown(self) -> None:
        for task in tuple(self._tasks): task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
