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

from typing import Callable, AnyStr

import numpy as np

from AoC_Companion.Day import Task
from AoC_Companion.Preprocess import Preprocessor


@Task(year=2021, day=1, task=1)
def task01(data, log: Callable[[AnyStr], None]):
    res = _count_inc(data[:-1], data[1:])
    log(f"There are {len(data)} measurements")
    return res


@Task(year=2021, day=1, task=2)
def task02(data, log: Callable[[AnyStr], None]):
    window_size = 3
    res = 0
    for i in range(window_size + 1, data.shape[0] + 1):
        res += 1 if data[i - window_size - 1:i - 1].sum() < data[i - window_size:i].sum() else 0
    log(f"There are {len(data)} measurements")
    return res


@Preprocessor(year=2021)
def preproc_0(data: str):
    return data.split("\n")


@Preprocessor(year=2021, day=1)
def preproc_1(data):
    data = np.array([int(x) for x in data if len(x) > 0], dtype=np.int32)
    return data


def _count_inc(data1: np.ndarray, data2: np.ndarray):
    return np.sum(data1 < data2)
