from pathlib import Path
import json

import pygame

emojisets = {}


class EmojiSet():
    def __init__(self, name, emoji_size, emoji_map, sheet):
        self.name = name
        self.emoji_size = emoji_size
        self.emoji_map = emoji_map
        sheet_size = sheet.get_size()
        self.emojis_per_line = sheet_size[0] / emoji_size[0]
        self.sheet = sheet

    def __str__(self):
        return f"EmojiSet({self.name!r})"

    def __getitem__(self, s):
        # TODO: Return actual image
        index = self.emoji_map[s]
        rect = self.index2rect(index)
        emoji_surf = self.sheet.subsurface(rect)
        return emoji_surf

    def __contains__(self, s):
        return s in self.emoji_map

    def index2rect(self, index):
        y, x = divmod(index, self.emojis_per_line)
        w, h = self.emoji_size
        x *= w
        y *= h
        rect = pygame.Rect(x, y, w, h)
        return rect

    @classmethod
    def from_json(cls, j, sheet):
        name = j["name"]
        emoji_size = j["emoji_width"], j["emoji_height"]
        emoji_map = {e: i for i, e in enumerate(j["emojis"])}
        return cls(name, emoji_size, emoji_map, sheet)

    @classmethod
    def load(cls, path):
        path = Path(path)
        with path.open("r", encoding="utf-8") as f:
            j = json.load(f)
        sheet_path = path.with_suffix(".png")
        with sheet_path.open("rb") as f:
            sheet = pygame.image.load(f)
        return cls.from_json(j, sheet)


def load_emojiset(folder_path):
    emojiset = EmojiSet.load(folder_path)
    emojisets[emojiset.name] = emojiset
    return emojiset


"""
{
    "name": "twemoji"
    "emoji_width": 72,
    "emoji_height": 72,
    "emojis": [
        "\U000000A9",
        "\U000000AE",
        ...
    ]
}
"""
