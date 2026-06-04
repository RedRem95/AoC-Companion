#  Copyright (c) 2022  RedRem
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime
import json
import os
import sys
from typing import Optional, Union, List, Iterable, AnyStr, Callable, Any
import inspect

from AoC_Companion.Day import Collection, Result
from AoC_Companion import __version__
from AoC_Companion.Data.input_data import get_data


def run(
        years: List[int] = None, days: List[int] = None, tasks: List[int] = None,
        stream: Callable[[AnyStr], None] = None, log: bool = True
):
    if stream is None:
        stream = sys.stdout.write

    stream(f"┏ Running AoC-Companion {__version__} (PY {'.'.join(str(x) for x in sys.version_info[:3])})\n")
    first = True

    def log_fnc(_t: Any):
        if log:
            _t = str(_t)
            _lines = _t.strip("\n").split("\n")
            for _l in _lines:
                stream(f"┃ │     {_l} \n")

    run_time = 0
    counter = 0
    years_set = set()
    days_set = set()

    for ydt, fnc, _ in Collection.iterate(years=years, days=days, tasks=tasks):
        data, preproc_count = get_data(year=ydt[0], day=ydt[1], task=ydt[2])
        if not first:
            stream(f"┣{'━' * 30}\n")
        stream(f"┠─┬Year: {ydt[0]:4d}; Day: {ydt[1]:2d}; Task {ydt[2]} ({preproc_count} preprocessors)\n")
        if log:
            stream(f"┠─┼─Log: \n")
        res: Result = fnc(data, log=log_fnc)
        stream(f"┠─┼Runtime: {datetime.timedelta(seconds=res.exec_time)}\n")
        stream(f"┠─┴Result: {res.data}\n")

        run_time += res.exec_time
        counter += 1
        years_set.add(ydt[:1])
        days_set.add(ydt[:2])

        first = False

    stream(f"┗ Ran {counter} tasks from {len(years_set)} years and {len(days_set)} days in {datetime.timedelta(seconds=run_time)}\n")
