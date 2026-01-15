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
        self.offset = 0  # Tare offset
        self.scale_ratio = HX711_REFERENCE_UNIT  # Kalibrasyon değeri
        
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)  # Uyarıları kapat
            
            self.hx = HX711(dout_pin=HX711_DOUT_PIN, pd_sck_pin=HX711_SCK_PIN)
            
            # Reset ve bağlantı testi - non-blocking
            print("[Scale] Sensör bağlantısı test ediliyor...")
            if not self._is_ready(timeout=2.0):
                print("[Scale] Sensör yanıt vermiyor (Zaman aşımı)")
                print("[Scale] MOCK moda geçiliyor...")
                self.mode = "MOCK"
                return
            
            print(f"[Scale] Sensör OK.")
            # İlk tare
            self.tare()
            
            print(f"[Scale] Başlatıldı (Mod: {self.mode})")
        except Exception as e:
            print(f"[Scale] Başlatma hatası: {e}")
            print("[Scale] MOCK moda geçiliyor...")
            self.mode = "MOCK"
    
    def _is_ready(self, timeout=1.0):
        """Sensörün hazır olup olmadığını (DOUT pininin LOW olmasını) kontrol et"""
        if self.mode == "MOCK":
            return True
        
        start_time = time.time()
        try:
            # HX711 veri göndermeye hazır olduğunda DOUT pinini LOW'a çeker
            while GPIO.input(HX711_DOUT_PIN) == 1:
                if time.time() - start_time > timeout:
                    return False
                time.sleep(0.01)
            return True
        except:
            return False

            
    def tare(self):
        """Tartıyı sıfırla - offset hesapla"""
        if self.mode == "MOCK":
            return
            
        try:
            # Sensör hazır mı kontrol et
            if not self._is_ready():
                print("[Scale] Tare hatası: Sensör hazır değil")
                return
                
            # Birkaç okuma yapıp ortalama al
            readings = []
            for _ in range(10):
                if not self._is_ready(): continue
                data = self.hx.get_raw_data()
                if data:
                    readings.append(data)
                time.sleep(0.05)
            
            if readings:
                self.offset = sum(readings) / len(readings)
                print(f"[Scale] Tare: offset = {self.offset:.0f}")
            else:
                print("[Scale] Tare hatası: Veri okunamadı")
                
        except Exception as e:
            print(f"[Scale] Tare hatası: {e}")
            
    
    def read_weight(self, samples=5):
        """Ağırlık oku (gram cinsinden)"""
        # MOCK modda 0 döndür
        if self.mode == "MOCK":
            return 0
            
        try:
            # Ham veri oku
            readings = []
            for _ in range(samples):
                if not self._is_ready(timeout=0.1): continue
                data = self.hx.get_raw_data()
                if data:
                    readings.append(data)
                time.sleep(0.02)
            
            if not readings:
                return 0
            
            # Ortalama al
            avg_raw = sum(readings) / len(readings)
            
            # Offset çıkar ve scale ratio ile böl
            weight = (avg_raw - self.offset) / self.scale_ratio
            
            # Negatif değerleri filtrele
            final_weight = max(0, int(weight))
            
            return final_weight
            
        except Exception as e:
            print(f"Tartı okuma hatası: {e}")
            return 0
    
    def calibrate(self, known_weight_grams):
        """Kalibrasyon yap - bilinen ağırlık ile"""
        try:
            # Ham değerleri oku
            readings = []
            for _ in range(10):
                data = self.hx.get_raw_data()
                if data:
                    readings.append(data)
                time.sleep(0.1)
            
            if not readings:
                print("Kalibrasyon hatası: Veri okunamadı")
                return self.scale_ratio
            
            avg_raw = sum(readings) / len(readings)
            
            # Scale ratio hesapla: (raw - offset) / weight = ratio
            self.scale_ratio = (avg_raw - self.offset) / known_weight_grams
            
            print(f"[Scale] Yeni scale_ratio: {self.scale_ratio:.2f}")
            
            return self.scale_ratio
            
        except Exception as e:
            print(f"Kalibrasyon hatası: {e}")
            return self.scale_ratio
    
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
