"""
    AoC-Companion main file that houses the container class that makes it easy to call days and auto import them
    Copyright (C) 2021  RedRem

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import datetime
import json
import os
import sys
from typing import Optional, Union, List, Iterable

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

        days_iterator: Iterable[Union[int]] = days
        try:
            if len(days) > 1:
                # noinspection PyUnresolvedReferences
                import tqdm
                days_iterator = tqdm.tqdm(days_iterator, desc="Running days", leave=False, unit="d")
        except ImportError:
            pass

        ret = []
        for d in days_iterator:
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
                try:
                    tmp_class = getattr(tmp, folder)
                    ret.append(tmp_class(**args))
                except AttributeError:
                    sys.stderr.write(f"Found matching module {tmp} but could not find correctly formatted class inside"
                                     f"\nSearched for class {folder}"
                                     f"\nPlease check that the class name is the same as the surrounding package and "
                                     f"the parameters are correctly setup\n")

        return ret
