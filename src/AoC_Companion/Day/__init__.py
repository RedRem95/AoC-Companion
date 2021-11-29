import datetime
import json
import os
import time
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Optional, Dict, List, Generator, Any, Tuple, Iterable

from AoC_Companion.misc import download


NOT_UNLOCKED_MESSAGE = "Please don't repeatedly request this endpoint before it unlocks! The calendar countdown is synchronized with the server time; the link will be enabled on the calendar the instant this puzzle becomes available."

class StarTask(IntEnum):
    Task01 = 1
    Task02 = 2


class TaskResult:
    def __init__(self, day: "Day", task: StarTask, result: str, duration: float, log: List[str] = None):
        self._day = day
        self._task = task
        self._result = result
        self._duration = duration
        self._log: List[str] = [] if log is None else log.copy()

    def get_day(self) -> "Day":
        return self._day

    def get_task(self) -> StarTask:
        return self._task

    def get_result(self) -> str:
        return self._result

    def get_duration(self) -> float:
        return self._duration

    def get_log(self) -> List[str]:
        return self._log.copy()

    def to_string(self, show_log: bool = True) -> List[str]:
        ret = [
            f"{self.get_day().get_name()} - {self.get_task().name}: {self.get_result()}",
            f"{'Duration':14s}: {datetime.timedelta(seconds=self.get_duration())}"
        ]
        log = self.get_log()
        if show_log and len(log) > 0:
            ret.append("Log:")
            for line in log:
                ret.append(f"    {line}")

        return ret

    @staticmethod
    def format(results: List["TaskResult"], show_log: bool = True) -> str:
        if len(results) == 0:
            return "No results"
        lines = []
        max_len = 0
        for r in results:
            lines.append(r.to_string(show_log=show_log))
            max_len = max(max_len, max(len(x) for x in lines[-1]))
        tmpl = "| {line:%ss} |" % (max_len)
        split_line = "".join(("+", '-' * (max_len + 2), "+"))
        ret = [split_line]
        for r in lines:
            for line in r:
                ret.append(tmpl.format(line=line))
            ret.append(split_line)
        return "\n".join(ret)


class Day(ABC):
    _days: Dict[Tuple[int, int], "Day"] = {}

    @classmethod
    def register_day(cls, day: "Day", *args, **kwargs):
        day_id = day.get_day()
        if day_id is None:
            raise KeyError(f"Class {day.__class__} has no valid formatted day. "
                           f"Please check class name or get_day function")
        cls._days[(day.get_year(), day_id)] = day

    def __init__(self, year: int, session_id: str = None):
        self._year = year
        self._session_id = session_id or os.environ.get("AoC_SESSION")
        self.register_day(self)

    def run_all(self, data: Any) -> Dict[StarTask, TaskResult]:
        ret = {}
        for task in sorted(StarTask, key=lambda x: x.value):
            res = self.run(task=task, data=data)
            if res is not None:
                ret[task] = res
        return ret

    def run(self, task: StarTask, data: Any) -> Optional[TaskResult]:
        if task == StarTask.Task01:
            return self.run_t1(data=data)
        if task == StarTask.Task02:
            return self.run_t2(data=data)
        raise KeyError(f"Task {task.name} not implemented")

    @abstractmethod
    def run_t1(self, data: Any) -> Optional[TaskResult]:
        return None

    @abstractmethod
    def run_t2(self, data: Any) -> Optional[TaskResult]:
        return None

    # noinspection PyMethodMayBeStatic
    def pre_process_input(self, data: Any) -> Any:
        data = str(data)
        return data.split("\n")

    def construct_data_package(self) -> Any:
        raw_data = self.get_input()
        return self.pre_process_input(data=raw_data)

    @classmethod
    def get_days(cls) -> List["Day"]:
        return list(Day.__iter__())

    @classmethod
    def __class_getitem__(cls, item: Tuple[int, int]) -> "Day":
        return cls._days[item]

    @classmethod
    def __iter__(cls) -> Iterable["Day"]:
        for i in sorted(cls._days.keys()):
            yield Day.__class_getitem__(item=i)

    def get_name(self) -> str:
        return self.__class__.__name__

    def get_day(self) -> Optional[int]:
        try:
            return int(self.get_name()[3:])
        except (ValueError, KeyError):
            return None

    def get_year(self) -> int:
        return self._year

    def get__file__(self) -> str:
        import inspect
        try:
            ret = inspect.getfile(self.__class__)
            if (ret is None) or (len(ret) <= 0) or (not os.path.exists(ret)):
                raise ValueError()
            return ret
        except (TypeError, ValueError):
            raise NotImplementedError(f"Could not get file {self.__class__.__name__} is defined in"
                                      "Please make sure inspect can find the file or "
                                      f"override Day.get__file__() in {self.__class__.__name__}")

    def get_input(self) -> Any:
        input_file = os.path.abspath(os.path.join(os.path.dirname(self.get__file__()), "input.txt"))
        if not os.path.exists(input_file):
            downloaded_data = download.download(
                url=download.input_url(day=self.get_day(), year=self.get_year()),
                verbose=True,
                session_id=self._session_id
            )
            if downloaded_data is not None and downloaded_data.strip() != NOT_UNLOCKED_MESSAGE:
                with open(input_file, "wb") as f_out:
                    f_out.write(downloaded_data.encode("utf-8"))

        try:
            with open(input_file, "rb") as f_in:
                return f_in.read().decode("utf-8")
        except FileNotFoundError:
            return ""
