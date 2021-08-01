from typing import Callable

import pytest
from fibonacci.dynamic import fibonacci_dynamic, fibonacci_dynamic_v2
from fibonacci.naive import fibonacci_naive
from fibonacci.cached import fibonacci_cached
from fibonacci.cached import fibonacci_lru_cached
from conftest import time_tracker


@pytest.mark.parametrize(
    "fib_fun", [fibonacci_naive, fibonacci_cached, fibonacci_lru_cached, fibonacci_dynamic, fibonacci_dynamic_v2]
)
@pytest.mark.parametrize("n,expected", [(0, 0), (1, 1), (2, 1), (20, 6765)])
# Callable[[int], int]  receive an int and return an int
def test_fibonacci(time_tracker, fib_fun: Callable[[int], int], n: int, expected: int) -> None:
    res = fib_fun(n)
    assert res == expected
