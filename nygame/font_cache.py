from functools import lru_cache

from pygame import freetype

font_cache = {}


@lru_cache(100)
def get_font(fontname=None, size=12, bold=False, italic=False):
    if fontname is None:
        fontname = freetype.get_default_font()
    return freetype.SysFont(fontname, size, bold=bold, italic=italic)
