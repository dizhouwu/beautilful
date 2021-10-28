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
