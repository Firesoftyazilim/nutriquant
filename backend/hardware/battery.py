# UPS HAT - Pil Yönetimi

try:
    from ina219 import INA219
    from smbus2 import SMBus
except ImportError:
    from hardware.mock_hardware import MockINA219 as INA219
    print("[Mock] Pil sensörü simülasyon modunda")
from config import UPS_I2C_BUS, UPS_I2C_ADDRESS, BATTERY_LOW_THRESHOLD, BATTERY_CRITICAL_THRESHOLD

class Battery:
    def __init__(self):
        try:
            self.ina = INA219(shunt_ohms=0.1, address=UPS_I2C_ADDRESS, busnum=UPS_I2C_BUS)
            self.ina.configure()
            self.available = True
        except Exception as e:
            print(f"UPS HAT bulunamadı: {e}")
            self.available = False
    
    def get_voltage(self):
        """Voltaj oku (V)"""
        if not self.available:
            return 5.0
        try:
            return self.ina.voltage()
        except:
            return 5.0
    
    def get_current(self):
        """Akım oku (mA)"""
        if not self.available:
            return 0
        try:
            return self.ina.current()
        except:
            return 0
    
    def get_power(self):
        """Güç oku (W)"""
        if not self.available:
            return 0
        try:
            return self.ina.power() / 1000
        except:
            return 0
    
    def get_percentage(self):
        """Pil yüzdesi (yaklaşık - voltaj bazlı)"""
        voltage = self.get_voltage()
        
        # Li-ion 2S (7.4V nominal, 8.4V max, 6.0V min)
        v_max = 8.4
        v_min = 6.0
        
        if voltage >= v_max:
            return 100
        elif voltage <= v_min:
            return 0
        else:
            percentage = ((voltage - v_min) / (v_max - v_min)) * 100
            return int(percentage)
    
    def is_charging(self):
        """Şarj oluyor mu?"""
        current = self.get_current()
        return current > 50
    
    def get_status(self):
        """Pil durumu"""
        percentage = self.get_percentage()
        charging = self.is_charging()
        
        if charging:
            return "charging"
        elif percentage <= BATTERY_CRITICAL_THRESHOLD:
            return "critical"
        elif percentage <= BATTERY_LOW_THRESHOLD:
            return "low"
        else:
            return "normal"

# Test fonksiyonu
if __name__ == "__main__":
    import time
    
    battery = Battery()
    print("Pil durumu izleniyor...\n")
    
    try:
        while True:
            print(f"Voltaj: {battery.get_voltage():.2f}V")
            print(f"Akım: {battery.get_current():.0f}mA")
            print(f"Güç: {battery.get_power():.2f}W")
            print(f"Yüzde: %{battery.get_percentage()}")
            print(f"Durum: {battery.get_status()}")
            print("-" * 30)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nÇıkış yapılıyor...")
