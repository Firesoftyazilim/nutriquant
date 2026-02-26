# GPIO3 Dokunmatik Buton - Power Modal Tetikleyici

import threading
import time
import requests
from typing import Optional, Callable

try:
    import RPi.GPIO as GPIO
    _GPIO_AVAILABLE = True
except ImportError:
    GPIO = None
    _GPIO_AVAILABLE = False


class TouchButton:
    def __init__(self, pin: int = 3, enabled: bool = True, debounce_ms: int = 50):
        """
        GPIO3 pinindeki dokunmatik buton için interrupt handler
        
        Args:
            pin: GPIO pin numarası (default: 3)
            enabled: Buton aktif mi
            debounce_ms: Debounce süresi (ms)
        """
        self.pin = int(pin)
        self.enabled = bool(enabled)
        self.debounce_ms = int(debounce_ms)
        
        self.available = _GPIO_AVAILABLE and self.enabled
        self._initialized = False
        self._last_press_time = 0
        
        # Callback fonksiyonu
        self._callback: Optional[Callable] = None
        
        if not self.available:
            print(f"[TouchButton] GPIO{self.pin} - Mock modda çalışıyor")
            return
            
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
            # Interrupt callback ekle (falling edge - buton basıldığında)
            GPIO.add_event_detect(
                self.pin, 
                GPIO.FALLING, 
                callback=self._interrupt_handler,
                bouncetime=self.debounce_ms
            )
            
            self._initialized = True
            print(f"[TouchButton] GPIO{self.pin} başarıyla başlatıldı")
            
        except Exception as e:
            print(f"[TouchButton] GPIO{self.pin} başlatma hatası: {e}")
            self.available = False
            self._initialized = False
    
    def set_callback(self, callback: Callable):
        """Buton basıldığında çağrılacak fonksiyonu ayarla"""
        self._callback = callback
        print(f"[TouchButton] Callback fonksiyonu ayarlandı")
    
    def _interrupt_handler(self, channel):
        """GPIO interrupt handler"""
        current_time = time.time() * 1000  # ms
        
        # Debounce kontrolü
        if (current_time - self._last_press_time) < self.debounce_ms:
            return
            
        self._last_press_time = current_time
        
        print(f"[TouchButton] GPIO{self.pin} basıldı!")
        
        # Callback fonksiyonunu çağır
        if self._callback:
            try:
                # Thread'de çalıştır ki interrupt bloklanmasın
                threading.Thread(target=self._callback, daemon=True).start()
            except Exception as e:
                print(f"[TouchButton] Callback hatası: {e}")
    
    def trigger_power_modal(self):
        """Power modal'ını tetikle - basit flag sistemi"""
        print("[TouchButton] 🔘 GPIO3 dokunmatik buton basıldı - Power modal tetikleniyor!")
        
        # Global flag dosyası oluştur - frontend bunu kontrol edecek
        try:
            with open('/tmp/power_modal_trigger', 'w') as f:
                f.write(str(time.time()))
            print("[TouchButton] Power modal trigger flag oluşturuldu")
        except Exception as e:
            print(f"[TouchButton] Flag oluşturma hatası: {e}")
    
    def cleanup(self):
        """GPIO temizleme"""
        if not self.available or not self._initialized:
            return
            
        try:
            GPIO.remove_event_detect(self.pin)
            GPIO.cleanup(self.pin)
            print(f"[TouchButton] GPIO{self.pin} temizlendi")
        except Exception as e:
            print(f"[TouchButton] Temizleme hatası: {e}")
            
        self._initialized = False
    
    def __del__(self):
        """Destructor - otomatik temizleme"""
        self.cleanup()


# Test fonksiyonu
def test_touch_button():
    """Dokunmatik buton test fonksiyonu"""
    def on_button_press():
        print("🔘 Dokunmatik buton basıldı - Power modal açılıyor!")
    
    button = TouchButton(pin=3, enabled=True)
    button.set_callback(on_button_press)
    
    try:
        print("Dokunmatik buton testi başlatıldı. Ctrl+C ile çıkış...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTest sonlandırılıyor...")
    finally:
        button.cleanup()


if __name__ == "__main__":
    test_touch_button()
