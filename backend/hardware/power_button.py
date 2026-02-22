import os
import threading
import time


try:
    import RPi.GPIO as GPIO
    _GPIO_AVAILABLE = True
except ImportError:
    GPIO = None
    _GPIO_AVAILABLE = False


class PowerButton:
    def __init__(self, pin, hold_seconds=3, enabled=True, poll_interval=0.05):
        self.pin = int(pin)
        self.hold_seconds = float(hold_seconds)
        self.enabled = bool(enabled)
        self.poll_interval = float(poll_interval)

        self.available = _GPIO_AVAILABLE
        self._initialized = False

        self._thread = None
        self._stop_event = threading.Event()

        if not self.enabled or not self.available:
            return

        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self._initialized = True
        except Exception:
            self.available = False
            self._initialized = False

    def start(self):
        if not self.enabled or not self.available or not self._initialized:
            return
        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1)

    def cleanup(self):
        self.stop()

        if not self.enabled or not self.available or not self._initialized:
            return

        try:
            GPIO.cleanup(self.pin)
        except Exception:
            pass

        self._initialized = False

    def _is_pressed(self):
        try:
            return GPIO.input(self.pin) == GPIO.LOW
        except Exception:
            return False

    def _shutdown(self):
        os.system("sudo /sbin/shutdown -h now")

    def _run(self):
        pressed_since = None

        while not self._stop_event.is_set():
            pressed = self._is_pressed()
            now = time.monotonic()

            if pressed:
                if pressed_since is None:
                    pressed_since = now
                elif (now - pressed_since) >= self.hold_seconds:
                    self._shutdown()
                    return
            else:
                pressed_since = None

            time.sleep(self.poll_interval)
