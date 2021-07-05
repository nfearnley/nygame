import nygame
from nygame.input import powermate


class Game(nygame.Game):
    def __init__(self):
        super().__init__()
        powermate.init(self)
        self.brightness = 128
        self.rate = 10
        self.pulse_always = True
        powermate.set_pulse_always(self.pulse_always)
        powermate.set_pulse_rate(self.rate)
        powermate.set_brightness(self.brightness)

    async def loop(self, events):
        for event in events:
            if event.type == powermate.ROTATE:
                if event.rot < 0:
                    print(f"⟲ {event.rot:3}")
                else:
                    print(f"⟳ {event.rot:3}")
                if self.pulse_always:
                    self.rate += event.rot
                    self.rate = max(0x00, min(self.rate, 0x3F))
                    powermate.set_pulse_rate(self.rate)
                else:
                    self.brightness += event.rot
                    self.brightness = max(0x00, min(self.brightness, 0xFF))
                    powermate.set_brightness(self.brightness)
            elif event.type == powermate.BUTTONDOWN:
                print("↓")
                self.pulse_always = not self.pulse_always
                powermate.set_pulse_always(self.pulse_always)
            elif event.type == powermate.BUTTONUP:
                print("↑")


if __name__ == "__main__":
    Game().run()
