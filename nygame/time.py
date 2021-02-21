"""nygame module for monitoring time
"""

import time

from pygame.time import set_timer

__all__ = ["get_ticks", "wait", "delay", "set_timer", "Clock"]

_start_time = None


def get_ticks() -> int:
    """get the time in nanoseconds

    Return the number of nanoseconds since get_ticks() was first called.

    Returns
    -------
        Time since get_ticks() was first called in nanoseconds.
    """
    return time.perf_counter_ns()


def get_ticks_sec() -> int:
    """get the time in seconds

    Return the number of seconds since get_ticks() was first called.

    Returns
    -------
        Time since get_ticks() was first called in nanoseconds.
    """
    return get_ticks() / 10**9


def wait(ticks: int) -> int:
    """pause the program for an amount of time

    Will pause for a given number of nanoseconds.
    This function sleeps the process to share the processor with other programs.
    A program that waits for even a few nanoseconds will consume very little processor time.
    It is slightly less accurate than the nygame.time.delay() function.

    Parameters
    ----------
    ticks
        The amount of time to pause in nanoseconds.

    Returns
    -------
        The actual number of nanoseconds used.
    """
    if ticks <= 0:
        return 0
    start = get_ticks()
    time.sleep(ticks / 10**9)
    return get_ticks() - start


def wait_secs(ticks: int) -> int:
    """pause the program for an amount of time

    Will pause for a given number of seconds.
    This function sleeps the process to share the processor with other programs.
    A program that waits for even a few seconds will consume very little processor time.
    It is slightly less accurate than the nygame.time.delay() function.

    Parameters
    ----------
    ticks
        The amount of time to pause in seconds.

    Returns
    -------
        The actual number of seconds used.
    """
    return wait(ticks * 10**9) / 10**9


def delay(ticks: int) -> int:
    """pause the program for an amount of time

    Will pause for a given number of nanoseconds.
    This function will use the processor (rather than sleeping) in order to make the delay more accurate than nygame.time.wait().

    Parameters
    ----------
    ticks
        The amount of time to pause in nanoseconds.

    Returns
    -------
        The actual number of nanoseconds used.
    """
    start = time.perf_counter_ns()
    ticks -= 26000  # arbitrary offset to make up for poor timer precision
    if ticks <= 0:
        return 0
    end = start + ticks
    while time.perf_counter_ns() < end:
        pass
    return time.perf_counter_ns() - start


def delay_secs(ticks: int) -> int:
    """pause the program for an amount of time

    Will pause for a given number of seconds.
    This function will use the processor (rather than sleeping) in order to make the delay more accurate than nygame.time.wait().

    Parameters
    ----------
    ticks
        The amount of time to pause in seconds.

    Returns
    -------
        The actual number of seconds used.
    """
    return delay(ticks * 10**9) / 10**9


class Clock:
    """create an object to help track time

    Creates a new Clock object that can be used to track an amount of time.
    The clock also provides several functions to help control a game's framerate.
    """
    __slots__ = ["_fps_tick", "_timepassed", "_rawpassed", "_last_tick", "_fps", "_fps_count"]

    def __init__(self):
        self._timepassed = 0
        self._rawpassed = 0
        self._last_tick = get_ticks()
        self._fps_tick = None
        self._fps = 0
        self._fps_count = 0

    def _tick(self, framerate=0, *, use_accurate_delay=False):
        if (framerate):
            ns_per_frame = 10**9 / framerate
            self._rawpassed = get_ticks() - self._last_tick
            ticks_delay = ns_per_frame - self._rawpassed
            if use_accurate_delay:
                delay(ticks_delay)
            else:
                wait(ticks_delay)
        nowtime = get_ticks()

        self._timepassed = nowtime - self._last_tick
        self._last_tick = nowtime
        if not framerate:
            self._rawpassed = self._timepassed

        self._fps_count += 1
        if self._fps_tick is None:
            self._fps_tick = nowtime
        if self._fps_count == 20:
            self._fps = 20 / ((nowtime - self._fps_tick) / 10**9)
            self._fps_count = 0
            self._fps_tick = nowtime

        return self._timepassed

    def tick(self, framerate: float = 0) -> int:
        """update the clock

        This method should be called once per frame. It will compute how many nanoseconds have passed since the previous call.

        If you pass the optional framerate argument the function will delay to keep the game running slower than the given ticks per second.
        This can be used to help limit the runtime speed of a game.
        By calling Clock.tick(40) once per frame, the program will never run at more than 40 frames per second.

        Note that this function uses nygame.time.wait() which is not accurate on every platform, but does not use much CPU.
        Use Clock.tick_busy_loop() if you want an accurate timer, and don't mind chewing CPU.

        Parameters
        ----------
        framerate : optional
            Target framerate used to limit the runtime speed of a game.

        Returns
        -------
            How many nanoseconds have passed since the previous call.
        """
        return self._tick(framerate, use_accurate_delay=False)

    def tick_busy_loop(self, framerate: float = 0) -> int:
        """update the clock

        This method should be called once per frame. It will compute how many nanoseconds have passed since the previous call.

        If you pass the optional framerate argument the function will delay to keep the game running slower than the given ticks per second.
        This can be used to help limit the runtime speed of a game.
        By calling Clock.tick_busy_loop(40) once per frame, the program will never run at more than 40 frames per second.

        Note that this function uses nygame.time.delay(), which uses lots of CPU in a busy loop to make sure that timing is more accurate.
        Use Clock.tick() if you want a more efficient timer, and don't mind reduced accuracy.

        Parameters
        ----------
        framerate : optional
            Target framerate used to limit the runtime speed of a game.

        Returns
        -------
            How many nanoseconds have passed since the previous call.
        """
        return self._tick(framerate, use_accurate_delay=True)

    def get_time(self) -> int:
        """time used in the previous tick

        The number of nanoseconds that passed between the previous two calls to Clock.tick().

        Returns
        -------
            The time used in the previous tick in nanoseconds.
        """
        return self._timepassed

    def get_time_secs(self) -> float:
        """time used in the previous tick

        The number of seconds that passed between the previous two calls to Clock.tick().

        Returns
        -------
            The time used in the previous tick in seconds.
        """
        return self._timepassed / 10**9

    def get_rawtime(self) -> int:
        """actual time used in the previous tick

        Similar to Clock.get_time(), but does not include any time used while Clock.tick() was delaying to limit the framerate.

        Returns
        -------
            The actual time used in the previous tick in nanoseconds.
        """
        return self._rawpassed

    def get_rawtime_secs(self) -> int:
        """actual time used in the previous tick

        Similar to Clock.get_time(), but does not include any time used while Clock.tick() was delaying to limit the framerate.

        Returns
        -------
            The actual time used in the previous tick in nanoseconds.
        """
        return self._rawpassed

    def get_fps(self) -> float:
        """compute the clock framerate

        Compute your game's framerate (in frames per second). It is computed by averaging the last ten calls to Clock.tick().

        Returns
        -------
            The computed clock framerate in frames per second.
        """
        return self._fps

    def __str__(self):
        return f"<Clock(fps={self._fps:.2f})>"

    def __repr__(self):
        return str(self)
