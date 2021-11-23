# -*- coding: utf-8 -*-
import re


"""
Copyright (c) 2010-2016  João S. O. Bueno - <gwidion@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

------------------------------------------------------------------------------

Exemplo didático de implementação de programação orientada
a aspectos com Python.

Sem otimizações que seriam prematuras
Caso deseje um uso real programação orientada a aspectos com python,
existem alguns projetos bem mantidos em repositórios apropriados
na internet. È melhor usar um desses do que re-inventar a roda
"""
class Aspecter(type):
    """
        Meta classe usada por classes que terão métodos orientados
        a aspecto (com os join-points e cross-cut points e etc.

        O objeto aspect_rules contém todas as regras de aspecto
    """
    aspect_rules = []
    wrapped_methods = []
    def __new__(cls, name, bases, dict):
        """
            Inicialização de classe que contém métodos orientados a aspectos.
            Basicamente anota todos os métodos da classe de forma que a cada
            chamada possa ser verificado se há uma regra correspondente
            aos mesmos:
        """
        for key, value in dict.items():
            if hasattr(value, "__call__") and key != "__metaclass__":
                dict[key] = Aspecter.wrap_method(value)
        return type.__new__(cls, name, bases, dict)

    @classmethod
    def register(cls, name_pattern="", in_objects=(), out_objects=(),
                 pre_function=None,
                 post_function=None):
        """
             Método usado para registrar uma nova regra de aspecto.
             O registro pode ser feito dinamicamente em tempo de execução
             name_pattern: é uma expressão regular que casa com o nome dos
             métodos. em branco, casa com todos os métodos.

             Em particular, note que esse esquema simplificado não dá conta
             de chamar uma pre_function baseando-se em out_objects
        """
        # Método to simples que poderia ser usado um append direto em
        # "aspect rules"
        rule = {"name_pattern": name_pattern, "in_objects": in_objects,
                 "out_objects": out_objects,
                 "pre": pre_function, "post": post_function}
        cls.aspect_rules.append(rule)

    @classmethod
    def wrap_method(cls, method):
        def call(*args, **kw):
            pre_functions =  cls.matching_pre_functions(method, args, kw)
            for function in pre_functions:
                function(*args, **kw)
            results = method(*args, **kw)
            post_functions = cls.matching_post_functions(method, results)
            for function in post_functions:
                function(results, *args, **kw)
            return results
        return call

    @classmethod
    def matching_names(cls, method):
        return [rule for rule in cls.aspect_rules
                    if re.match(rule["name_pattern"], method.func_name)
                       or rule["name_pattern"] == ""
               ]

    @classmethod
    def matching_pre_functions(cls, method, args, kw):
        all_args = args + tuple(kw.values())
        return [rule["pre"] for rule in cls.matching_names(method)
                    if rule["pre"] and
                        (rule["in_objects"] == () or
                         any((type(arg) in rule["in_objects"] for arg in all_args)))
               ]
    @classmethod
    def matching_post_functions(cls, method, results):
        if type(results) != tuple:
            results = (results,)
        return [rule["post"] for rule in cls.matching_names(method)
                    if rule["post"] and
                       (rule["out_objects"] == () or
                        any((type(result) in rule["out_objects"] for result in results)))
               ]

if __name__ == "__main__":
    #testing
    class Address(object):
        def __repr__(self):
            return "Address..."


    class Person(object):
        __metaclass__ = Aspecter
        def updateAddress(self, address):
            pass
        def __str__(self):
            return "person object"

    def log_update(*args, **kw):
        print "Updating object %s" %str(args[0])

    def log_address(*args, **kw):
        addresses = [arg for arg in (args + tuple(kw.values()))
                    if type(arg) == Address]
        print addresses

    Aspecter.register(name_pattern="^update.*", pre_function=log_update)
    Aspecter.register(in_objects=(Address,), pre_function=log_address)

    p = Person()
    p.updateAddress(Address())

