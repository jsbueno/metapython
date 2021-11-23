# -*- coding: utf-8 -*-
from functools import wraps


class Staticator(object):
    def __init__(self, *args, **kw):
        self.types = args
        self.kw_types = kw
    
    def __call__(self, function):
        self.func_name = function.func_name
        @wraps(function)
        def new_function(*args, **kw):
            self.check_args(args, kw)
            return function(*args, **kw)
        return new_function
    
    def raise_type_error(self, arg, type_):
        raise TypeError(
            "Incorrect argument %s - should be of type %s in call to %s()" %
            (str(arg), str(type_), self.func_name))
    
    def check_args(self, args, kw):
        for type_, arg in zip(self.types, args):
            if not isinstance(arg, type_):
                self.raise_type_error(arg, type_)
        for key in kw:
            try:
                if not isinstance(kw[key], self.kw_types[key]):
                    self.raise_type_error(kw[key], type_)
            except KeyError:
                 raise TypeError("%s() got an unexpected "
                                 "keyword argument '%s'" %
                                 (self.func_name, key))

if __name__ == "__main__":
    @Staticator(int, int)
    def sum(a, b):
        return a + b

    sum(2,3)
    sum(2.0, 3)