from typing import Tuple
from enum import Enum

from pygame import Color
from pygame.font import Font
import pygame.draw


class FontCache:
    cache = {}

    @classmethod
    def get_font(cls, name, size, bold=False, italic=False):
        key = name, size, bold, italic
        if key not in cls.cache:
            cls.cache[key] = pygame.freetype.SysFont(name, size, bold, italic)
        return cls.cache[key]


class Span:
    def __init__(self, parent, text: str, *, font: Font = None, color: Color = None):
        if font:
            font.origin = True
        self.parent = parent
        self.text = text
        self.font = font or parent.font
        self.color = color or parent.color
        self.style = pygame.freetype.STYLE_NORMAL

    @property
    def adv_x(self):
        metrics = self.font.get_metrics(self.text, style=self.style)
        HORIZONTAL_ADVANCE_X = 4
        adv_x = sum(m[HORIZONTAL_ADVANCE_X] for m in metrics)
        return adv_x

    def get_rect(self):
        if self.text == "":
            return pygame.rect.Rect(0, 0, 0, 0)
        return self.font.get_rect(self.text, style=self.style)

    def render_to(self, surf, dest):
        if self.text == "":
            return 0
        rect = self.font.render_to(surf, dest, self.text, self.color, style=self.style)
        calcrect = self.get_rect()
        calcrect.x = dest[0] + calcrect.x
        calcrect.y = dest[1] - calcrect.y
        pygame.draw.rect(surf, "blue", rect, width=1)
        pygame.draw.rect(surf, "purple", calcrect, width=1)
        #pygame.draw.line(surf, "orange", (dest[0] + self.adv_x, rect.top), (dest[0] + self.adv_x, rect.bottom))
        #pygame.draw.line(surf, "green", (dest[0] + calcrect.w, rect.top), (dest[0] + calcrect.w, rect.bottom))
        return self.adv_x


class Direction(Enum):
    left = "left"
    center = "center"
    right = "right"


class Text:
    def __init__(
        self,
        *,
        font = None,
        size: Tuple[int, int] = None,  # size will just be "big enough the fix the text" by default
        justify: Direction = Direction.left,
        wrap: bool = False,
        parse_emoji_shortcodes: bool = False
    ):
        self.spans = []
        if font:
            font.origin = True
        self.font = font
        self.size = size
        self.justify = Direction(justify)
        self.wrap = wrap
        self.parse_emoji_shortcodes = parse_emoji_shortcodes

    def get_rect(self):
        if len(self.spans) == 0:
            return None
        rects = []
        x = 0
        for span in self.spans:
            rect = span.get_rect()
            rect.x = x
            rect.y = -rect.y
            rect.right = rect.x + span.adv_x
            rects.append(rect)
            x += span.adv_x
        out = rects[0].unionall(rects)
        return out

    def add_span(self, *args, **kwargs):
        self.spans.append(Span(self, *args, **kwargs))

    def render_to(self, surf, dest=(0, 0)):
        rect = self.get_rect()
        rect.y = dest[1] + rect.y
        pygame.draw.rect(surf, "#ff0000", rect)

        x, y = dest
        for span in self.spans:
            w = span.render_to(surf, (x, y))
            x += w


def test_digifont():
    Text("Hello, World").get_rect()
    Text("Hello, World").render()
    Text("Hello, World").render_to()
    Text("Hello, ", color="red") + Text("World", color="green")
    Text("Hello", color="red") + ", " + Text("World", color="green")
    "Hello, World" + Text("!", style="bold")
    my_texts = []
    my_texts.append(Text("Hello"))
    my_texts.append(", ")
    my_texts.append(Text("World"))
    text = sum(my_texts)
    text.render()
