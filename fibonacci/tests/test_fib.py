from fibonacci.naive import fibonacci_naive
import pytest
from my_decorator import my_parametrized


@pytest.mark.parametrize("n,expected", [(0, 0), (1, 1), (2, 1), (20, 6765)])
def test_naive(n: int, expected: int) -> None:
    res = fibonacci_naive(n=n)
    assert res == expected

# create our own parametrize and use it to test naive
@my_parametrized(identifiers = "n,expected", values = [(0, 0), (1, 1), (2, 1), (20, 6765)])
def test_naive_with_my_decorator(n: int, expected: int) -> None:
    res = fibonacci_naive(n=n)
    assert res == expected
