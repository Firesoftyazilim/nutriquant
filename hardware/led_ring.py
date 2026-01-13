# LED Ring (WS2812B) - Görsel Geri Bildirim

import time
try:
    from rpi_ws281x import PixelStrip, Color
except ImportError:
    from hardware.mock_hardware import MockPixelStrip as PixelStrip, MockColor as Color
    print("[Mock] LED Ring simülasyon modunda")
from config import LED_PIN, LED_COUNT, LED_BRIGHTNESS

class LEDRing:
    def __init__(self):
        self.strip = PixelStrip(LED_COUNT, LED_PIN, brightness=LED_BRIGHTNESS)
        self.strip.begin()
        self.off()
    
    def set_color(self, r, g, b):
        """Tüm LED'leri aynı renge ayarla"""
        color = Color(r, g, b)
        for i in range(LED_COUNT):
            self.strip.setPixelColor(i, color)
        self.strip.show()
    
    def off(self):
        """Tüm LED'leri kapat"""
        self.set_color(0, 0, 0)
    
    def white(self):
        """Beyaz ışık - ölçüm sırasında"""
        self.set_color(255, 255, 255)
    
    def green(self):
        """Yeşil - başarılı"""
        self.set_color(0, 255, 0)
    
    def red(self):
        """Kırmızı - uyarı"""
        self.set_color(255, 0, 0)
    
    def blue(self):
        """Mavi - işlem yapılıyor"""
        self.set_color(0, 0, 255)
    
    def yellow(self):
        """Sarı - bekleniyor"""
        self.set_color(255, 255, 0)
    
    def pulse(self, r, g, b, duration=1.0, steps=20):
        """Nabız efekti"""
        for i in range(steps):
            brightness = int((i / steps) * 255)
            self.set_color(
                int(r * brightness / 255),
                int(g * brightness / 255),
                int(b * brightness / 255)
            )
            time.sleep(duration / (steps * 2))
        
        for i in range(steps, 0, -1):
            brightness = int((i / steps) * 255)
            self.set_color(
                int(r * brightness / 255),
                int(g * brightness / 255),
                int(b * brightness / 255)
            )
            time.sleep(duration / (steps * 2))
    
    def rainbow(self, duration=2.0):
        """Gökkuşağı efekti"""
        colors = [
            (255, 0, 0),    # Kırmızı
            (255, 127, 0),  # Turuncu
            (255, 255, 0),  # Sarı
            (0, 255, 0),    # Yeşil
            (0, 0, 255),    # Mavi
            (75, 0, 130),   # Çivit
            (148, 0, 211)   # Mor
        ]
        
        step_time = duration / len(colors)
        for color in colors:
            self.set_color(*color)
            time.sleep(step_time)

# Test fonksiyonu
if __name__ == "__main__":
    led = LEDRing()
    
    try:
        print("Beyaz...")
        led.white()
        time.sleep(1)
        
        print("Yeşil...")
        led.green()
        time.sleep(1)
        
        print("Kırmızı...")
        led.red()
        time.sleep(1)
        
        print("Mavi nabız...")
        led.pulse(0, 0, 255)
        
        print("Gökkuşağı...")
        led.rainbow()
        
    finally:
        led.off()
