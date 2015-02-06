###################################################################################################
class binary_function(type):
    def __call__(kls, a, b):
        return super(binary_function, kls).__call__()(a, b)

###################################################################################################
def fold(kls):
    def call(self, *args):
        return kls.fn(args[0], kls(*args[1:]))
    return call

###################################################################################################
class seq_function(type):
    def __init__(kls, name, bases, nmspc):
        if not hasattr(kls, 'cache'):
           kls.cache = False

        if kls.cache is True:
            if not hasattr(kls, 'values'):
                kls.values = {}

        if not isinstance(kls.fn, binary_function):
            raise TypeError

        kls.__call__ = fold(kls)

    def __getitem__(kls, args):
        if args in kls.values:
            return kls.values[args]

        raise KeyError

    def __setitem__(kls, *args):
        key = args[0:-1]
        val = args[-1]
        kls.values[key] = val

    def __call__(kls, *args):
        if kls.cache is True and args in kls.values:
            ret = kls[args]
        else:
            f = super(seq_function, kls).__call__()
            ret = f(*args)
            if kls.cache:
                kls[args] = ret
        
        return ret

###################################################################################################
class add(metaclass = binary_function):
    def __call__(self, a, b):
        return a + b

class sum_series(metaclass = seq_function):
    cache = True
    fn = add
    values  = {():0}
    def __call__(self, *args):
        return add(args[0], sum_series(*args[1:]))

###################################################################################################
class mul2(object):
    __metaclass__ = binary_function
    def __call__(self, a, b):
        return a * b 

class mul(metaclass = seq_function):
    cache = True
    fn = mul2
    values = {(): 1}


###################################################################################################
if __name__ == '__main__':
    assert(sum_series(1, 2, 3) == 6)
    assert(mul(1, 2, 3) == 6)

