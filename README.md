# nygame

nygame is a wrapper around the pygame library. It's goal is to provide and more pythonic and easy to use experience.

## Usage

A basic game structure can be started like this:

```python
import nygame
import pygame

class Game(nygame.Game):
    def __init__(self):
        super().__init__(size=(300, 200))
        pass

    def loop(self, events):
        pygame.draw.circle(self.surface, "red", (150, 100), 50)

if __name__ == "__main__":
    Game().run()
```

After `Game.__init__()` is called, a new game. A window of 300x200 will be created to host the game. Further options are available in `super().__init__()`'s doc string.

`Game.loop()` will be called every frame, with the most recent events in the `events` argument. The screen will automatically be cleared before every frame and can be drawn to by using `self.surface`.

## Demos

[EmojiApp](demos) - A demo app that lets you browse through emoji

## Development

### Deployment

???