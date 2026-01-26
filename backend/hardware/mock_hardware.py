# Mock Donanım - Windows Simülasyonu

import random
import time

class MockHX711:
    """HX711 Simülasyonu"""
    def __init__(self, dout_pin, pd_sck_pin):
        self.reference_unit = 210
        self.tare_value = 0
        self.base_weight = 0  # Temel ağırlık
        self.last_change_time = time.time()
        self.change_interval = 5  # 5 saniyede bir ağırlık değiştir
    
    def set_reading_format(self, byte1, byte2):
        pass
    
    def set_reference_unit(self, value):
        self.reference_unit = value
    
    def reset(self):
        pass
    
    def tare(self, samples=10):
        self.tare_value = random.randint(-100, 100)
        self.base_weight = 0
    
    def get_weight(self, samples=5):
        # Her 5 saniyede bir ağırlığı değiştir
        current_time = time.time()
        if current_time - self.last_change_time > self.change_interval:
            self.base_weight = random.randint(0, 500)
            self.last_change_time = current_time
        
        # Küçük varyasyon ekle (daha gerçekçi)
        noise = random.uniform(-2, 2)
        return max(0, self.base_weight + noise)
    
    def power_down(self):
        pass
    
    def power_up(self):
        pass

class MockGPIO:
    """GPIO Simülasyonu"""
    BCM = 'BCM'
    
    @staticmethod
    def setmode(mode):
        pass
    
    @staticmethod
    def cleanup():
        pass

class MockPixelStrip:
    """WS2812B LED Simülasyonu"""
    def __init__(self, num, pin, brightness=128):
        self.num = num
        self.brightness = brightness
        self.pixels = [(0, 0, 0)] * num
    
    def begin(self):
        pass
    
    def setPixelColor(self, n, color):
        if 0 <= n < self.num:
            self.pixels[n] = color
    
    def show(self):
        pass

def MockColor(r, g, b):
    """Renk simülasyonu"""
    return (r, g, b)

class MockINA219:
    """INA219 Pil Sensörü Simülasyonu"""
    def __init__(self, shunt_ohms=0.1, address=0x36, busnum=1):
        self.voltage_val = 7.8
        self.current_val = 500
    
    def configure(self):
        pass
    
    def voltage(self):
        return self.voltage_val + random.uniform(-0.1, 0.1)
    
    def current(self):
        return self.current_val + random.uniform(-50, 50)
    
    def power(self):
        return self.voltage() * self.current()

class MockPicamera2:
    """Picamera2 Simülasyonu"""
    def __init__(self):
        self.running = False
    
    def create_still_configuration(self, main=None):
        return {}
    
    def configure(self, config):
        pass
    
    def start(self):
        self.running = True
        print("[Mock] Kamera başlatıldı")
    
    def capture_array(self):
        import numpy as np
        return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    def stop(self):
        self.running = False
        print("[Mock] Kamera durduruldu")
