"""Opt-in CPython PY_START capture, without business-function replacement.

Only the creating thread may start, stop or deliver entries to the handler.
No Scene, business owner, saved input, reference CPU or scheduler is imported.
The implementation uses the Python 3.12 monitoring cleanup contract explicitly.
"""
from __future__ import annotations

from collections.abc import Callable
import sys
import threading
from types import CodeType, FrameType


EntryHandler = Callable[[CodeType, FrameType, int], bool | None]
MAX_FRAME_SEARCH = 64


class EntryMonitorError(RuntimeError):
    """An unavailable owner, actual frame or monitoring lifecycle is not guessed."""


def _live_callee_frame(code: CodeType) -> FrameType:
    """Find the nearest actual callee by identity, with a finite stack walk."""
    candidate = None
    try:
        candidate = sys._getframe(1)
        for _ in range(MAX_FRAME_SEARCH):
            if candidate is None:
                break
            if candidate.f_code is code:
                return candidate
            candidate = candidate.f_back
        raise EntryMonitorError('PY_START callee frame not found within the actual stack search bound')
    finally:
        # In particular, an exception traceback must not retain this local.
        del candidate


class EntryMonitor:
    """One explicit, single-use monitoring-tool reservation and entry handler.

    Constructing the object has no monitoring side effect. The handler borrows
    the live callee frame only during its call; it must not retain the frame.
    """

    def __init__(self, handler: EntryHandler, *, tool_id: int):
        if not callable(handler):
            raise TypeError('an explicit callable entry handler is required')
        if type(tool_id) is not int or not 0 <= tool_id <= 5:
            raise ValueError('an explicit monitoring tool_id integer from 0 through 5 is required')
        self._handler = handler
        self._tool_id = tool_id
        self._thread = threading.current_thread()
        self._tool_name = 'g5510-entry-monitor-' + format(id(self), 'x')
        self._monitoring = None
        self._callback = self._on_start
        self._reserved = False
        self._callback_installed = False
        self._active = False
        self._closed = False
        self._failed = False

    @property
    def active(self) -> bool:
        return self._active

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def failed(self) -> bool:
        return self._failed

    @property
    def tool_id(self) -> int:
        return self._tool_id

    def _require_thread(self):
        if threading.current_thread() is not self._thread:
            raise EntryMonitorError('entry monitor lifecycle belongs to its creating thread')

    def _claim_tool(self, monitoring):
        if monitoring.get_tool(self._tool_id) is not None:
            raise EntryMonitorError('explicit monitoring tool_id is already in use')
        # use_tool_id also rejects a reservation made after the preceding read.
        monitoring.use_tool_id(self._tool_id, self._tool_name)
        self._reserved = True
        try:
            if monitoring.get_events(self._tool_id) != monitoring.events.NO_EVENTS:
                raise EntryMonitorError('unused tool_id retains foreign global events; it is not a clean slot')
            previous = monitoring.register_callback(
                self._tool_id, monitoring.events.PY_START, self._callback)
            if previous is not None:
                monitoring.register_callback(self._tool_id, monitoring.events.PY_START, previous)
                raise EntryMonitorError('unused tool_id retains a foreign PY_START callback; it was restored')
            self._callback_installed = True
        except BaseException as error:
            # Before our own callback is installed, preserve any orphaned state
            # exactly as found rather than clearing somebody else's callbacks.
            try:
                monitoring.free_tool_id(self._tool_id)
            except BaseException as cleanup:
                error.add_note('Entry-monitor reservation release failed: ' + str(cleanup))
            else:
                self._reserved = False
            raise

    def start(self):
        """Reserve the caller-selected free ID and enable only PY_START."""
        self._require_thread()
        if self._active or self._closed or self._monitoring is not None:
            raise EntryMonitorError('entry monitor is single-use and must be started exactly once')
        monitoring = getattr(sys, 'monitoring', None)
        if sys.implementation.name != 'cpython' or monitoring is None:
            raise EntryMonitorError('CPython with the Python 3.12 sys.monitoring API is required')
        self._monitoring = monitoring
        try:
            self._claim_tool(monitoring)
            self._active = True
            monitoring.set_events(self._tool_id, monitoring.events.PY_START)
        except BaseException as error:
            self._stop_after_failure(error)
            raise
        return self

    def _on_start(self, code: CodeType, instruction_offset: int):
        # Monitoring masks are interpreter-wide. A foreign-thread event must
        # neither invoke the owner handler nor DISABLE this code for its owner.
        if threading.current_thread() is not self._thread or not self._active:
            return None
        live_frame = None
        try:
            if self._monitoring.get_tool(self._tool_id) != self._tool_name:
                raise EntryMonitorError('entry monitor lost its explicit tool reservation')
            if type(code) is not CodeType or type(instruction_offset) is not int or instruction_offset < 0:
                raise EntryMonitorError('PY_START requires its actual CodeType and instruction offset')
            live_frame = _live_callee_frame(code)
            keep = self._handler(code, live_frame, instruction_offset)
            if keep is not None and type(keep) is not bool:
                raise TypeError('entry handler must return exactly False, True or None')
            if keep is False and self._active:
                return self._monitoring.DISABLE
            return None
        except BaseException as error:
            self._stop_after_failure(error)
            raise
        finally:
            del live_frame

    def _stop_after_failure(self, original_error: BaseException):
        self._failed = True
        self._active = False
        try:
            self.close()
        except BaseException as cleanup:
            original_error.add_note('Entry-monitor cleanup also failed: ' + str(cleanup))

    def close(self):
        """Stop collection and explicitly clean only this tool's reservation."""
        self._require_thread()
        self._active = False
        self._closed = True
        if not self._reserved:
            return
        monitoring = self._monitoring
        if monitoring.get_tool(self._tool_id) != self._tool_name:
            self._reserved = False
            raise EntryMonitorError('will not clean or free a tool_id now owned by another tool')
        if not self._callback_installed:
            # A failed dirty-slot admission owns no callback or event mask.
            monitoring.free_tool_id(self._tool_id)
            self._reserved = False
            return
        errors = []
        operations = (
            ('set_events', (self._tool_id, monitoring.events.NO_EVENTS)),
            ('register_callback', (self._tool_id, monitoring.events.PY_START, None)),
            ('free_tool_id', (self._tool_id,)),
        )
        for name, arguments in operations:
            try:
                getattr(monitoring, name)(*arguments)
            except BaseException as error:
                errors.append((name, error))
            else:
                if name == 'register_callback':
                    self._callback_installed = False
                elif name == 'free_tool_id':
                    self._reserved = False
        if errors:
            self._failed = True
            first_name, first_error = errors[0]
            first_error.add_note('Entry-monitor cleanup failed at ' + first_name)
            for name, error in errors[1:]:
                first_error.add_note('Additional cleanup failure at ' + name + ': ' + str(error))
            raise first_error
