from pathlib import Path
import json


emoji_sets = {}


class EmojiSet():
    def __init__(self, emoji_size, emoji_map, sheet):
        self.emoji_size = emoji_size
        self.emoji_map = emoji_map
        self.sheet = sheet

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
        sheet = sheet_path.read_bytes()
        return cls.from_json(j, sheet)


def load_emoji_set(folder_path):
    emoji_set = EmojiSet.load(folder_path)
    emoji_sets[emoji_set.name] = emoji_set


"""
{
    "name": "twemoji"
    "emoji_width": 72,
    "emoji_height": 72,
    "emojis": [
        "\U000000A9",
        "\U000000EA",
        ...
    ]
}
"""
