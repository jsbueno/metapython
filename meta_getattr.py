class Meta(type):
    def __getattribute__(self, attr):
        if attr.startswith("__"):
            return type.__getattribute__(self, attr)
        print attr, dir(self.__dict__[attr])
        v =  type.__getattribute__(self, attr)
        print attr, dir(v)
        return v


__metaclass__ = Meta

class A:
    def a(self):
        pass

