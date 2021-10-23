from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Optional

if TYPE_CHECKING:
    from nygame.game import Game

from enum import Enum
from functools import wraps

import pygame
from pygame.event import Event
from pygame.mixer import Sound
from pygame.mixer import music as pgmusic

from nygame.utils import clamp


class Status(Enum):
    initialized = "initialized"
    stopped = "stopped"
    playing = "playing"
    paused = "paused"


def require_status(*st: Status) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def wrapper(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def wrapped(self: Music, *args: Any, **kwargs: Any) -> Any:
            if self.status not in st:
                return
            return fn(self, *args, *kwargs)
        return wrapped
    return wrapper


class Music:
    def __init__(self):
        self.MUSIC_END_EVENT: Optional[int] = None
        self._initialized: bool = False
        self.length: float = 0
        self.offset: float = 0
        self.status: Status = Status.initialized

    def load(self, filename: str) -> None:
        self.length = Sound(filename).get_length()
        self.offset = 0
        pgmusic.load(filename)
        self.status = Status.stopped

    def play(self, filename: Optional[str] = None) -> None:
        if filename:
            self.load(filename)
        if self.status == Status.stopped:
            pgmusic.play()
            self.status = Status.playing
        elif self.status == Status.paused:
            pgmusic.unpause()
            self.status = Status.playing

    @require_status(Status.playing, Status.paused)
    def stop(self) -> None:
        pgmusic.stop()
        self.on_end()

    def on_end(self) -> None:
        self.offset = (pgmusic.get_pos() / 1000)
        self.status = Status.stopped

    @require_status(Status.playing)
    def pause(self) -> None:
        pgmusic.pause()
        self.status = Status.paused

    @require_status(Status.playing, Status.paused, Status.stopped)
    def playpause(self) -> None:
        if self.status == Status.playing:
            self.pause()
        else:
            self.play()

    @property
    def elapsed(self) -> float:
        # If we ff or rw, it doesn't change the get_pos(), so gotta store an offset
        return max(0, pgmusic.get_pos() / 1000 - self.offset)

    @elapsed.setter
    @require_status(Status.playing, Status.paused)
    def elapsed(self, new_pos: float) -> None:
        new_pos = clamp(0, new_pos, self.length)
        pgmusic.set_pos(new_pos)
        self.offset = (pgmusic.get_pos() / 1000) - new_pos

    @property
    def remaining(self) -> float:
        return self.length - self.elapsed

    @remaining.setter
    def remaining(self, new_pos: float) -> None:
        self.elapsed = self.length - new_pos

    @property
    def volume(self) -> float:
        return pgmusic.get_volume() * 128

    @volume.setter
    def volume(self, value: float) -> None:
        pgmusic.set_volume(value / 128)

    @property
    def paused(self) -> bool:
        return self.status == Status.paused

    @paused.setter
    def paused(self, value: bool) -> None:
        if value:
            self.pause()
        else:
            self.play()

    @property
    def playing(self) -> bool:
        return self.status == Status.playing

    @playing.setter
    def playing(self, value: bool) -> None:
        if value:
            self.play()
        else:
            self.pause()

    def handle_event(self, e: Event):
        if e.type == self.MUSIC_END_EVENT:
            self.on_end()

    # Module init
    def init(self, game: Game):
        if self._initialized:
            return
        self.MUSIC_END_EVENT = pygame.event.custom_type()
        pgmusic.set_endevent(self.MUSIC_END_EVENT)
        game.register_eventhandler(self.handle_event)
        self._initialized = True


music = Music()
