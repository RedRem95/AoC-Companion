"""
    AoC-Companion download code so its easier to download data from AoC
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

from typing import Optional

import requests


def input_url(day: int, year: int) -> str:
    return f'https://adventofcode.com/{year}/day/{day}/input'


def download(url: str, session_id: str, verbose: bool = True) -> Optional[str]:
    # TODO: Add check to not spam server
    cookies = {'session': session_id}
    headers = {'User-Agent': 'Mozilla/5.0'}
    if verbose:
        print(f"Download from {url}")
    response = requests.get(url, cookies=cookies, headers=headers)
    return response.text
