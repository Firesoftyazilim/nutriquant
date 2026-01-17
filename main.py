# Nutriquant - Ana Uygulama
# Raspberry Pi 4 - Akıllı Yemek Tartısı
# v2.0 - Dashboard ve Manuel Kontrol

import time
import sys
import pygame
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
        
        self.current_user = self.load_default_user()
        self.current_nutrition = None # Son ölçüm sonucu
        self.selected_profile_id = None  # Seçili profil ID
        self.profiles = []  # Profil listesi
        
        # Açılış animasyonu ve müzik
        self.show_splash_animation()
        
        print("Sistem hazır!")
        self.speaker.play_ready()
        self.led.green()
        time.sleep(1)
        self.led.off()
    
    def show_splash_animation(self):
        """Açılış ekranı animasyonu göster"""
        # Müziği başlat
        self.speaker.play_startup_music()
        
        # 2 saniye animasyon
        animation_duration = 2.0  # saniye
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            progress = min(elapsed / animation_duration, 1.0)
            
            # Animasyonu göster
            self.display.show_splash(progress)
            
            # Tamamlandıysa çık
            if progress >= 1.0:
                break
            
            # Çıkış tuşlarını kontrol et (opsiyonel)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return
            
            time.sleep(0.016)  # ~60 FPS
        
        # Dashboard'a geç
        self.display.state = UIState.DASHBOARD
    
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
                battery_percent = self.battery.get_percentage()
                
                # 2. Profilleri yükle
                self.profiles = self.db.get_all_profiles()
                
                # 3. UI Durumuna Göre Çizim Yap
                if self.display.state == UIState.DASHBOARD:
                    self.display.show_dashboard(battery_percent, self.profiles, self.selected_profile_id)
                
                elif self.display.state == UIState.PROFILE_ADD:
                    self.display.show_profile_form(is_edit=False)
                
                elif self.display.state == UIState.PROFILE_EDIT:
                    self.display.show_profile_form(is_edit=True)
                
                elif self.display.state == UIState.TEST_MENU:
                    self.display.show_test_menu()
                    
                elif self.display.state == UIState.TEST_SCALE:
                    weight = self.scale.read_weight()
                    self.display.show_test_scale(weight)
                    
                elif self.display.state == UIState.TEST_SPEAKER:
                    self.display.show_test_speaker()
                    
                elif self.display.state == UIState.TEST_CAMERA:
                    # Kamera test modunda sadece UI göster, rpicam-vid arka planda çalışıyor
                    self.display.show_camera_feed()
                    
                elif self.display.state == UIState.SETTINGS:
                    self.display.show_settings()

                    
                # 4. Olayları Dinle
                event = self.display.handle_events()
                
                if event == 'quit':
                    break
                
                elif event == 'click_add_profile':
                    # Profil ekleme formunu aç
                    self.display.profile_form_data = {"name": "", "gender": "Erkek", "height": "", "weight": ""}
                    self.display.active_input = None
                    self.display.editing_profile_id = None
                    self.display.state = UIState.PROFILE_ADD
                
                elif isinstance(event, tuple) and event[0] == 'select_profile':
                    # Profil seçildi
                    profile_id = event[1]
                    self.selected_profile_id = profile_id
                    print(f"Profil seçildi: {profile_id}")
                
                elif isinstance(event, tuple) and event[0] == 'edit_profile':
                    # Profil düzenleme
                    profile_id = event[1]
                    profile = next((p for p in self.profiles if p['id'] == profile_id), None)
                    if profile:
                        self.display.profile_form_data = {
                            "name": profile['name'],
                            "gender": profile['gender'],
                            "height": str(profile['height']),
                            "weight": str(profile['weight'])
                        }
                        self.display.active_input = None
                        self.display.editing_profile_id = profile_id
                        self.display.state = UIState.PROFILE_EDIT
                
                elif event == 'click_scan':
                    # Tarama başlat (profil seçiliyse)
                    if self.selected_profile_id:
                        weight = self.scale.read_weight()
                        self.perform_scan(weight)
                
                elif event == 'save_profile':
                    # Profil kaydet
                    self.save_profile()
                
                elif event == 'delete_profile':
                    # Profil sil
                    if self.display.editing_profile_id:
                        self.db.delete_profile(self.display.editing_profile_id)
                        if self.selected_profile_id == self.display.editing_profile_id:
                            self.selected_profile_id = None
                        self.display.state = UIState.DASHBOARD
                        self.speaker.play_success()
                    
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
                    
                elif event == 'click_settings':
                    self.display.state = UIState.SETTINGS
                    
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
                    
                    # Profil formlarından çıkış
                    if self.display.state in [UIState.PROFILE_ADD, UIState.PROFILE_EDIT]:
                        self.display.state = UIState.DASHBOARD
                    elif self.display.state == UIState.SETTINGS:
                        self.display.state = UIState.DASHBOARD
                    elif self.display.state == UIState.TEST_MENU:
                        self.display.state = UIState.DASHBOARD
                    else:
                        self.display.state = UIState.TEST_MENU
                        
                elif event and event.startswith('select_wallpaper_'):
                    print(f"[Debug] Main event yakalandı: {event}")
                    wp_name = event.replace('select_wallpaper_', '')
                    if wp_name == 'none':
                        self.display.set_wallpaper(None)
                    else:
                        self.display.set_wallpaper(wp_name)
                        
                elif event == 'click_play_sound':
                    self.speaker.play_beep()
                    time.sleep(0.5)
                    self.speaker.play_success()
                
        except KeyboardInterrupt:
            print("\nKapatılıyor...")
        
        finally:
            self.cleanup()
    
    def save_profile(self):
        """Profil kaydet (yeni veya güncelleme)"""
        form_data = self.display.profile_form_data
        
        # Validasyon
        if not form_data['name'] or not form_data['height'] or not form_data['weight']:
            print("Hata: Tüm alanları doldurun")
            return
        
        try:
            height = int(form_data['height'])
            weight = int(form_data['weight'])
        except ValueError:
            print("Hata: Boy ve kilo sayı olmalı")
            return
        
        if self.display.editing_profile_id:
            # Güncelleme
            self.db.update_profile(
                self.display.editing_profile_id,
                form_data['name'],
                form_data['gender'],
                height,
                weight
            )
            print(f"Profil güncellendi: {form_data['name']}")
        else:
            # Yeni profil
            profile = self.db.add_profile(
                form_data['name'],
                form_data['gender'],
                height,
                weight
            )
            print(f"Yeni profil eklendi: {form_data['name']}")
            self.selected_profile_id = profile['id']
        
        self.display.state = UIState.DASHBOARD
        self.speaker.play_success()
    
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
