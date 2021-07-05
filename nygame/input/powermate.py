import pygame

try:
    import usb.core
    import usb.util
except ImportError:
    pass

vid = 0x077d
pid = 0x0410


def sign(val):
    return -1 if val < 0 else 1


class Powermate:
    ROTATE = pygame.event.custom_type()
    BUTTONDOWN = pygame.event.custom_type()
    BUTTONUP = pygame.event.custom_type()

    def __init__(self):
        self.initialized = False
        self.device = None
        self._last_btn = 0

    def init(self, game):
        if not self.initialized:
            self.device: usb.core.Device = usb.core.find(idVendor=vid, idProduct=pid)
            if self.device is None:
                return
            self.initialized = True
            game.register_preloop_handler(self._poll)

    def _read_hid(self):
        try:
            return self.device.read(0x81, 6, 10)
        except usb.core.USBError:
            return None

    def _poll(self):
        raw_events = []
        while data := self._read_hid():
            btn: int
            rot: int
            btn, rot, _, _, _, _ = data
            if rot == 0xFF:
                rot = -1
            if rot != 0:
                raw_events.append(pygame.event.Event(self.ROTATE, rot=rot))
            if self._last_btn != btn:
                self._last_btn = btn
                raw_events.append(pygame.event.Event(self.BUTTONUP if btn == 0 else self.BUTTONDOWN))

        events = []
        if raw_events:
            events = raw_events[:1]
            for new_event in raw_events[1:]:
                # get the previous event
                last_event = events[-1]
                if new_event.type in (self.BUTTONDOWN, self.BUTTONUP) and new_event.type == last_event.type:
                    # skip duplicate button presses
                    continue
                elif new_event.type == self.ROTATE and new_event.type == last_event.type and sign(last_event.rot) == sign(new_event.rot):
                    # collapse repeated rotations
                    events.pop()
                    events.append(pygame.event.Event(self.ROTATE, rot=last_event.rot + new_event.rot))
                else:
                    # add this event to collapsed events, and move to the next event
                    events.append(new_event)

        for event in events:
            pygame.event.post(event)

    def set_brightness(self, brightness):
        try:
            self.device.ctrl_transfer(bmRequestType=usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_INTERFACE, bRequest=1, wValue=1, wIndex=brightness)
        except usb.core.USBError:
            pass

    def set_pulse_during_sleep(self, pulse_during_sleep):
        try:
            self.device.ctrl_transfer(bmRequestType=usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_INTERFACE, bRequest=1, wValue=2, wIndex=1 if pulse_during_sleep else 0)
        except usb.core.USBError:
            pass

    def set_pulse_always(self, pulse_always):
        try:
            self.device.ctrl_transfer(bmRequestType=usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_INTERFACE, bRequest=1, wValue=3, wIndex=1 if pulse_always else 0)
        except usb.core.USBError:
            pass

    def _set_pulse_rate_raw(self, raw_pulse_rate):
        print(format(raw_pulse_rate, "04x"))
        try:
            self.device.ctrl_transfer(bmRequestType=usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_INTERFACE, bRequest=1, wValue=4, wIndex=raw_pulse_rate)
        except usb.core.USBError:
            pass

    def set_pulse_rate(self, pulse_rate):
        if 0x00 <= pulse_rate <= 0x0E:
            raw_pulse_rate = (0x0F - pulse_rate) << 8
        elif 0x0F <= pulse_rate <= 0x3F:
            raw_pulse_rate = (pulse_rate - 0x0D) << 8 | 0x02
        else:
            raise ValueError
        self._set_pulse_rate_raw(raw_pulse_rate)


powermate = Powermate()


def demo():
    count = 0
    oldbtn = 0
    while True:
        data = powermate.read_hid()
        if not data:
            continue
        btn, rot, c, d, e, f = data

        events = []

        if rot == 0xff:
            events.append("⟲")
        elif rot == 0x01:
            events.append("⟳")

        if btn != oldbtn:
            if btn == 0x00:
                events.append("↑")
            elif btn == 0x01:
                events.append("↓")
            oldbtn = btn

        events_str = " ".join(events)
        print(f"{count:>4} {btn:02x} {rot:02x} {events_str}")
        count += 1


# Pulse rates are weird
# raw_pulse_rate=[
# 0x0f00, # 32.5s     0x00 | 0x0F-0x00 = 0x0F
# 0x0e00, #           0x01 | 0x0F-0x01 = 0x0E
# 0x0d00, #           0x02 | 0x0F-0x02 = 0x0D
# 0x0c00, #           0x03 | 0x0F-0x03 = 0x0C
# 0x0b00, #           0x04 | 0x0F-0x04 = 0x0B
# 0x0a00, #           0x05 | 0x0F-0x05 = 0x0A
# 0x0900, #           0x06 | 0x0F-0x06 = 0x09
# 0x0800, # 16s       0x07 | 0x0F-0x07 = 0x08
# 0x0700, #           0x08 | 0x0F-0x08 = 0x07
# 0x0600, # 13s       0x09 | 0x0F-0x09 = 0x06
# 0x0500, #           0x0A | 0x0F-0x0A = 0x05
# 0x0400, #           0x0B | 0x0F-0x0B = 0x04
# 0x0300, # 6.5s      0x0C | 0x0F-0x0C = 0x03
# 0x0200, # 4.3s      0x0D | 0x0F-0x0D = 0x02
# 0x0100, # 2.3s      0x0E | 0x0F-0x0E = 0x01
# 0x0202, # 1.95s     0x0F | 0x0F-0x0D = 0x02
# 0x0302, # 1.35s     0x10 | 0x10-0x0D = 0x03
# 0x0402, # 0.975s    0x11
# 0x0502, # 0.77s     0x12
# 0x0602, #           0x13
# 0x0702, #           0x14
# 0x0802, # 0.46      0x15
# 0x0902, #           0x16
# 0x0A02, #           0x17
# 0x0B02, #           0x18
# 0x0C02, #           0x19
# 0x0D02, #           0x1A
# 0x0E02, #           0x1B
# 0x0F02, #           0x1C
# 0x1002, #           0x1D
# 0x1102, #           0x1E
# 0x1202, #           0x1F
# 0x1302, #           0x20
# 0x1402, #           0x21
# 0x1502, #           0x22
# 0x1602, #           0x23
# 0x1702, #           0x24
# 0x1802, #           0x25
# 0x1902, #           0x26
# 0x1A02, #           0x27
# 0x1B02, #           0x28
# 0x1C02, #           0x29
# 0x1D02, #           0x2A
# 0x1E02, #           0x2B
# 0x1F02, #           0x2C
# 0x2002, #           0x2D
# 0x2102, #           0x2E
# 0x2202, #           0x2F
# 0x2302, #           0x30
# 0x2402, #           0x31
# 0x2502, #           0x32
# 0x2602, #           0x33
# 0x2702, #           0x34
# 0x2802, #           0x35
# 0x2902, #           0x36
# 0x2A02, #           0x37
# 0x2B02, #           0x38
# 0x2C02, #           0x39
# 0x2D02, #           0x3A
# 0x2E02, #           0x3B
# 0x2F02, #           0x3C
# 0x3002  #           0x3D
# ]
