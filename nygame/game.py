import pygame
from . import font_cache, time
from .music import music


class Game:
    def __init__(self, *, size=(800, 600), fps=30, bgcolor="black", showfps=False):
        pygame.init()
        self.clock = time.Clock()
        self.surface = pygame.display.set_mode(size, pygame.DOUBLEBUF)
        self.size = self.surface.get_size()
        self.running = True
        self.fps = fps
        self.showfps = showfps
        self.fps_font = font_cache.get_font("Consolas", 24)
        self.bgcolor = bgcolor
        self.MUSIC_END_EVENT = pygame.event.custom_type()
        pygame.mixer.music.set_endevent(self.MUSIC_END_EVENT)

    def run(self):
        while self.running:
            self.surface.fill(self.bgcolor)
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False
                elif e.type == self.MUSIC_END_EVENT:
                    music.on_end(e)
            self.loop(events)
            if self.showfps:
                self.draw_fps(self.clock.get_fps())
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
