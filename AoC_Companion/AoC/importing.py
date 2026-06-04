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

import os
import sys
import importlib
import importlib.util


def import_stuff(path: str):
    path = os.path.abspath(path=path)
    spec = importlib.util.spec_from_file_location("AoC", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["AoC"] = mod
    spec.loader.exec_module(mod)
