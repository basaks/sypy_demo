class function(type):
    def __init__(kls, name, bases, nmspc):
        if not hasattr(kls, 'cache'):
           kls.cache = False

        if kls.cache is True:
            if not hasattr(kls, 'values'):
                kls.values = {}

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
            f = super(function, kls).__call__()
            ret = f(*args)
            if kls.cache:
                kls[args] = ret
        
        return ret

###################################################################################################
def add(a, b):
    return a + b

class sum_series(object):
    __metaclass__ = function
    cache = True
    fn = add
    values = {(): 0}
    def __call__(self, *args):
        #print add(args[0], sum_series(*args[1:]))
        return add(args[0], sum_series(*args[1:]))

###################################################################################################
if __name__ == '__main__':
    print sum_series(1, 2, 3)
    assert(sum_series(1, 2, 3) == 6)
    # assert(sum_series(1, 2, 3, 4) == 10)
    # assert(sum_series(1, 2, 3, 4, 20) == 30)

