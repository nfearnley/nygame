from . import _quietload

from pygame import Rect, Color, joystick
from . import time, digifont, emoji, data
from .music import music
from .game import Game
from .digifont import DigiText
from .perf import perf
from .constants import *

del _quietload

__all__ = ["Rect", "Color", "joystick", "time", "digifont", "emoji", "data", "music", "Game", "DigiText", "perf"]
