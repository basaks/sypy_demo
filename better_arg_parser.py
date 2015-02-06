class function(type):
    @property
    def varnames(kls):
        return kls.__call__.__code__.co_varnames[1:]

    @property
    def argcount(kls):
        return kls.__call__.__code__.co_argcount - 1

    def __init__(kls, name, bases, nmspc):
        if not hasattr(kls, 'cache'):
           kls.cache = False

        if kls.cache is True:
            if not hasattr(kls, 'values'):
                kls.values = {}

        if len(kls.vartypes) != len(kls.varnames):
             raise ValueError

        if len(kls.varnames) != kls.argcount:
            if len(kls.varnames) < kls.argcount:
                raise NotImplementedError

            if len(kls.varnames) > kls.argcount + 1:
                raise NotImplementedError

            # here - check that it is a tuple/list
            if kls.vartypes[kls.argcount] not in [tuple, list]:
                raise NotImplementedError("not sure if this will work!")

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
        if len(args) < kls.argcount:
             raise ValueError

        for i in range(kls.argcount):
            if not isinstance(args[i], kls.vartypes[i]):
                raise TypeError

        if len(args) > kls.argcount:
            if not isinstance(args[kls.argcount:], kls.vartypes[kls.argcount]):
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
class sum_series(object):
    __metaclass__ = function
    vartypes = [tuple]
    cache  = True
    values = {(): 0}
    def __call__(self, *a):
        return a[0] + sum_series(*a[1:])
###################################################################################################
if __name__ == '__main__':
    assert(sum_series(1, 2) == 3)

