# Kamera Flash LED - GPIO ile kısa süreli pulse

import time


try:
    import RPi.GPIO as GPIO
    _GPIO_AVAILABLE = True
except ImportError:
    GPIO = None
    _GPIO_AVAILABLE = False


class Flash:
    def __init__(self, pin, pulse_ms=80, enabled=True, mode_bcm=True):
        self.pin = int(pin)
        self.pulse_ms = int(pulse_ms)
        self.enabled = bool(enabled)
        self.mode_bcm = bool(mode_bcm)
        self.available = _GPIO_AVAILABLE
        self._initialized = False

        if not self.enabled or not self.available:
            return

        try:
            if self.mode_bcm:
                GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)
            self._initialized = True
        except Exception:
            self.available = False
            self._initialized = False

    def pulse(self):
        if not self.enabled or not self.available or not self._initialized:
            return

        try:
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(max(0, self.pulse_ms) / 1000.0)
        finally:
            try:
                GPIO.output(self.pin, GPIO.LOW)
            except Exception:
                pass

    def cleanup(self):
        if not self.enabled or not self.available or not self._initialized:
            return

        try:
            GPIO.output(self.pin, GPIO.LOW)
        except Exception:
            pass

        try:
            GPIO.cleanup(self.pin)
        except Exception:
            pass

        self._initialized = False
