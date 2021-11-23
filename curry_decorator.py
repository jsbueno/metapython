# -*- coding: utf-8 -*-
from functools import partial, wraps

"""Curry decorator for "currying" functions acording to lambda calculus.
Check http://en.wikipedia.org/wiki/Lambda_calculus 
for more
"""

def curry(func):
    @wraps(func)
    def wrapper(*args, **kw):
        return partial(func, *args, **kw)
    return wrapper

if __name__ == "__main__":
    @curry
    def somaquad(a, b):
        return a * a + b * b

    b = somaquad(3)(4)
    print b