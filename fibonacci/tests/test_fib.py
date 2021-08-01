from fibonacci.naive import fibonacci_naive


def test_naive() -> None:
    res = fibonacci_naive(n = 0)
    assert res == 0

    res = fibonacci_naive(n=1)
    assert res == 1

    res = fibonacci_naive(n=2)
    assert res == 1

    res = fibonacci_naive(n=20)
    assert res == 6765