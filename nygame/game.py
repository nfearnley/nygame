import pygame
from . import font_cache, time
from .music import music


class Game:
    def __init__(self, *, size=(800, 600), scale=1, fps=30, bgcolor="black", showfps=False):
        pygame.init()
        self.clock = time.Clock()
        self._currsize = None
        self._currscale = None
        self.size = size
        self.scale = scale
        self.reset_display()
        self.running = True
        self.fps = fps
        self.showfps = showfps
        self.fps_font = font_cache.get_font("Consolas", 24)
        self.bgcolor = bgcolor
        music.init()

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

    def run(self):
        while self.running:
            if self.bgcolor is not None:
                self.surface.fill(self.bgcolor)
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False
                elif e.type == music.MUSIC_END_EVENT:
                    music.on_end(e)
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
