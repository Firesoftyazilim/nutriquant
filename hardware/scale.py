# HX711 Tartı Modülü - Ağırlık Ölçümü

import time
import sys

# Import denemesi ve hata ayıklama
try:
    from hx711 import HX711
    import RPi.GPIO as GPIO
    MODE = "REAL"
    print("[Scale] Gerçek donanım sürücüleri yüklendi.")
except ImportError as e:
    print(f"\n[DIKKAT] Donanım sürücü hatası: {e}")
    print("[DIKKAT] Sistem SIMULASYON moduna geçiyor. Rastgele değerler üretilecek.\n")
    from hardware.mock_hardware import MockHX711 as HX711, MockGPIO as GPIO
    MODE = "MOCK"
except Exception as e:
    print(f"\n[DIKKAT] Beklenmedik başlatma hatası: {e}")
    from hardware.mock_hardware import MockHX711 as HX711, MockGPIO as GPIO
    MODE = "MOCK"

from config import HX711_DOUT_PIN, HX711_SCK_PIN, HX711_REFERENCE_UNIT, TARE_SAMPLES

class Scale:
    def __init__(self):
        self.mode = MODE
        try:
            GPIO.setmode(GPIO.BCM)
            self.hx = HX711(dout_pin=HX711_DOUT_PIN, pd_sck_pin=HX711_SCK_PIN)
            
            # tatobari/hx711py API
            self.hx.set_reading_format("MSB", "MSB")
            self.hx.set_reference_unit(HX711_REFERENCE_UNIT)
            self.hx.reset()
            self.tare()
            print(f"[Scale] Başlatıldı (Mod: {self.mode})")
        except Exception as e:
            print(f"[Scale] Başlatma hatası: {e}")
            
    def tare(self):
        """Tartıyı sıfırla"""
        try:
            self.hx.tare(TARE_SAMPLES)
            time.sleep(0.5)
        except Exception as e:
            print(f"[Scale] Tare hatası: {e}")
            
    
    def read_weight(self, samples=5):
        """Ağırlık oku (gram cinsinden)"""
        try:
            # tatobari/hx711py API: get_weight_mean() kullanır
            weight = self.hx.get_weight_mean(samples)
            
            # Negatif değerleri filtrele
            final_weight = max(0, int(weight))
            
            # Mock modundaysak ve değer 0 ise, ara sıra rastgelelik ekle (kullanıcı test edebilsin diye)
            if self.mode == "MOCK" and final_weight == 0:
                pass 
                
            return final_weight
        except Exception as e:
            print(f"Tartı okuma hatası: {e}")
            return 0
    
    def calibrate(self, known_weight_grams):
        """Kalibrasyon yap - bilinen ağırlık ile"""
        # tatobari/hx711py API: get_weight_mean() kullanır
        raw_value = self.hx.get_weight_mean(10)
        reference_unit = raw_value / known_weight_grams
        self.hx.set_reference_unit(reference_unit)
        return reference_unit
    
    def cleanup(self):
        """GPIO temizle"""
        try:
            GPIO.cleanup()
        except:
            pass

# Test fonksiyonu
if __name__ == "__main__":
    scale = Scale()
    print(f"Tartı hazır (Mod: {scale.mode}). Ağırlık ölçülüyor...")
    
    try:
        while True:
            weight = scale.read_weight()
            print(f"Ağırlık: {weight} gram")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nÇıkış yapılıyor...")
        scale.cleanup()
