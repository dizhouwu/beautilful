import cProfile
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"Func {func.__qualname__} Elapsed time: {elapsed_time:0.4f} seconds")
        return value

    return wrapper_timer

def profileit(func):
    @functools.wraps(func)  
    def wrapper(*args, **kwargs):
        datafn = func.__qualname__ + ".profile" 
        prof = cProfile.Profile()
        retval = prof.runcall(func, *args, **kwargs)
        prof.dump_stats(datafn)
        return retval

    return wrapper
