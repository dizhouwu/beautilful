import asyncio
import functools

def async_run(coro):
    """async wrapper for Python 3.6"""

    @functools.wraps(coro)
    def run_with_event_loop(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))

    return run_with_event_loop
