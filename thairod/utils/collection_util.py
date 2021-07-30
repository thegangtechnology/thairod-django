from typing import TypeVar, List, Tuple

T1 = TypeVar('T1')
T2 = TypeVar('T2')


def pair_leftover(a: List[T1], b: List[T2]) -> Tuple[List[Tuple[T1, T2]], List[T1], List[T2]]:
    pair = list(zip(a, b))
    leftover_a = []
    leftover_b = []
    if len(a) > len(b):
        leftover_a = a[len(b):]
    if len(a) < len(b):
        leftover_b = b[len(a):]
    return pair, leftover_a, leftover_b
