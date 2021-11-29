from typing import Set, TypeVar

_T = TypeVar("_T")


def common(*sets: Set[_T]) -> Set[_T]:
    if len(sets) == 0:
        return set()
    ret = sets[0]
    for s in sets[1:]:
        ret = ret & s
    return ret
