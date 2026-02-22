import threading
import time


try:
    from rpi_ws281x import PixelStrip, Color
    _LED_AVAILABLE = True
except ImportError:
    from hardware.mock_hardware import MockPixelStrip as PixelStrip, MockColor as Color
    _LED_AVAILABLE = False


class LedRing:
    def __init__(self, count, pin, brightness=128, enabled=True):
        self.count = int(count)
        self.pin = int(pin)
        self.brightness = int(brightness)
        self.enabled = bool(enabled)

        self._lock = threading.Lock()
        self.available = _LED_AVAILABLE

        self.strip = PixelStrip(self.count, self.pin, brightness=self.brightness)
        try:
            self.strip.begin()
        except Exception:
            self.available = False

    def _set_all(self, r, g, b):
        if not self.enabled:
            return
        with self._lock:
            color = Color(int(r), int(g), int(b))
            for i in range(self.count):
                self.strip.setPixelColor(i, color)
            self.strip.show()

    def off(self):
        self._set_all(0, 0, 0)

    def on_white(self):
        self._set_all(255, 255, 255)

    def blink_white(self, seconds=1.0):
        if not self.enabled:
            return

        self.on_white()
        time.sleep(max(0.0, float(seconds)))
        self.off()
