from functools import lru_cache

@lru_cache(maxsize=None)
def fib_memo(n):
    if n < 2:
        return n
    return fib_memo(n-1) + fib_memo(n-2)

print(fib_memo(50))