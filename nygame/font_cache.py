from functools import lru_cache
from typing import Optional

from pygame.freetype import get_default_font, SysFont


font_cache = {}


@lru_cache(100)
def get_font(fontname: Optional[str] = None, size: int = 12, bold: bool = False, italic: bool = False):
    if fontname is None:
        fontname = get_default_font()
    return SysFont(fontname, size, bold=bold, italic=italic)
