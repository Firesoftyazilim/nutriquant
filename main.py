# Nutriquant - Ana Uygulama
# Raspberry Pi 4 - Akıllı Yemek Tartısı

import time
import sys
from hardware.scale import Scale
from hardware.camera import Camera
from hardware.battery import Battery
from hardware.led_ring import LEDRing
from hardware.speaker import Speaker
from ai.food_recognition import FoodRecognizer
from core.nutrition import NutritionCalculator
from core.bmi import BMICalculator
from core.database import Database
from ui.display import Display
from config import MIN_WEIGHT_THRESHOLD

class Nutriquant:
    def __init__(self):
        print("Nutriquant başlatılıyor...")
        
        self.scale = Scale()
        self.camera = Camera()
        self.battery = Battery()
        self.led = LEDRing()
        self.speaker = Speaker()
        self.recognizer = FoodRecognizer()
        self.nutrition_calc = NutritionCalculator()
        self.bmi_calc = BMICalculator()
        self.db = Database()
        self.display = Display()
        
        self.current_user = self.load_default_user()
        
        print("Sistem hazır!")
        self.speaker.play_ready()
        self.led.green()
        time.sleep(1)
        self.led.off()
    
    def load_default_user(self):
        """Varsayılan kullanıcı yükle"""
        user = self.db.get_user(1)
        if not user:
            user = {
                "name": "Kullanıcı",
                "age": 30,
                "weight": 70,
                "height": 175
            }
            self.db.save_user(1, user)
        return user
    
    def run(self):
        """Ana döngü"""
        try:
            while True:
                battery_percent = self.battery.get_percentage()
                self.display.show_home_screen(battery_percent)
                
                event = self.display.handle_events()
                if event == 'quit':
                    break
                
                weight = self.scale.read_weight()
                
                if weight >= MIN_WEIGHT_THRESHOLD:
                    self.process_measurement(weight)
                
                time.sleep(0.5)
        
        except KeyboardInterrupt:
            print("\nKapatılıyor...")
        
        finally:
            self.cleanup()
    
    def process_measurement(self, weight):
        """Ölçüm işle"""
        print(f"\nÖlçüm: {weight}g")
        
        self.led.blue()
        self.speaker.play_beep()
        self.display.show_measuring_screen(weight)
        time.sleep(1)
        
        self.led.white()
        image = self.camera.capture_image()
        
        food_key, confidence = self.recognizer.recognize(image)
        
        if not food_key:
            print("Yemek tanınamadı")
            self.led.yellow()
            self.speaker.play_warning()
            self.display.show_error_screen("Yemek tanınamadı")
            time.sleep(2)
            self.led.off()
            return
        
        print(f"Tanınan yemek: {food_key} (%{confidence*100:.1f})")
        
        nutrition = self.nutrition_calc.calculate(food_key, weight)
        
        if not nutrition:
            print("Besin değerleri hesaplanamadı")
            self.led.red()
            self.speaker.play_error()
            self.display.show_error_screen("Besin değerleri bulunamadı")
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
        
        if should_warn:
            self.led.red()
            self.speaker.play_warning()
        else:
            self.led.green()
            self.speaker.play_success()
        
        self.display.show_result_screen(nutrition['name'], nutrition, bmi_comment)
        
        print(f"\n{nutrition['name']}: {nutrition['weight']}g")
        print(f"Kalori: {nutrition['calorie']} kcal")
        print(f"Protein: {nutrition['protein']}g")
        print(f"Karbonhidrat: {nutrition['carb']}g")
        print(f"Yağ: {nutrition['fat']}g")
        print(f"VKİ: {bmi} - {bmi_comment}")
        
        time.sleep(5)
        self.led.off()
    
    def cleanup(self):
        """Kaynakları temizle"""
        print("Temizlik yapılıyor...")
        self.led.off()
        self.scale.cleanup()
        self.camera.cleanup()
        self.display.cleanup()
        print("Sistem kapatıldı.")

if __name__ == "__main__":
    app = Nutriquant()
    app.run()
