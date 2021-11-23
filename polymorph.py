# -*- coding: utf-8 -*-
from functools import wraps



class Polymorphator(object):
    __metaclass__ = type
    polymorphators = {}
    def __init__(self):
        if not hasattr(self.__class__, "current_class"):
            self.__class__.current_polymorphator = para_polymorphator_factory()
    def __call__(self, *args, **kw):
        return self.__class__.current_polymorphator(*args, **kw)
    @classmethod
    def commit_class(cls, class_name):
        cls.polymorphators[class_name] = cls.current_polymorphator
        cls.current_polymorphator = para_polymorphator_factory()


class MetaPolymorphator(type):
    def __new__(cls, name, bases, dict_):
        Polymorphator.commit_class(name)
        function_type = type(lambda:None)
        for key, value in dict_.items():
            if isinstance(value, function_type) and hasattr(value, "polymorphed"):
                base_homonimous = {} 
                # FIXME: not recursing bases (have to do so in proper reversed(MRO))
                for base in reversed(bases):
                    base_name = base.__name__
                    if base_name in Polymorphator.polymorphators:
                        methods = Polymorphator.polymorphators[base_name].methods
                        if key in methods:
                            base_homonimous.update(methods[key])
                Polymorphator.polymorphators[name].methods[key].update(base_homonimous)
        return type.__new__(cls, name, bases, dict_)


__metaclass__ = MetaPolymorphator


def para_polymorphator_factory():
    class ParaPolymorphator(object):
        __metaclass__ = type
        methods = {}
        
        def __init__(self, *args, **kw):
            self.methods = {}
            self.signature = self.get_reg_signature(args, kw)
        
        def get_reg_signature(self, args, kw):
            return (tuple(args), tuple(sorted(kw.items())))
            
        def get_run_signature(self, args, kw):
            argstuple = tuple((type(arg) for arg in args[1:]))
            kwtuple = tuple(sorted (((item[0], type(item[1])) for item in kw.items() )) )
            return (argstuple, kwtuple)
            
        def __call__(self, method):
            name = method.func_name
            if not name in self.__class__.methods:
                self.__class__.methods[name] = {self.signature: method}
            else:
                self.__class__.methods[name][self.signature] = method
            @wraps(method)
            def new_function(*args, **kw):
                signature = self.get_run_signature(args, kw)
                try:
                    return self.__class__.methods[name][signature](*args, **kw)
                except KeyError:
                    raise TypeError("No method '%s' registered for signature %s"
                                 %(name, str(signature)))
            new_function.polymorphed = True
            return new_function
    return ParaPolymorphator

polymorphator = Polymorphator()

##testclasses:

class A:
    @polymorphator(int, int)
    def sum(self, a, b):
        print "A soma de %d e %d é: %d" % (a, b, a+b)

    @polymorphator(str, str)
    def sum(self, a, b):
        print "A concatenação de %s e %s é: %s" % (a, b, a + " - " + b)

class B:
    @polymorphator(float, float)
    def sum(self, a, b):
        print "A soma de %f e %f é: %f" % (a, b, a+b)
        
class C(A):
    @polymorphator(complex, complex)
    def sum(self, a, b):
        print "A soma dos complexos %s e %s é: %s" % (a, b, a+b)

if __name__ == "__main__":
    a = A()
    a.sum(2,3)
    a.sum("maçã", "laranja")
    b = B()
    b.sum(2.5,3.1)
    try:
        b.sum(2,3)
    except TypeError, error:
        print "Properly raised Typerror: %s" %error
    c = C()
    c.sum(1 + 1j, -1j)
    c.sum(4, 8)
    try:
        c.sum(2.1,3.1)
    except TypeError, error:
        print "Properly raised Typerror: %s" %error
