"""
Timer class
Ref.: https://realpython.com/python-timer/#python-timer-functions

"""
import time
from contextlib import ContextDecorator
from dataclasses import dataclass, field
from typing import Any, ClassVar


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""
    pass


@dataclass
class Timer(ContextDecorator):
    timers: ClassVar = {}  # used to accumulate times of named timers
    name: str = ''
    text: str = 'Elapsed time: {:0.4f} seconds'
    logger: Any = print
    _start_time: Any = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Add timer to dict of timers after initialization"""
        if self.name:
            self.timers.setdefault(self.name, 0)

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")
        self._start_time = time.perf_counter()

    def elapsed(self):
        """Returns the elapsed time since the timer was started
        """
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        return time.perf_counter() - self._start_time

    def stop(self):
        """Stop the timer, and report the elapsed time
        """
        elapsed_time = self.elapsed()
        self._start_time = None
        if self.logger:
            self.logger(self.text.format(elapsed_time))
        if self.name:
            self.timers[self.name] += elapsed_time
        return elapsed_time

    def __del__(self):
        """Make sure the timer is stopped and named timer stores the accumulated value in timers"""
        if self._start_time:
            self.logger = None
            self.stop()

    def __enter__(self):
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """Stop the context manager timer"""
        self.stop()
