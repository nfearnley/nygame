from nygame.common import Coord
import pygame
from . import font_cache, time
from .music import music


class Game:
    def __init__(self, *, size=(800, 600), scale=1, fps=30, showfps=False, bgcolor="black"):
        pygame.init()
        pygame.colordict.THECOLORS["clear"] = (0, 0, 0, 0)

        self.size = size
        self.scale = scale
        self.fps = fps
        self.showfps = showfps
        self.bgcolor = bgcolor

        self._currsize = None
        self._currscale = None
        self.clock = time.Clock()
        self.running = True
        self.fps_font = font_cache.get_font("Consolas", 24)

        self.eventhandlers = []
        self.register_eventhandler(self.quit_handler)
        self.register_eventhandler(self.mouse_handler)

        self.reset_display()
        music.init(self)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, newscale):
        if newscale is None:
            newscale = 1
        if not isinstance(newscale, int) or newscale < 1:
            raise ValueError(f"Invalid scale: {newscale}")
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
    def mouse_pos(self, newpos):
        x, y = newpos
        newpos = x * self.scale, y * self.scale
        pygame.mouse.set_pos(newpos)

    def run(self):
        while self.running:
            if self.bgcolor is not None:
                self.surface.fill(self.bgcolor)
            events = pygame.event.get()
            for e in events:
                self.handle_event(e)
            self.loop(events)
            if self.showfps:
                self.draw_fps(self.clock.get_fps())
            if self.out_surface is not None:
                pygame.transform.scale(self.surface, self.out_surface.get_size(), self.out_surface)
            pygame.display.flip()
            self.clock.tick_busy_loop(self.fps)

    def draw_fps(self, fps):
        fps = format(fps, ".0f")
        font = self.fps_font
        font.pad = True
        font.render_to(self.surface, (1, 2), fps, fgcolor="black")
        font.render_to(self.surface, (0, 0), fps, fgcolor="green")

    def loop(self):
        # Game code runs here
        raise NotImplementedError

    def register_eventhandler(self, handler):
        self.eventhandlers.append(handler)

    def handle_event(self, e):
        for eventhandler in self.eventhandlers:
            eventhandler(e)

    def mouse_handler(self, e):
        if e.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            e.pos = tuple(Coord(e.pos) / self.scale)

    def quit_handler(self, e):
        if e.type == pygame.QUIT:
            self.running = False
