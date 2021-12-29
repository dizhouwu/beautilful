import cProfile
import functools
import time

import logging
import time


def timer(logger, level=None):
    if level is None:
        level = logging.INFO

    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            start = time.monotonic()
            result = func(*args, **kwargs)
            elapsed_time = time.monotonic() - start
            logger.log(level, f"Func {func.__qualname__} Elapsed time: {elapsed_time:0.4f} seconds")
            return result

        return inner

    return decorator


def profileit(func):
    @functools.wraps(func)  
    def wrapper(*args, **kwargs):
        datafn = func.__qualname__ + ".profile" 
        prof = cProfile.Profile()
        retval = prof.runcall(func, *args, **kwargs)
        prof.dump_stats(datafn)
        return retval

    return wrapper

from contextlib import contextmanager
@contextmanager
def time_out(seconds):
    class TimeOutException(Exception): pass
    def signal_handler(signum, frame):
        raise TimeOutException

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

        
import functools
def decorator(func=None,deco_arg='default'):
    if not callable(func):
        return functools.partial(decorator,deco_arg=deco_arg)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("deco_arg: ",deco_arg)
        schema = kwargs.get("schema")
        print("schema: ",schema)
        return func(*args, **kwargs)

    return wrapper

class A:

    @decorator(deco_arg="deco_arg1")
    def bar1(self,*, schema=None):
        pass
    
    @decorator(deco_arg="deco_arg2")
    def bar2(self,*, schema=None):
        pass
    
    @decorator
    def bar3(self,*, schema=None):
        pass

print(A().bar1(schema='schema1'))
print('-'*10)
print(A().bar2(schema='schema2'))
print('-'*10)
print(A().bar3(schema='schema3'))
"""
output:
    deco_arg:  deco_arg1
    schema:  schema1
    None
    ----------
    deco_arg:  deco_arg2
    schema:  schema2
    None
    ----------
    deco_arg:  default
    schema:  schema3
    None
"""
