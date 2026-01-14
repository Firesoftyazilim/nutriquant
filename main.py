# Nutriquant - Ana Uygulama
# Raspberry Pi 4 - Akıllı Yemek Tartısı
# v2.0 - Dashboard ve Manuel Kontrol

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
from ui.display import Display, UIState
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
        
        # UI Başlat
        self.display = Display()
        self.state = UIState.DASHBOARD
        
        self.current_user = self.load_default_user()
        self.current_nutrition = None # Son ölçüm sonucu
        
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
                # 1. Sensörleri Oku
                weight = self.scale.read_weight()
                battery_percent = self.battery.get_percentage()
                
                # 2. UI Durumuna Göre Çizim Yap
                if self.display.state == UIState.DASHBOARD:
                    self.display.show_dashboard(weight, battery_percent)
                
                elif self.display.state == UIState.TEST_MENU:
                    self.display.show_test_menu()
                    
                elif self.display.state == UIState.TEST_SCALE:
                    self.display.show_test_scale(weight)
                    
                elif self.display.state == UIState.TEST_SPEAKER:
                    self.display.show_test_speaker()
                    
                elif self.display.state == UIState.TEST_CAMERA:
                    # Kamera test modunda sadece UI göster, rpicam-vid arka planda çalışıyor
                    self.display.show_camera_feed()

                    
                # 3. Olayları Dinle
                event = self.display.handle_events()
                
                if event == 'quit':
                    break
                    
                elif event == 'click_scan':
                    self.perform_scan(weight)
                    
                elif event == 'click_retry':
                    self.display.state = UIState.DASHBOARD
                    self.led.off()
                    
                elif event == 'click_save':
                    self.save_result()
                    self.display.state = UIState.DASHBOARD
                    self.speaker.play_success()
                    
                # Test Events
                elif event == 'click_test_mode':
                    self.display.state = UIState.TEST_MENU
                    
                elif event == 'test_scale':
                    self.display.state = UIState.TEST_SCALE
                    
                elif event == 'test_cam':
                    self.display.state = UIState.TEST_CAMERA
                    # Kamera önizlemesini başlat
                    self.camera.start_preview()
                    
                elif event == 'test_spk':
                    self.display.state = UIState.TEST_SPEAKER
                    
                elif event == 'click_back':
                    # Kamera testinden çıkılıyorsa önizlemeyi durdur
                    if self.display.state == UIState.TEST_CAMERA:
                        self.camera.stop_preview()
                    
                    if self.display.state == UIState.TEST_MENU:
                        self.display.state = UIState.DASHBOARD
                    else:
                        self.display.state = UIState.TEST_MENU
                        
                elif event == 'click_play_sound':
                    self.speaker.play_beep()
                    time.sleep(0.5)
                    self.speaker.play_success()
                
        except KeyboardInterrupt:
            print("\nKapatılıyor...")
        
        finally:
            self.cleanup()
    
    def perform_scan(self, weight):
        """Tarama ve Analiz İşlemi"""
        # Ağırlık kontrolü (Opsiyonel: 0 olsa bile çalışsın istendi ama uyarı verebiliriz)
        if weight < 10:
            print("Uyarı: Ağırlık çok düşük")
            # Yine de devam ediyoruz, belki sadece görüntü istiyorlardır
            
        self.display.state = UIState.SCANNING
        self.display.show_camera_feed()
        self.led.white()
        self.speaker.play_beep()
        
        # Kamera Görüntüsü Al (Biraz gecikme efekti verilebilir)
        time.sleep(0.5) 
        image = self.camera.capture_image()
        
        self.display.state = UIState.ANALYZING
        self.display.show_analysis()
        self.led.blue()
        
        # AI Analizi
        food_key, confidence = self.recognizer.recognize(image)
        
        if not food_key:
            print("Yemek tanınamadı")
            self.led.yellow()
            self.speaker.play_warning()
            # Hata ekranı yerine, bilinmeyen olarak devam edebilir veya uyarı verebiliriz
            # Şimdilik Dashboard'a dönelim
            time.sleep(1)
            self.display.state = UIState.DASHBOARD
            self.led.off()
            return
            
        print(f"Tanınan: {food_key} (Weight: {weight}g)")
        
        # Besin Hesaplama
        nutrition = self.nutrition_calc.calculate(food_key, max(weight, 100)) # En az 100g baz alalım hesap için
        
        if nutrition:
            self.current_nutrition = nutrition
            
            # VKİ Kontrolü
            bmi = self.bmi_calc.calculate(self.current_user['weight'], self.current_user['height'])
            bmi_comment = self.bmi_calc.get_comment(bmi, self.current_user['age'])
            
            self.display.state = UIState.RESULT
            self.display.show_results(nutrition['name'], nutrition, bmi_comment)
            self.led.green()
        else:
            self.led.red()
            self.display.state = UIState.DASHBOARD
            
    def save_result(self):
        """Sonucu veritabanına kaydet"""
        if self.current_nutrition:
            self.db.add_measurement(
                user_id=1,
                food_name=self.current_nutrition['name'],
                weight=self.current_nutrition['weight'],
                nutrition=self.current_nutrition,
                bmi_data={'bmi': 0, 'comment': '-'}
            )
            print("Kayıt başarılı")

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
