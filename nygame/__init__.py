import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
del os

from . import time, digifont, emoji, data
from .music import music
from .game import Game
from .digifont import DigiText
from .perf import perf

__all__ = ["time", "digifont", "emoji", "data", "music", "Game", "DigiText", "perf"]
