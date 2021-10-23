from typing import Any, Callable, Optional, TypeVar, Union, cast, overload

from functools import wraps
import cProfile
import pstats

FN = TypeVar("FN", bound=Callable[..., Any])


@overload
def perf() -> Callable[[FN], FN]:
    ...


@overload
def perf(fn: FN, *, sort: Optional[str]) -> FN:
    ...


def perf(fn: Optional[FN] = None, *, sort: Optional[str] = None) -> Union[Callable[[FN], FN], FN]:
    def wrapper(fn: FN) -> FN:
        @wraps(fn)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            pr = cProfile.Profile(builtins=False)
            pr.enable()
            results = fn(*args, **kwargs)
            pr.disable
            stats = pstats.Stats(pr)
            if sort:
                stats.sort_stats(sort)
            stats.print_stats()
            return results
        return cast(FN, wrapped)
    if fn is not None:
        if not callable(fn):
            raise ValueError("BeepBoop")
        return wrapper(fn)
    return wrapper
