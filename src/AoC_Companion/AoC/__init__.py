import os
import datetime
from typing import Optional, Union, List, Dict
import json

from AoC_Companion.Day import Day, TaskResult


class AoC:

    def __init__(self, year: int = None, source_folder: str = None, base_folder: str = None):
        self._year = year or datetime.datetime.now().year
        if source_folder is not None:
            self.auto_import(source_folder=source_folder, year=self.get_year(), base_folder=base_folder)

    def run(self, *days: Optional[Union[int]]) -> List[TaskResult]:
        """
        Runs AoC_Companion
        :param day:
            if None is given runs all
        :return:
        """
        if len(days) == 0:
            days = tuple(x.get_day() for x in self.get_days())

        ret = []
        for d in days:
            try:
                day: Day = Day.__class_getitem__(item=(self.get_year(), d))
                data = day.construct_data_package()
                res = day.run_all(data=data)
                for r in sorted(res.keys(), key=lambda x: x.value):
                    ret.append(res[r])
            except KeyError:
                pass
        return ret

    def run_latest(self) -> List[TaskResult]:
        return self.run(self.get_days()[-1].get_day())

    def get_days(self) -> List[Day]:
        return list(x for x in Day.get_days() if x.get_year() == self.get_year())

    def get_year(self) -> int:
        return self._year

    @staticmethod
    def auto_import(source_folder: str, year: int, base_folder: str = None) -> List[Day]:
        if base_folder is None:
            base_folder = os.path.dirname(source_folder)
        import importlib
        ret = []
        for folder in (x for x in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, x))):
            folder_abs = os.path.join(source_folder, folder)
            if os.path.exists(folder_abs) and \
                    os.path.isdir(folder_abs) and \
                    os.path.exists(os.path.join(folder_abs, "__init__.py")):
                args = {"year": year}
                if os.path.exists(os.path.join(folder_abs, "config.json")):
                    with open(os.path.join(folder_abs, "config.json"), "rb") as conf_in:
                        args.update(json.load(conf_in))
                module_dir = os.path.relpath(os.path.join(source_folder, folder), base_folder)
                tmp = importlib.import_module(module_dir.replace(os.path.sep, "."))
                tmp = getattr(tmp, folder)
                ret.append(tmp(**args))
        return ret
