from functools import lru_cache

cache = {}


def fibonacci_cached(n: int) -> int:
    if n in cache:
        return cache[n]

    if n == 0 or n == 1:
        return n

    fn = fibonacci_cached(n - 1) + fibonacci_cached(n - 2)
    cache[n] = fn
    return fn


# the same as fibonacci_cached
# will automatically save the result to cache
@lru_cache(maxsize=256)
def fibonacci_lru_cached(n: int) -> int:
    if n == 0 or n == 1:
        return n

    return fibonacci_lru_cached(n - 1) + fibonacci_lru_cached(n - 2)
