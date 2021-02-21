from functools import wraps
import cProfile
import pstats


def perf(fn=None, *, sort=None):
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            pr = cProfile.Profile(builtins=False)
            pr.enable()
            fn(*args, **kwargs)
            pr.disable
            stats = pstats.Stats(pr)
            if sort:
                stats.sort_stats(sort)
            stats.print_stats()
        return wrapped
    if fn is not None:
        if not callable(fn):
            raise ValueError("BeepBoop")
        return wrapper(fn)
    return wrapper
