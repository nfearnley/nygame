import inspect
import asyncio
from typing import Callable, Union, Any

import pygame
import pygame.event
from pygame.event import Event
import pygame.surface
from pygame.color import Color

from nygame import font_cache, time
from nygame.music import music
from nygame.common import Coord


ColorInput = Union[str, tuple[int, int, int], list[int], int, tuple[int, int, int, int]]

PreloopHandler = Callable[[], None]
EventHandler = Callable[[Event], None]


async def wrap_async(value: Any):
    if inspect.isawaitable(value):
        return await value
    return value


class Game:
    def __init__(self, *, size: tuple[int, int] = (800, 600), scale: int = 1, fps: int = 30, showfps: bool = False, bgcolor: ColorInput = "black"):
        pygame.init()
        pygame.colordict.THECOLORS["clear"] = (0, 0, 0, 0)

        self.size = size
        self.scale = scale
        self.fps = fps
        self.showfps = showfps
        self.bgcolor = Color(bgcolor)

        self._currsize = None
        self._currscale = None
        self.clock = time.Clock()
        self.running = True
        self.fps_font = font_cache.get_font("Consolas", 24)

        self.preloop_handlers: list[PreloopHandler] = []
        self.eventhandlers: list[EventHandler] = []
        self.register_eventhandler(self.quit_handler)
        self.register_eventhandler(self.mouse_handler)

        self.reset_display()
        music.init(self)

    @property
    def scale(self) -> int:
        return self._scale

    @scale.setter
    def scale(self, newscale: int) -> None:
        if newscale is None:
            newscale = 1
        self._scale = newscale

    def reset_display(self):
        if (self._currscale, self._currsize) == (self.scale, self.size):
            return
        (self._currscale, self._currsize) = (self.scale, self.size)
        if self.scale == 1:
            self.out_surface = None
            self.surface = pygame.display.set_mode(self.size, pygame.DOUBLEBUF)
        else:
            w, h = self.size
            scaled_size = w * self.scale, h * self.scale
            self.out_surface = pygame.display.set_mode(scaled_size, pygame.DOUBLEBUF)
            self.surface = pygame.Surface(self.size)

    @property
    def mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        return int(x / self.scale), int(y / self.scale)

    @mouse_pos.setter
    def mouse_pos(self, newpos: tuple[int, int]):
        x, y = newpos
        newpos = x * self.scale, y * self.scale
        pygame.mouse.set_pos(newpos)

    def run(self):
        asyncio.run(self.run_async())

    async def run_async(self):
        while self.running:
            if self.bgcolor is not None:
                self.surface.fill(self.bgcolor)
            for handler in self.preloop_handlers:
                handler()
            events = pygame.event.get()
            for e in events:
                await self.handle_event(e)
            await wrap_async(self.loop(events))
            if self.showfps:
                await wrap_async(self.draw_fps(self.clock.get_fps()))
            if self.out_surface is not None:
                pygame.transform.scale(self.surface, self.out_surface.get_size(), self.out_surface)
            pygame.display.flip()
            self.clock.tick_busy_loop(self.fps)

    async def draw_fps(self, fps: float):
        fps_text = format(fps, ".0f")
        font = self.fps_font
        font.pad = True
        font.render_to(self.surface, (1, 2), fps_text, fgcolor="black")
        font.render_to(self.surface, (0, 0), fps_text, fgcolor="green")

    async def loop(self, events: list[Event]) -> None:
        # Game code runs here
        raise NotImplementedError

    def register_preloop_handler(self, handler: PreloopHandler):
        self.preloop_handlers.append(handler)

    def register_eventhandler(self, handler: EventHandler):
        self.eventhandlers.append(handler)

    async def handle_event(self, e: Event):
        for eventhandler in self.eventhandlers:
            await wrap_async(eventhandler(e))

    # e must by Any before e.pos is not settable
    def mouse_handler(self, e: Any):
        if e.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            e.pos = tuple(Coord(*e.pos) / self.scale)

    def quit_handler(self, e: Event):
        if e.type == pygame.QUIT:
            self.running = False
