# HX711 Tartı Modülü - Ağırlık Ölçümü

import time
try:
    from hx711 import HX711
    import RPi.GPIO as GPIO
except ImportError:
    from hardware.mock_hardware import MockHX711 as HX711, MockGPIO as GPIO
    print("[Mock] HX711 simülasyon modunda")
from config import HX711_DOUT_PIN, HX711_SCK_PIN, HX711_REFERENCE_UNIT, TARE_SAMPLES

class Scale:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.hx = HX711(dout_pin=HX711_DOUT_PIN, pd_sck_pin=HX711_SCK_PIN)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(HX711_REFERENCE_UNIT)
        self.hx.reset()
        self.tare()
    
    def tare(self):
        """Tartıyı sıfırla"""
        self.hx.tare(TARE_SAMPLES)
        time.sleep(0.5)
    
    def read_weight(self, samples=5):
        """Ağırlık oku (gram cinsinden)"""
        try:
            weight = self.hx.get_weight(samples)
            self.hx.power_down()
            time.sleep(0.01)
            self.hx.power_up()
            return max(0, int(weight))
        except Exception as e:
            print(f"Tartı okuma hatası: {e}")
            return 0
    
    def calibrate(self, known_weight_grams):
        """Kalibrasyon yap - bilinen ağırlık ile"""
        raw_value = self.hx.get_weight(10)
        reference_unit = raw_value / known_weight_grams
        self.hx.set_reference_unit(reference_unit)
        return reference_unit
    
    def cleanup(self):
        """GPIO temizle"""
        GPIO.cleanup()

# Test fonksiyonu
if __name__ == "__main__":
    scale = Scale()
    print("Tartı hazır. Ağırlık ölçülüyor...")
    
    try:
        while True:
            weight = scale.read_weight()
            print(f"Ağırlık: {weight} gram")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nÇıkış yapılıyor...")
        scale.cleanup()
