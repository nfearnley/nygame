from functools import reduce
import operator

from typing import Iterable, List, Sequence, Tuple, Union
from pygame.freetype import STYLE_UNDERLINE
from pygame import Rect, Surface, Color, freetype, SRCALPHA

from . import font_cache

_ColorValue = Union[Color, str, Tuple[int, int, int], List[int], int, Tuple[int, int, int, int]]


class DigiText:
    font = None
    size = 12
    color = "#000000"

    __slots__ = ("_spans")

    def __new__(cls, firstarg=None, *args, **kwargs):
        if isinstance(firstarg, cls):
            return firstarg
        if not isinstance(firstarg, str) and isinstance(firstarg, Iterable):
            return reduce(operator.add, (DigiText(t) for t in firstarg))

        instance = super().__new__(cls)
        instance._spans = None
        return instance

    def __init__(
        self, text: str = None, *, font: str = None, size: int = None, color: _ColorValue = None,
        bold: bool = False, italic: bool = False, underline: bool = False, strikethru: bool = False
    ):
        if self._spans is not None:
            return
        if font is None:
            font = self.font
        if size is None:
            size = self.size
        if color is None:
            color = self.color
        if text is not None:
            self._spans = (DigiSpan(text, font=font, size=size, color=color, bold=bold, italic=italic, underline=underline, strikethru=strikethru), )
        else:
            self._spans = tuple()

    def __str__(self):
        return "".join(str(span) for span in self._spans)

    def __add__(self, other):
        # Have to make sure both sides are a DigiText, since addition can be reversed
        if not isinstance(other, DigiText):
            other = DigiText(other)
        t = DigiText()
        t._spans = self._spans + other._spans
        return t

    def __radd__(self, other):
        if not isinstance(other, DigiText):
            other = DigiText(other)
        t = DigiText()
        t._spans = self._spans + other._spans
        return t

    def get_rect(self):
        y = 0
        h = 0
        w = 0
        for span in self._spans:
            srect = span.get_rect()
            charw = span.char_width
            y = max(y, srect.y)
            h = max(h, srect.h)
            w += charw
        return Rect(0, y, w, h)

    @property
    def char_width(self):
        return sum(s.char_width for s in self._spans)

    def render(self):
        rect = self.get_rect()
        surf = Surface(rect.size, flags = SRCALPHA)
        self.render_to(surf, (0, rect.y))
        return surf

    def render_to(self, surf: Surface, dest: Union[Tuple[int, int], Sequence[int], Rect]) -> Rect:
        if isinstance(dest, Rect):
            dest = dest.topleft
        x, y = dest
        for span in self._spans:
            span.render_to(surf, (x, y))
            x += span.char_width


class DigiSpan:
    __slots__ = ("text", "fontname", "size", "color", "bold", "italic", "underline", "strikethru", "rendered", "_char_width")
    _cached = {}

    def __new__(
        cls, text: str, *, font: str = None, size: int = None, color: _ColorValue = None,
        bold: bool = False, italic: bool = False, underline: bool = False, strikethru: bool = False
    ):
        key = (text, font, size, color, bold, italic, underline, strikethru)
        if key in cls._cached:
            return cls._cached[key]
        instance = super().__new__(cls)
        cls._cached[key] = instance
        instance.text = None
        return instance

    def __init__(
        self, text: str, *, font: str = None, size: int = None, color: _ColorValue = None,
        bold: bool = False, italic: bool = False, underline: bool = False, strikethru: bool = False
    ):
        if self.text is not None:
            return
        if underline and strikethru:
            raise ValueError("DigiText underline and strikethru are not mutually compatible")
        if font is None:
            raise ValueError("font must be set")
        if size is None:
            raise ValueError("size must be set")
        if color is None:
            raise ValueError("color must be set")
        self.text = text
        self.fontname = font
        self.size = size
        self.color = color
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.strikethru = strikethru
        self.rendered = None
        self._char_width = None

    @property
    def char_width(self):
        if self._char_width is None:
            metrics = self.font.get_metrics(self.text)
            self._char_width = 0
            self._char_width += sum(m[4] for m in metrics if m is not None)  # 4 = HORIZONTAL_ADVANCE_X
            self._char_width += sum(self.font.get_rect(self.text[i], style=self.style).w for i, m in enumerate(metrics) if m is None)
        return self._char_width

    def get_rect(self):
        return self.font.get_rect(self.text, style=self.style)

    def render(self) -> Tuple[Surface, Rect]:
        if not self.rendered:
            self.rendered = self.font.render(self.text, fgcolor=self.color, style=self.style)
        return self.rendered

    # Drop shadow prototype
    # =====================
    # def render(self) -> Tuple[Surface, Rect]:
    #     if not self.rendered:
    #         text_surf, rect = self.font.render(self.text, fgcolor=self.color, style=self.style)
    #         pa = PixelArray(text_surf.copy())
    #         pa.replace(Color("white"), Color("black"), 0.99)
    #         shadow = pa.make_surface()
    #         pa.close()
    #         w, h = text_surf.get_rect().size
    #         dsx, dsy = 8, 12
    #         w += dsx
    #         h += dsy
    #         out = Surface((w, h), flags=SRCALPHA)
    #         shadow.set_alpha(120)
    #         out.blit(shadow, (dsx,dsy))
    #         out.blit(text_surf, (0,0))
    #         self.rendered = out, rect
    #     return self.rendered

    def render_to(self, surf: Surface, dest: Union[Tuple[int, int], Sequence[int], Rect]) -> Rect:
        span_surf, rect = self.render()
        x, y = dest
        aligned_dest = (x + rect.x, y - rect.y)
        surf.blit(span_surf, aligned_dest)

    @property
    def font(self) -> freetype.Font:
        font = font_cache.get_font(self.fontname, self.size, self.bold, self.italic)
        font.origin = True
        font.underline_adjustment = self.underline_adjustment
        return font

    @property
    def style(self) -> int:
        style = self.font.style
        if self.underline or self.strikethru:
            style |= STYLE_UNDERLINE
        return style

    @property
    def underline_adjustment(self) -> float:
        underline_adjustment = 0
        if self.strikethru:
            underline_adjustment = -0.5
        return underline_adjustment

    def __str__(self):
        return self.text


def init():
    global dummyfont
    freetype.init()
    DigiText.font = freetype.get_default_font()
