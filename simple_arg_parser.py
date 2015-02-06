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

    def check_positional_args(kls, *args):
        """
            Positional args have to be specified in the order in which they are mentioned in the class fields.
        """
        if len(args) == len(kls.arguments):
            # there is a one to one correspondence
            for i in range(len(args)):
                if not isinstance(args[i], kls.arguments[i]):
                    raise TypeError

    def __call__(kls, *args):
        # check the args
        kls.check_positional_args(*args)

        if kls.cache is True and args in kls.values:
            ret = kls[args]
        else:
            f = super(function, kls).__call__()
            ret = f(*args)
            if kls.cache:
                kls[args] = ret
        
        return ret

###################################################################################################
class add(object):
    __metaclass__ = function
    arguments = (int, int)
    def __call__(self, a, b):
        return a + b
###################################################################################################
if __name__ == '__main__':
    assert(add(1, 2) == 3)

