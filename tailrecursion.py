from threading import currentThread

class TailRecursiveCall(Exception):
    pass

def tailrecursive(f):
    class Rec_f(object):
        def __init__(self):
            self.tr_d = {}
    
        def __call__(self, *args, **kw):
            self.args = args
            self.kw = kw
            thread = currentThread()
            if thread not in self.tr_d:
                self.tr_d[thread] = {}
                self.tr_d[thread]["depth"] = 0
                
            self.tr_d[thread]["depth"] += 1
            self.tr_d[thread]["args"] = args
            self.tr_d[thread]["kw"] = kw
            depth =  self.tr_d[thread]["depth"]
            if depth > 1:
                raise TailRecursiveCall
            over = False
            while not over:
                over = True
                args = self.tr_d[thread]["args"]
                kw = self.tr_d[thread]["kw"]
                #print "meta depth: %d" % depth
                try:
                    result = f (*args, **kw)
                except TailRecursiveCall:
                    self.tr_d[thread]["depth"] -= 1
                    over = False
            self.tr_d[thread]["depth"] -= 1
            return result
    
    return Rec_f()


def fatorial (n):
    if n == 1:
        return 1
    return n * fatorial(n -1)


@tailrecursive
def tail_fatorial (n, a=1):
    if n == 1:
        return a * 1
    return tail_fatorial(n -1, n * a)


if __name__ == "__main__":
        
    try:
        print "999! %d" % fatorial(999)
        print "2000! %d" % fatorial (2000)
    except RuntimeError, error:
        print "Fatorial normal quebrou: %s " % str(error)


    try:
        print "999! %d" % tail_fatorial(999)
        print "2000! %d" % tail_fatorial (3000)
    except RuntimeError, error:
        print "Fatorial tail tambem quebrou: %s" %str(error)
    