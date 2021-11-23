from inspect import stack

def define(*y):
    parent_frame = stack()[-2][0]
    parent_frame.f_globals[y[0]] = y[1] if (len(y) < 3 ) else y[1:]

d = define

def cond(*l):
    for item in l:
        if hasattr(item, "__len__") and len(item) >= 2:
            if item[0]:
                return item[1:]
            else:
                return item
    return None

c = cond

def if_(*l):
    return cond((l[0], l[1]), l[2] if len(l) == 2 else None)

def scheme(*l):
    if len(l):
        return l[0](*l[1:])
    else:
        return None

s = scheme

s(define, "add", lambda *x: sum(x))
s(define, "mul", lambda x, y: x * y)
s(define, "square", lambda x: s(mul, x, x))
s(define, "sum_of_squares", lambda x,y: s(add, s(square, x), s(square, y)))
print s(sum_of_squares, 3, 4)
