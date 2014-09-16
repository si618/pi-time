import functools

def method(publish=None):
    def decorator(func, *args, **kwargs):
        @functools.wraps(func)
        def wrapper(self, func, *args, **kwargs):
            print "Before {} function runs".format(func)
            func(self, *args, **kwargs)
            print "After {} function runs".format(func)
        return wrapper
    return decorator

