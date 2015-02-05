from property import *
###################################################################################################
class typed_property(property):
    def __init__(kls, name, bases, nmspc):
        kls.cache = True
        kls.values = {}
    
    def __getitem__(kls, a):

        if a in kls.values:
            return kls.values[a]
        raise KeyError

    def __setitem__(kls, *args):
        key = args[0]
        val = args[1]

        if not isinstance(key, kls.key_type):
            raise TypeError
        
        if not isinstance(val, kls.value_type):
            raise TypeError

        kls.values[key] = val

    def __call__(kls, *args):
        if len(args) == 1:
            return kls[args[0]]
        elif len(args) == 2:
            kls[args[0]] = args[1]
            return args[1]
        else:
            raise KeyError

###################################################################################################
class name(metaclass = typed_property):
    key_type = str
    value_type = str
 
if __name__ == '__main__':
    name("harbour bridge", "old coat hanger")
    print(name("harbour bridge"))

    name(1, "ten")
