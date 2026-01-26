# HX711 Tartı Modülü - Ağırlık Ölçümü (hx711v0_5_1)

import time
import sys
import threading

# Import denemesi ve hata ayıklama
try:
    from hx711v0_5_1 import HX711
    import RPi.GPIO as GPIO
    MODE = "REAL"
    print("[Scale] Gerçek donanım sürücüleri yüklendi (hx711v0_5_1).")
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
        
        if self.mode == "MOCK":
            print("[Scale] MOCK modda başlatıldı")
            return
        
        try:
            # HX711 başlat (GPIO 5=DOUT, 6=SCK)
            self.hx = HX711(HX711_DOUT_PIN, HX711_SCK_PIN)
            
            # Reading format ayarla (MSB, MSB)
            self.hx.setReadingFormat("MSB", "MSB")
            
            # Otomatik offset ayarla
            print("[Scale] Otomatik offset ayarlanıyor...")
            self.hx.autosetOffset()
            offset_value = self.hx.getOffset()
            print(f"[Scale] Offset ayarlandı: {offset_value}")
            
            # Reference unit ayarla (kalibrasyon değeri)
            print(f"[Scale] Reference unit ayarlanıyor: {HX711_REFERENCE_UNIT}")
            self.hx.setReferenceUnit(HX711_REFERENCE_UNIT)
            
            # Interrupt-based callback aktifleştir
            print("[Scale] Interrupt-based okuma aktifleştiriliyor...")
            self.hx.enableReadyCallback(self._weight_callback)
            
            print(f"[Scale] Başlatıldı (Mod: {self.mode}, Interrupt-based)")
            
        except Exception as e:
            print(f"[Scale] Başlatma hatası: {e}")
            print("[Scale] MOCK moda geçiliyor...")
            self.mode = "MOCK"
    
    def _weight_callback(self, rawBytes):
        """HX711 interrupt callback - her yeni veri geldiğinde çağrılır"""
        try:
            weight_grams = self.hx.rawBytesToWeight(rawBytes)
            with self.lock:
                # Negatif değerleri filtrele
                self.current_weight = max(0, int(weight_grams))
        except Exception as e:
            print(f"[Scale] Callback hatası: {e}")
    
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
            self.hx.autosetOffset()
            offset_value = self.hx.getOffset()
            print(f"[Scale] Yeni offset: {offset_value}")
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
            
            # Birkaç okuma yap
            time.sleep(2)
            
            # Raw bytes al
            rawBytes = self.hx.getRawBytes()
            longValue = self.hx.rawBytesToLong(rawBytes)
            longWithOffset = self.hx.rawBytesToLongWithOffset(rawBytes)
            
            # Reference unit hesapla
            new_reference_unit = longWithOffset / known_weight_grams
            
            print(f"[Scale] Long value: {longValue}")
            print(f"[Scale] Long with offset: {longWithOffset}")
            print(f"[Scale] Yeni reference unit: {new_reference_unit}")
            
            # Yeni reference unit'i ayarla
            self.hx.setReferenceUnit(new_reference_unit)
            
            print(f"[Scale] Kalibrasyon tamamlandı!")
            print(f"[Scale] config.py dosyasında HX711_REFERENCE_UNIT = {int(new_reference_unit)} olarak güncelleyin")
            
            return new_reference_unit
            
        except Exception as e:
            print(f"[Scale] Kalibrasyon hatası: {e}")
            return HX711_REFERENCE_UNIT
    
    def cleanup(self):
        """GPIO temizle"""
        try:
            if self.mode != "MOCK":
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
