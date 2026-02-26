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
    def __init__(self, pin: int = 3, enabled: bool = True, poll_interval: float = 0.1):
        """
        GPIO3 pinindeki dokunmatik buton için polling-based handler
        
        Args:
            pin: GPIO pin numarası (default: 3)
            enabled: Buton aktif mi
            poll_interval: Polling aralığı (saniye)
        """
        self.pin = int(pin)
        self.enabled = bool(enabled)
        self.poll_interval = float(poll_interval)
        
        self.available = _GPIO_AVAILABLE and self.enabled
        self._initialized = False
        self._last_state = None
        self._last_press_time = 0
        
        # Callback fonksiyonu ve polling thread
        self._callback: Optional[Callable] = None
        self._polling_thread = None
        self._stop_polling = threading.Event()
        
        if not self.available:
            print(f"[TouchButton] GPIO{self.pin} - Mock modda çalışıyor")
            return
            
        try:
            GPIO.setmode(GPIO.BCM)
            # GPIO3 fiziksel pull-up resistor var - None kullan (varsayılan)
            GPIO.setup(self.pin, GPIO.IN)
            
            self._initialized = True
            print(f"[TouchButton] GPIO{self.pin} polling sistemi başlatıldı")
            
        except Exception as e:
            print(f"[TouchButton] GPIO{self.pin} başlatma hatası: {e}")
            self.available = False
            self._initialized = False
    
    def set_callback(self, callback: Callable):
        """Buton basıldığında çağrılacak fonksiyonu ayarla ve polling başlat"""
        self._callback = callback
        print(f"[TouchButton] Callback fonksiyonu ayarlandı")
        self.start_polling()
    
    def start_polling(self):
        """Polling thread'ini başlat"""
        if not self.available or not self._initialized:
            return
            
        if self._polling_thread and self._polling_thread.is_alive():
            return
            
        self._stop_polling.clear()
        self._polling_thread = threading.Thread(target=self._polling_loop, daemon=True)
        self._polling_thread.start()
        print(f"[TouchButton] GPIO{self.pin} polling başlatıldı")
    
    def stop_polling(self):
        """Polling thread'ini durdur"""
        self._stop_polling.set()
        if self._polling_thread:
            self._polling_thread.join(timeout=1)
    
    def _polling_loop(self):
        """Ana polling döngüsü"""
        while not self._stop_polling.is_set():
            try:
                current_state = GPIO.input(self.pin)
                
                # Durum değişikliği kontrolü
                if self._last_state is not None and current_state != self._last_state:
                    current_time = time.time() * 1000  # ms
                    
                    # Debounce kontrolü
                    if (current_time - self._last_press_time) > 100:  # 100ms debounce
                        state_text = "HIGH" if current_state == GPIO.HIGH else "LOW"
                        print(f"[TouchButton] 🔘 GPIO{self.pin} değişti: {state_text}")
                        
                        # Callback'i çağır
                        if self._callback:
                            try:
                                threading.Thread(target=self._callback, daemon=True).start()
                            except Exception as e:
                                print(f"[TouchButton] Callback hatası: {e}")
                        
                        self._last_press_time = current_time
                
                self._last_state = current_state
                
            except Exception as e:
                print(f"[TouchButton] Polling hatası: {e}")
                
            time.sleep(self.poll_interval)
    
    
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
        """GPIO temizleme ve polling durdurma"""
        # Polling'i durdur
        self.stop_polling()
        
        if not self.available or not self._initialized:
            return
            
        try:
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
