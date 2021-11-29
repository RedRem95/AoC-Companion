from typing import Optional

import requests


def input_url(day: int, year: int) -> str:
    return f'https://adventofcode.com/{year}/day/{day}/input'


def download(url: str, session_id: str, verbose: bool = True) -> Optional[str]:
    cookies = {'session': session_id}
    headers = {'User-Agent': 'Mozilla/5.0'}
    if verbose:
        print(f"Download from {url}")
    response = requests.get(url, cookies=cookies, headers=headers)
    return response.text
