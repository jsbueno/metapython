#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author: João S. O. Bueno
# copyright (c): João S. O. Bueno 2009
# License: LGPL V3.0

# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this module; if not, see <http://www.gnu.org/licenses/>.


# KNOWN Bugs: 
# 1) Could not make it work for arithmetic operations with float or complex
# when the lazy evaluated value is a number. (Maybe explicetly implement the
# __r..__ methods? )
# 2) Some sequence type methods for non -sequence objects
# are returning "not implemented" when they should raise a typeerror


from functools import wraps
def lazy(func):
    class Template(object):
        def __init__(self, *args, **kw):
            self.args = args
            self.kw = kw
            self.executed = False
        def _exec(self):
            if not self.executed:
               self.value = func(*self.args, **self.kw)
               self.executed = True
            return self.value
        
        def __setattr__(self, attr, value):
            if attr not in ("args", "kw", "executed", "value"):
                return setattr(self._exec(), attr, value)
            return object.__setattr__(self, attr, value)
            
        def __getattr__(self, attr):
            if attr not in ("args", "kw", "executed", "value"):
                return self._exec().__getattribute__(attr)
            return object.__getattr__(self, attr)
        
        def __unicode__(self):
            return unicode(self._exec())
        
        # FIXME, DOUBT: should the closure's values be frozen at function call time? guess not!
        func_closure = func.func_closure
        
    # The core of it all: create a a suply of every possible way of using an 
    # object, assuring the function call happens as the object is used
    
    #FIXME: Maybe remove the actual function call one further level,
    # creating a class at the evaluation moment
    # so that once the function is evaluated, only the pertinent
    # methods would  exist for the class
    
    def meta_meta_method(method_name, error="TypeError"):
        def meta_method(self, *args,**kw):
            #FIXME: will get strange not implemented errors - example:
            # "NotImplemented: '__getitem__'" instead of:
            # "TypeError: 'int' object is unsubscriptable"
            # for the delayed function call returned values
            try:
                method = getattr(self._exec(), method_name)
            except AttributeError:
                if error == "NotImplemented":
                    return NotImplemented
                else:
                    raise TypeError, ("%s object can't do %s" % (
                                      type(self._exec()),
                                      method_name.replace("__", "")
                                   ))
            return method(*args,**kw)
            #FIXME: maybe this hides the nature of these objects
            #and maybe this hiding should be avoided at all:
            meta_method.func_name = method_name
        return meta_method
    
    optional_methods = """__lt__ __eq__ __ne__ __gt__ __ge__ """.split()
    
    data_model_methods = """
        __repr__ __str__ __cmp__
        __hash__  __nonzero__
        __delattr__
        __call__
        __len__ __getitem__ __setitem__ __delitem__ __reversed__ __contains__
        __add__ __sub__ __mul__ __floordiv__ __mod__ __divmod__ __pow__  __div__ __truediv__
        __lshift__  __rshift__ __and__ __xor__ __or__
        __radd__ __rsub__ __rmul__ __rfloordiv__ __rmod__ __rdivmod__
        __rpow__ __rdiv__ __rtruediv__
        __rlshift__  __rrshift__ __rand__ __rxor__ __ror__
        __iadd__ __isub__ __imul__ __ifloordiv__ __imod__  __ipow__ __idiv__ __itruediv__
        __ilshift__  __irshift__ __iand__ __ixor__ __ior__
        __neg__ __pos__ __abs__ __invert__
        __complex__ __int__ __long__ __float__
        __oct__ __hex__
        __index__ __coerce__
    """.split()
    optional_methods = """__lt__ __eq__ __ne__ __gt__ __ge__  __unicode__""".split()
    # FIXME: left out: __getslice__ __setslice__ __delslice__
    
    data_model_dict = dict([(method_name, meta_meta_method(method_name))
                               for method_name in data_model_methods]) 
    optional_dict = dict([(method_name, meta_meta_method(method_name, error="NotImplemented"))
                               for method_name in data_model_methods]) 
    
    data_model_dict.update(optional_dict)
    
    LazyFuncClass = type("Lazy_%s" %func.func_name, (Template,), data_model_dict)
   
    #functools.wraps -> for decorators: preserves some of the original function attributes
    @wraps(func)
    def _call_(*args,**kw):
        return LazyFuncClass (*args,**kw)
    
    return _call_

if __name__ == "__main__":
    @lazy
    def bla(x):
        print "bla in execution for %s" % x
        return x
    ob_a = bla(3)
    print "ob_a created - should be evaluated in the line bellow"
    print ob_a + 2

"""
@lazy
def proc():
    return proc()


class Tracer(object):
    def __getattribute__(self, attr):
        print attr
        return object.__getattribute__(self, attr)

from lazy_decorator import lazy

@lazy
def openfile(fn, mode="rt"):
   print "opening" ,  fn
   return open(fn, mode)

arq = openfile("teste", "wb")

class A(object):
  @lazy
  def add(self, a, b):
    print "adding: %s, %s" %(a,b)
    return a + b
    
@lazy
def bla(x):
    print "bla in execution for %s" % x
    return x
"""