import datetime
import inspect
import sys
import traceback
import types
from contextlib import contextmanager
from typing import Iterator, Callable, Any, Iterable

import six

from approvaltests import to_string
from approvaltests.utilities.string_wrapper import StringWrapper
from approvaltests.namer import StackFrameNamer


class Toggles:
    def __init__(self, show: bool):
        self.queries = show
        self.messages = show
        self.variables = show
        self.hour_glass = show
        self.markers = show
        self.events = show


def _is_iterable(arg):
    return isinstance(arg, Iterable) and not isinstance(arg, six.string_types)


class LoggingInstance:
    def __init__(self):
        self.log_stack_traces = True
        self.toggles = Toggles(True)
        self.previous_timestamp = None
        self.logger = lambda t: print(t, end="")
        self.tabbing = 0
        self.counter = 0
        self.log_with_timestamps = True
        self.timer: Callable[[], datetime.datetime] = datetime.datetime.now

    def log_to_string(self) -> StringWrapper:
        buffer = StringWrapper()
        self.logger = buffer.append
        self.log_with_timestamps = False
        self.log_stack_traces = False
        return buffer

    @contextmanager
    def use_markers(self, additional_stack: int = 0) -> Iterator[None]:
        if not self.toggles.markers:
            yield
            return
        stack_position = 1 + additional_stack
        stack = inspect.stack(stack_position)[2]
        method_name = stack.function
        filename = StackFrameNamer.get_class_name_for_frame(stack)
        expected = f"-> in: {method_name}(){filename}"
        self.log_line(expected)
        self.tabbing = self.tabbing + 1
        yield
        self.tabbing = self.tabbing - 1
        expected = f"<- out: {method_name}(){filename}"
        self.log_line(expected)
        pass

    def log_line(self, text: str, use_timestamps=True) -> None:
        if self.counter != 0:
            self.logger("\n")
            self.counter = 0
        timestamp = self.get_timestamp() if use_timestamps else ""
        output_message = f"{timestamp}{self.get_tabs()}{text}\n"
        self.logger(output_message)

    def get_timestamp(self) -> str:
        timestamp = ""
        if self.log_with_timestamps:
            time1: datetime.datetime = self.timer()
            time = time1.strftime("%Y-%m-%dT%H:%M:%SZ")
            diff_millseconds = 0
            if self.previous_timestamp != None:
                delta = time1 - self.previous_timestamp
                diff_millseconds = int((delta).total_seconds() * 1000)
            diff = diff_millseconds
            diff_display = f" ~{diff:06}ms"
            timestamp = f"[{time} {diff_display}] "
            self.previous_timestamp = time1
        return timestamp

    def hour_glass(self) -> None:
        if not self.toggles.hour_glass:
            return

        self.increment_hour_glass_counter()
        if self.counter == 1:
            self.logger(f"{self.get_tabs()}.")
        elif self.counter == 100:
            self.logger("10\n")
            self.counter = 0
        elif self.counter % 10 == 0:
            digit = int(self.counter / 10)
            self.logger(f"{digit}")
        else:
            self.logger(".")

    def get_tabs(self) -> str:
        return "  " * self.tabbing

    def increment_hour_glass_counter(self) -> None:
        self.counter = self.counter + 1

    def variable(self, name: str, value: Any, show_types: bool = False) -> None:
        if not self.toggles.variables:
            return

        if _is_iterable(value):
            self.log_line(f"variable: {name}.length = {len(value)}")
            for (i, v) in enumerate(value):
                self.logger(f"{name}[{i}] = {v}\n")
        else:
            type_text = ""
            if show_types:
                type_text = f" <{type(value).__name__}>"
            self.log_line(f"variable: {name} = {value}{type_text}")

    def event(self, event_name: str) -> None:
        if not self.toggles.events:
            return
        self.log_line(f"event: {event_name}")

    def query(self, query_text: str) -> None:
        if not self.toggles.queries:
            return
        self.log_line(f"Sql: {query_text}")

    def message(self, message):
        if not self.toggles.messages:
            return
        self.log_line(f"message: {message}")

    def warning(self, text: str = "", exception: Exception = None) -> None:
        if isinstance(text, Exception):
            temp = ""
            if exception:
                temp = str(exception)
            exception = text
            text = temp

        warning_stars = "*" * 91
        self.log_line(warning_stars, use_timestamps=False)
        if self.log_with_timestamps:
            self.log_line("", use_timestamps=True)
        if text:
            self.log_line(f"Message:{text}", use_timestamps=False)
        if exception:
            if self.log_stack_traces:
                format_exception = traceback.format_exception(
                    None, exception, exception.__traceback__
                )
                stack_trace = "".join(format_exception)
            else:
                stack_trace = to_string(exception)
            self.log_line(stack_trace, use_timestamps=False)
        self.log_line(warning_stars, use_timestamps=False)

    def show_queries(self, show):
        self.toggles.queries = show

    def show_all(self, show: bool) -> None:
        self.toggles = Toggles(show)

    def show_messages(self, show):
        self.toggles.messages = show

    def show_variables(self, show):
        self.toggles.variables = show

    def show_hour_glass(self, show):
        self.toggles.hour_glass = show

    def show_markers(self, show):
        self.toggles.markers = show

    def show_events(self, show):
        self.toggles.events = show
