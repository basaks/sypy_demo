class unary_function(type):
    def __init__(kls, name, bases, nmspc):
        if not hasattr(kls, 'cache'):
           kls.cache = False

        if kls.cache is True:
            if not hasattr(kls, 'values'):
                kls.values = {}

    def __getitem__(kls, arg):
        if arg in kls.values:
            return kls.values[arg]

        raise KeyError

    def __setitem__(kls, key, val):
        kls.values[key] = val


    def __call__(kls, arg):
        if kls.cache is True and arg in kls.values:
            ret = kls[arg]
        else:
            f = super(unary_function, kls).__call__()
            ret = f(arg)
            if kls.cache:
                kls[arg] = ret
        
        return ret

class naive_fibonacci(object):
    __metaclass__ = unary_function
    cache = True
    values = {0: 1, 1: 1}
    def __call__(self, a):
        return naive_fibonacci(a - 1) + naive_fibonacci(a -2)

###################################################################################################
if __name__ == '__main__':
    print(naive_fibonacci(10))
