import inspect

def ActionBinder(func):
    def wrapper(*args, **kargs):
        missing = missingargs(func, kargs)
        for m in missing:
            if m != 'self' and args[0].request.get(m, '') != '':
                kargs[m] = args[0].request.get(m)
        return func(*args, **kargs)
    return wrapper

def getrequiredargs(func):
    args, varargs, varkw, defaults = inspect.getargspec(func)
    if defaults:
        args = args[:-len(defaults)]
    return args   # *args and **kwargs are not required, so ignore them.

def missingargs(func, argdict):
    return set(getrequiredargs(func)).difference(argdict)

def invalidargs(func, argdict):
    args, varargs, varkw, defaults = inspect.getargspec(func)
    if varkw:
        return set()  # All accepted
    return set(argdict) - set(args)