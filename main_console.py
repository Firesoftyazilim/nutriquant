# Nutriquant - Konsol Simülasyonu (Windows Test)

import time
import sys
from hardware.scale import Scale
from hardware.camera import Camera
from hardware.battery import Battery
from hardware.led_ring import LEDRing
from ai.food_recognition import FoodRecognizer
from core.nutrition import NutritionCalculator
from core.bmi import BMICalculator
from core.database import Database
from config import MIN_WEIGHT_THRESHOLD

class NutriquantConsole:
    def __init__(self):
        print("=" * 60)
        print("NUTRIQUANT - Akıllı Yemek Tartısı (Konsol Simülasyonu)")
        print("=" * 60)
        print("\nSistem başlatılıyor...\n")
        
        self.scale = Scale()
        self.camera = Camera()
        self.battery = Battery()
        self.led = LEDRing()
        self.recognizer = FoodRecognizer()
        self.nutrition_calc = NutritionCalculator()
        self.bmi_calc = BMICalculator()
        self.db = Database()
        
        self.current_user = self.load_default_user()
        
        print("\n✓ Sistem hazır!")
        print("=" * 60)
        self.led.green()
        time.sleep(1)
        self.led.off()
    
    def load_default_user(self):
        """Varsayılan kullanıcı yükle"""
        user = self.db.get_user(1)
        if not user:
            user = {
                "name": "Test Kullanıcı",
                "age": 30,
                "weight": 70,
                "height": 175
            }
            self.db.save_user(1, user)
        return user
    
    def run(self):
        """Ana döngü"""
        try:
            print("\n[CTRL+C ile çıkış yapabilirsiniz]\n")
            
            for i in range(3):  # 3 ölçüm simülasyonu
                print(f"\n{'='*60}")
                print(f"ÖLÇÜM #{i+1}")
                print(f"{'='*60}")
                
                battery_percent = self.battery.get_percentage()
                print(f"🔋 Pil: %{battery_percent}")
                print("\n⏳ Tartıya yemek yerleştiriliyor...")
                time.sleep(1)
                
                weight = self.scale.read_weight()
                
                if weight >= MIN_WEIGHT_THRESHOLD:
                    self.process_measurement(weight)
                else:
                    print(f"⚠️  Ağırlık çok düşük: {weight}g (min: {MIN_WEIGHT_THRESHOLD}g)")
                
                print("\n⏸️  5 saniye bekleniyor...")
                time.sleep(5)
            
            print("\n" + "="*60)
            print("Simülasyon tamamlandı!")
            print("="*60)
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Kapatılıyor...")
        
        finally:
            self.cleanup()
    
    def process_measurement(self, weight):
        """Ölçüm işle"""
        print(f"\n📊 Ölçüm: {weight}g")
        
        self.led.blue()
        print("🔵 LED: Mavi (İşlem yapılıyor)")
        time.sleep(1)
        
        self.led.white()
        print("⚪ LED: Beyaz (Görüntü yakalama)")
        print("📷 Kamera görüntü alıyor...")
        image = self.camera.capture_image()
        
        print("🤖 AI yemek tanıma çalışıyor...")
        food_key, confidence = self.recognizer.recognize(image)
        
        if not food_key:
            print("❌ Yemek tanınamadı")
            self.led.yellow()
            print("🟡 LED: Sarı (Uyarı)")
            time.sleep(2)
            self.led.off()
            return
        
        print(f"✓ Tanınan yemek: {food_key} (Güven: %{confidence*100:.1f})")
        
        nutrition = self.nutrition_calc.calculate(food_key, weight)
        
        if not nutrition:
            print("❌ Besin değerleri hesaplanamadı")
            self.led.red()
            print("🔴 LED: Kırmızı (Hata)")
            time.sleep(2)
            self.led.off()
            return
        
        bmi = self.bmi_calc.calculate(
            self.current_user['weight'],
            self.current_user['height']
        )
        bmi_comment = self.bmi_calc.get_comment(bmi, self.current_user['age'])
        should_warn = self.bmi_calc.should_warn(bmi, self.current_user['age'])
        
        self.db.add_measurement(
            user_id=1,
            food_name=nutrition['name'],
            weight=weight,
            nutrition=nutrition,
            bmi_data={'bmi': bmi, 'comment': bmi_comment}
        )
        
        print("\n" + "─"*60)
        print(f"🍽️  YEMEK: {nutrition['name']}")
        print(f"⚖️  AĞIRLIK: {nutrition['weight']}g")
        print("─"*60)
        print(f"🔥 Kalori:       {nutrition['calorie']} kcal")
        print(f"💪 Protein:      {nutrition['protein']}g")
        print(f"🌾 Karbonhidrat: {nutrition['carb']}g")
        print(f"🧈 Yağ:          {nutrition['fat']}g")
        print("─"*60)
        print(f"📈 VKİ: {bmi} - {bmi_comment}")
        print("─"*60)
        
        if should_warn:
            self.led.red()
            print("🔴 LED: Kırmızı (VKİ Uyarısı)")
            print("⚠️  UYARI: Kalori alımınıza dikkat edin!")
        else:
            self.led.green()
            print("🟢 LED: Yeşil (Başarılı)")
            print("✓ Besin değerleri kaydedildi")
        
        time.sleep(3)
        self.led.off()
    
    def cleanup(self):
        """Kaynakları temizle"""
        print("\n🧹 Temizlik yapılıyor...")
        self.led.off()
        self.scale.cleanup()
        self.camera.cleanup()
        print("✓ Sistem kapatıldı.")

if __name__ == "__main__":
    app = NutriquantConsole()
    app.run()
