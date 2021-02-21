from enum import Enum
from functools import wraps

from pygame.mixer import Sound
from pygame.mixer import music as pgmusic

from .utils import clamp


class Status(Enum):
    initialized = "initialized"
    stopped = "stopped"
    playing = "playing"
    paused = "paused"


def require_status(*st):
    def wrapper(fn):
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            if self.status not in st:
                return
            return fn(self, *args, *kwargs)
        return wrapped
    return wrapper


class Music:
    def __init__(self):
        self.length = 0
        self.offset = 0
        self.status = Status.initialized

    def load(self, filename):
        self.length = Sound(filename).get_length()
        self.offset = 0
        pgmusic.load(filename)
        self.status = Status.stopped

    def play(self, filename=None):
        if filename:
            self.load(filename)
        if self.status == Status.stopped:
            pgmusic.play()
            self.status = Status.playing
        elif self.status == Status.paused:
            pgmusic.unpause()
            self.status = Status.playing

    @require_status(Status.playing, Status.paused)
    def stop(self):
        pgmusic.stop()
        self.offset = 0
        self.status = Status.stopped

    @require_status(Status.playing)
    def pause(self):
        pgmusic.pause()
        self.status = Status.paused

    @require_status(Status.playing, Status.paused, Status.stopped)
    def playpause(self):
        if self.status == Status.playing:
            self.pause()
        else:
            self.play()

    @property
    def elapsed(self):
        # If we ff or rw, it doesn't change the get_pos(), so gotta store an offset
        return max(0, pgmusic.get_pos() / 1000 - self.offset)

    @elapsed.setter
    @require_status(Status.playing, Status.paused)
    def elapsed(self, new_pos):
        new_pos = clamp(0, new_pos, self.length)
        pgmusic.set_pos(new_pos)
        self.offset = (pgmusic.get_pos() / 1000) - new_pos

    @property
    def remaining(self):
        return self.length - self.elapsed

    @remaining.setter
    def remaining(self, new_pos):
        self.elapsed = self.length - new_pos

    @property
    def volume(self):
        return pgmusic.get_volume()

    @volume.setter
    def volume(self, value):
        return pgmusic.set_volume(value)


music = Music()
