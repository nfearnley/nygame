from nygame import utils
import importlib.resources as pkg_resources

from emoji import UNICODE_EMOJI_ENGLISH

import nygame
import nygame.data.emojisets
from nygame import SDL_EventType
from nygame import DigiText as T
from nygame.emoji import load_emojiset


class Game(nygame.Game):
    def __init__(self):
        super().__init__(fps=120, size=(903, 903), showfps=True)
        T.font = "Arial"
        T.color = "yellow"
        T.size = 24
        with pkg_resources.path(nygame.data.emojisets, "twemoji.json") as path:
            self.eset = load_emojiset(path)
        self.codes = [e for e in UNICODE_EMOJI_ENGLISH.keys() if e in self.eset]
        self.index = 0
        self.hovered = None

    def loop(self, events):
        for event in events:
            if event.type == SDL_EventType.MOUSEWHEEL.value:
                self.index = utils.clamp(0, self.index - event.y * 10, len(self.codes)-1)
            elif event.type == SDL_EventType.MOUSEMOTION.value:
                self.hovered = pos2index(event.pos)
        for n, i in enumerate(range(self.index, min(self.index + 100, len(self.codes)-1))):
            code = self.codes[i]
            emoji_surf = self.eset[code]
            emoji_rect = emoji_surf.get_rect()
            y, x = divmod(n, 10)
            emoji_rect.x = 10 + x * 90
            emoji_rect.y = 10 + y * 90
            self.surface.blit(emoji_surf, emoji_rect)
        if self.hovered is not None:
            n, pos = self.hovered
            if self.index + n < len(self.codes):
                code = self.codes[self.index + n]
                emoji_name = T(UNICODE_EMOJI_ENGLISH[code].strip(":"))
                text_rect = emoji_name.get_rect()
                text_rect.midbottom = pos
                shadow = T(UNICODE_EMOJI_ENGLISH[code].strip(":"), color="black")
                shadow.render_to(self.surface, text_rect)
                shadow.render_to(self.surface, text_rect.move(1, 0))
                shadow.render_to(self.surface, text_rect.move(-1, 0))
                shadow.render_to(self.surface, text_rect.move(0, 1))
                shadow.render_to(self.surface, text_rect.move(0, -1))
                emoji_name.render_to(self.surface, text_rect)


def pos2index(pos):
    x, y = pos
    x -= 10
    y -= 10
    x_index, x_offset = divmod(x, 90)
    y_index, y_offset = divmod(y, 90)
    if x_offset > 72 or y_offset > 72:
        return None
    index = y_index * 10 + x_index
    return index, pos


if __name__ == "__main__":
    Game().run()
