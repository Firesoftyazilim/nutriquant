# HX711 Tartı Modülü - Ağırlık Ölçümü

import time
import sys
import threading

# Import denemesi ve hata ayıklama
try:
    from hardware.hx711 import HX711
    import RPi.GPIO as GPIO
    MODE = "REAL"
    print("[Scale] Gerçek donanım sürücüleri yüklendi (HX711).")
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
        self.current_weight = 0  # Son okunan ağırlık
        self.lock = threading.Lock()  # Thread-safe erişim için
        self.reading_thread = None
        self.running = False
        
        if self.mode == "MOCK":
            print("[Scale] MOCK modda başlatıldı")
            return
        
        try:
            # HX711 başlat (GPIO 5=DOUT, 6=SCK)
            self.hx = HX711(HX711_DOUT_PIN, HX711_SCK_PIN)
            
            # Reading format ayarla (MSB, MSB)
            self.hx.set_reading_format("MSB", "MSB")
            
            # Reference unit ayarla (kalibrasyon değeri)
            print(f"[Scale] Reference unit ayarlanıyor: {HX711_REFERENCE_UNIT}")
            self.hx.set_reference_unit(HX711_REFERENCE_UNIT)
            
            # Tare yap (offset ayarla)
            print("[Scale] Tare yapılıyor...")
            self.hx.tare(TARE_SAMPLES)
            
            # Sürekli okuma thread'i başlat
            self.running = True
            self.reading_thread = threading.Thread(target=self._continuous_reading, daemon=True)
            self.reading_thread.start()
            
            print(f"[Scale] Başlatıldı (Mod: {self.mode}, Continuous reading)")
            
        except Exception as e:
            print(f"[Scale] Başlatma hatası: {e}")
            print("[Scale] MOCK moda geçiliyor...")
            self.mode = "MOCK"
    
    def _continuous_reading(self):
        """Arka planda sürekli ağırlık oku"""
        while self.running:
            try:
                # HX711'den ağırlık oku (3 örnek ortalaması)
                weight = self.hx.get_weight(3)
                
                with self.lock:
                    # Negatif değerleri filtrele, gram cinsine çevir
                    self.current_weight = max(0, int(weight))
                
                # Kısa bekleme (CPU kullanımını azaltmak için)
                time.sleep(0.1)
                
            except Exception as e:
                print(f"[Scale] Okuma hatası: {e}")
                time.sleep(0.5)
    
    def read_weight(self):
        """Anlık ağırlık değerini döndür (gram)"""
        if self.mode == "MOCK":
            return 0
        
        with self.lock:
            return self.current_weight
    
    def tare(self):
        """Tartıyı sıfırla - offset'i yeniden ayarla"""
        if self.mode == "MOCK":
            print("[Scale] MOCK modda tare yapılamaz")
            return
        
        try:
            print("[Scale] Tare yapılıyor...")
            self.hx.tare(TARE_SAMPLES)
            print(f"[Scale] Tare tamamlandı")
            with self.lock:
                self.current_weight = 0
        except Exception as e:
            print(f"[Scale] Tare hatası: {e}")
    
    def calibrate(self, known_weight_grams):
        """
        Kalibrasyon yap - bilinen ağırlık ile reference unit hesapla
        
        Kullanım:
        1. Tartıyı sıfırla (tare)
        2. Bilinen ağırlığı koy (örn: 1000g)
        3. Bu fonksiyonu çağır: scale.calibrate(1000)
        """
        if self.mode == "MOCK":
            print("[Scale] MOCK modda kalibrasyon yapılamaz")
            return HX711_REFERENCE_UNIT
        
        try:
            print(f"[Scale] Kalibrasyon başlıyor ({known_weight_grams}g ile)...")
            print("[Scale] Lütfen birkaç saniye bekleyin...")
            
            # Birkaç okuma yap ve ortalama al
            time.sleep(1)
            value = self.hx.get_value(10)
            
            # Reference unit hesapla
            new_reference_unit = value / known_weight_grams
            
            print(f"[Scale] Okunan değer: {value}")
            print(f"[Scale] Yeni reference unit: {new_reference_unit}")
            
            # Yeni reference unit'i ayarla
            self.hx.set_reference_unit(new_reference_unit)
            
            print(f"[Scale] Kalibrasyon tamamlandı!")
            print(f"[Scale] config.py dosyasında HX711_REFERENCE_UNIT = {int(new_reference_unit)} olarak güncelleyin")
            
            return new_reference_unit
            
        except Exception as e:
            print(f"[Scale] Kalibrasyon hatası: {e}")
            return HX711_REFERENCE_UNIT
    
    def cleanup(self):
        """GPIO temizle ve thread'i durdur"""
        try:
            # Thread'i durdur
            self.running = False
            if self.reading_thread:
                self.reading_thread.join(timeout=2)
            
            # GPIO temizle
            if self.mode != "MOCK":
                GPIO.cleanup()
        except Exception as e:
            print(f"[Scale] Cleanup hatası: {e}")

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
