import functools
import operator

from typing import Tuple


def vec_sum(*vecs: Tuple[int, int]) -> Tuple[int, int]:
    return tuple(map(sum, zip(*vecs)))


def vec_mul(*vecs: Tuple[int, int]) -> Tuple[int, int]:
    def prod(iterable):
        return functools.reduce(operator.mul, iterable, 1)

    return tuple(map(prod, zip(*vecs)))
