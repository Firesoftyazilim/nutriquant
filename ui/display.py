# 4.3" Dokunmatik Ekran UI - Pygame
# Modern Nutriquant Interface

import pygame
import sys
import time
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, FPS, APP_NAME
from ui.keyboard import OnScreenKeyboard

# Renk Paleti (Modern & Premium)
COLORS = {
    'bg_dark': (20, 24, 30),      # Koyu Arka Plan
    'card_bg': (32, 38, 48),      # Kart Arka Planı
    'primary': (0, 122, 255),     # Canlı Mavi
    'primary_hover': (0, 100, 230),
    'accent': (255, 69, 58),      # Canlı Kırmızı (Accent)
    'success': (50, 215, 75),     # Yeşil
    'text_main': (255, 255, 255), # Beyaz Metin
    'text_sec': (160, 170, 180),  # Gri Metin
    'border': (60, 65, 75)        # Kenarlık
}

class UIState:
    SPLASH = -1
    DASHBOARD = 0
    SCANNING = 1
    ANALYZING = 2
    RESULT = 3
    ERROR = 4
    TEST_MENU = 5
    TEST_SCALE = 6
    TEST_CAMERA = 7
    TEST_SPEAKER = 8
    SETTINGS_MENU = 9  # Ayarlar menüsü
    WALLPAPER_SELECT = 10  # Arka plan seçimi
    PROFILE_ADD = 11
    PROFILE_EDIT = 12

class Display:
    def __init__(self, database=None):
        pygame.init()
        
        flags = pygame.FULLSCREEN if FULLSCREEN else 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        pygame.display.set_caption(APP_NAME)
        
        self.clock = pygame.time.Clock()
        self.db = database  # Database referansı
        
        # Fontlar
        try:
            # Sistem fontlarını dene, yoksa varsayılan
            self.font_xl = pygame.font.SysFont("segoeui", 64, bold=True)
            self.font_lg = pygame.font.SysFont("segoeui", 48, bold=True)
            self.font_md = pygame.font.SysFont("segoeui", 32)
            self.font_sm = pygame.font.SysFont("segoeui", 24)
        except:
            self.font_xl = pygame.font.Font(None, 80)
            self.font_lg = pygame.font.Font(None, 60)
            self.font_md = pygame.font.Font(None, 40)
            self.font_sm = pygame.font.Font(None, 28)
        
        # Logo yükle
        try:
            self.logo = pygame.image.load("assets/images/icon.png")
        except:
            print("[Uyarı] Logo yüklenemedi, varsayılan kullanılacak")
            self.logo = None
        
        # Settings icon yükle
        try:
            self.settings_icon = pygame.image.load("assets/images/icons/settings.png")
            self.settings_icon = pygame.transform.scale(self.settings_icon, (40, 40))
        except:
            print("[Uyarı] Settings icon yüklenemedi")
            self.settings_icon = None
        
        # Wallpaper'ları yükle
        self.wallpapers = {}
        self.wallpaper_names = []
        self.current_wallpaper = None
        self.load_wallpapers()
            
        self.state = UIState.SPLASH
        
        # Buton tanımları (Rect objeleri)
        self.btn_back = pygame.Rect(20, 20, 60, 40)
        self.btn_retry = pygame.Rect(SCREEN_WIDTH//2 - 140, 380, 130, 60)
        self.btn_save = pygame.Rect(SCREEN_WIDTH//2 + 10, 380, 130, 60)
        
        # Dashboard butonları
        self.btn_settings = pygame.Rect(20, 20, 50, 50)  # Sol üst - ayarlar
        self.btn_add_profile = pygame.Rect(SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 - 80, 160, 160)  # Ortada + butonu
        
        # Test Alanı Butonları
        self.btn_test_mode = pygame.Rect(SCREEN_WIDTH - 160, 20, 140, 50)
        
        self.btn_test_scale = pygame.Rect(SCREEN_WIDTH//2 - 240, 140, 220, 100)
        self.btn_test_cam = pygame.Rect(SCREEN_WIDTH//2 + 20, 140, 220, 100)
        self.btn_test_spk = pygame.Rect(SCREEN_WIDTH//2 - 240, 260, 220, 100)
        self.btn_test_back = pygame.Rect(SCREEN_WIDTH//2 + 20, 260, 220, 100)
        
        self.btn_spk_play = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 40, 200, 80)
        
        
        # Wallpaper seçim butonları (dinamik olarak oluşturulacak)
        self.wallpaper_buttons = []
        self.wallpaper_scroll_offset = 0  # Scroll pozisyonu
        self.wallpaper_scroll_max = 0  # Maksimum scroll
        
        # Profil yönetimi
        self.profile_buttons = []
        self.profile_form_data = {"name": "", "gender": "Erkek", "height": "", "weight": ""}
        self.active_input = None  # Hangi input aktif
        self.editing_profile_id = None  # Düzenlenen profil ID'si
        
        # Ekran klavyesi (dokunmatik ekran için)
        self.keyboard = OnScreenKeyboard(self.screen, self.font_md)
        
        # Dokunmatik scroll için
        self.touch_start_y = None
        self.touch_start_scroll = None

    def draw_rounded_rect(self, surface, color, rect, radius=15):
        """Köşeleri yuvarlatılmış dikdörtgen çiz"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def draw_card(self, x, y, w, h, title=None, value=None):
        """Bilgi kartı çiz"""
        rect = pygame.Rect(x, y, w, h)
        self.draw_rounded_rect(self.screen, COLORS['card_bg'], rect, 15)
        pygame.draw.rect(self.screen, COLORS['border'], rect, 2, border_radius=15)
        
        if title:
            text = self.font_sm.render(title, True, COLORS['text_sec'])
            self.screen.blit(text, (x + 20, y + 15))
            
        if value:
            text = self.font_lg.render(value, True, COLORS['text_main'])
            self.screen.blit(text, (x + 20, y + 50))

    def draw_button(self, rect, text, primary=True):
        """Modern buton çiz"""
        color = COLORS['primary'] if primary else COLORS['card_bg']
        hover_color = COLORS['primary_hover'] if primary else COLORS['border']
        
        # Basit hover efekti (mouse pozisyonuna göre)
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            self.draw_rounded_rect(self.screen, hover_color, rect, 20)
        else:
            self.draw_rounded_rect(self.screen, color, rect, 20)
            
        text_surf = self.font_md.render(text, True, COLORS['text_main'])
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
    
    def load_wallpapers(self):
        """Wallpaper'ları yükle"""
        import os
        from config import WALLPAPERS_DIR
        
        if not os.path.exists(WALLPAPERS_DIR):
            print(f"[Uyarı] Wallpaper klasörü bulunamadı: {WALLPAPERS_DIR}")
            return
        
        try:
            files = os.listdir(WALLPAPERS_DIR)
            for filename in files:
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    filepath = os.path.join(WALLPAPERS_DIR, filename)
                    try:
                        img = pygame.image.load(filepath)
                        # Ekran boyutuna ölçeklendir
                        img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                        self.wallpapers[filename] = img
                        self.wallpaper_names.append(filename)
                    except Exception as e:
                        print(f"[Uyarı] Wallpaper yüklenemedi {filename}: {e}")
            
            print(f"[Display] {len(self.wallpapers)} wallpaper yüklendi")
            
            # Kayıtlı arka planı yükle
            if self.db:
                saved_wallpaper = self.db.get_wallpaper()
                if saved_wallpaper and saved_wallpaper in self.wallpapers:
                    self.current_wallpaper = saved_wallpaper
                    print(f"[Display] Kayıtlı arka plan yüklendi: {saved_wallpaper}")
                elif saved_wallpaper is None:
                    self.current_wallpaper = None
                    print("[Display] Varsayılan arka plan kullanılıyor")
        except Exception as e:
            print(f"[Uyarı] Wallpaper yükleme hatası: {e}")
    
    def draw_background(self):
        """Arka plan çiz (wallpaper veya düz renk)"""
        if self.current_wallpaper and self.current_wallpaper in self.wallpapers:
            self.screen.blit(self.wallpapers[self.current_wallpaper], (0, 0))
        else:
            self.screen.fill(COLORS['bg_dark'])
    
    def set_wallpaper(self, wallpaper_name):
        """Wallpaper değiştir ve veritabanına kaydet"""
        if wallpaper_name in self.wallpapers:
            self.current_wallpaper = wallpaper_name
            print(f"[Display] Wallpaper değiştirildi: {wallpaper_name}")
        elif wallpaper_name is None:
            self.current_wallpaper = None
            print("[Display] Wallpaper kaldırıldı (varsayılan)")
        
        # Veritabanına kaydet
        if self.db:
            self.db.save_wallpaper(wallpaper_name)
            print(f"[Display] Wallpaper tercihi kaydedildi: {wallpaper_name}")


    def show_dashboard(self, battery, profiles, selected_profile_id=None):
        """Ana Dashboard Ekranı - Yeni Tasarım"""
        self.draw_background()
        
        # Sol üst - Settings ikonu
        if self.settings_icon:
            self.screen.blit(self.settings_icon, (25, 25))
        else:
            self.draw_button(self.btn_settings, "⚙", primary=False)
        
        # Sağ üst - Pil durumu (küçük)
        battery_color = COLORS['success'] if battery > 20 else COLORS['accent']
        battery_text = self.font_sm.render(f"🔋 %{battery}", True, COLORS['text_main'])
        self.screen.blit(battery_text, (SCREEN_WIDTH - 120, 30))
        
        # Ortada + Butonu (Profil Ekle)
        plus_rect = self.btn_add_profile
        self.draw_rounded_rect(self.screen, COLORS['card_bg'], plus_rect, 20)
        
        # Hover efekti
        mouse_pos = pygame.mouse.get_pos()
        if plus_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, COLORS['primary'], plus_rect, 4, border_radius=20)
        else:
            pygame.draw.rect(self.screen, COLORS['border'], plus_rect, 2, border_radius=20)
        
        # + işareti
        plus_text = self.font_xl.render("+", True, COLORS['primary'])
        plus_text_rect = plus_text.get_rect(center=plus_rect.center)
        self.screen.blit(plus_text, plus_text_rect)
        
        # Profil Listesi (+ butonunun yanında)
        self.profile_buttons = []
        if profiles:
            # Profilleri yatay olarak göster (+ butonunun sağında ve solunda)
            profile_size = 140
            spacing = 20
            start_x = plus_rect.right + spacing
            
            # Sağ taraftaki profiller
            for i, profile in enumerate(profiles[:3]):  # İlk 3 profil sağda
                x = start_x + i * (profile_size + spacing)
                y = plus_rect.y
                
                if x + profile_size > SCREEN_WIDTH - 20:
                    break
                
                rect = pygame.Rect(x, y, profile_size, profile_size)
                self.profile_buttons.append((profile, rect))
                
                # Seçili profil vurgusu
                is_selected = (profile['id'] == selected_profile_id)
                border_color = COLORS['primary'] if is_selected else COLORS['border']
                border_width = 4 if is_selected else 2
                
                self.draw_rounded_rect(self.screen, COLORS['card_bg'], rect, 15)
                pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=15)
                
                # Profil bilgileri
                name_text = self.font_md.render(profile['name'][:8], True, COLORS['text_main'])
                name_rect = name_text.get_rect(center=(rect.centerx, rect.centery - 20))
                self.screen.blit(name_text, name_rect)
                
                # Cinsiyet ikonu
                gender_icon = "♂" if profile['gender'] == 'Erkek' else "♀"
                gender_text = self.font_lg.render(gender_icon, True, COLORS['primary'])
                gender_rect = gender_text.get_rect(center=(rect.centerx, rect.centery + 20))
                self.screen.blit(gender_text, gender_rect)
            
            # Sol taraftaki profiller
            if len(profiles) > 3:
                for i, profile in enumerate(profiles[3:6]):  # 4-6. profiller solda
                    x = plus_rect.left - (i + 1) * (profile_size + spacing)
                    y = plus_rect.y
                    
                    if x < 20:
                        break
                    
                    rect = pygame.Rect(x, y, profile_size, profile_size)
                    self.profile_buttons.append((profile, rect))
                    
                    is_selected = (profile['id'] == selected_profile_id)
                    border_color = COLORS['primary'] if is_selected else COLORS['border']
                    border_width = 4 if is_selected else 2
                    
                    self.draw_rounded_rect(self.screen, COLORS['card_bg'], rect, 15)
                    pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=15)
                    
                    name_text = self.font_md.render(profile['name'][:8], True, COLORS['text_main'])
                    name_rect = name_text.get_rect(center=(rect.centerx, rect.centery - 20))
                    self.screen.blit(name_text, name_rect)
                    
                    gender_icon = "♂" if profile['gender'] == 'Erkek' else "♀"
                    gender_text = self.font_lg.render(gender_icon, True, COLORS['primary'])
                    gender_rect = gender_text.get_rect(center=(rect.centerx, rect.centery + 20))
                    self.screen.blit(gender_text, gender_rect)
        
        # Tarama butonu (profil seçiliyse)
        if selected_profile_id:
            scan_btn = pygame.Rect(SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT - 120, 240, 70)
            self.draw_button(scan_btn, "Yemeği Tara", primary=True)
            self.btn_scan = scan_btn
        
        # Alt bilgi
        if not profiles:
            info = self.font_sm.render("Başlamak için profil ekleyin", True, COLORS['text_sec'])
            self.screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, SCREEN_HEIGHT - 60))
        elif not selected_profile_id:
            info = self.font_sm.render("Profil seçin veya yeni profil ekleyin", True, COLORS['text_sec'])
            self.screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, SCREEN_HEIGHT - 60))
        else:
            info = self.font_sm.render("Uzun basarak profil düzenleyin", True, COLORS['text_sec'])
            self.screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, SCREEN_HEIGHT - 40))
        
        self.update()

    def show_camera_feed(self, image=None):
        """Kamera Önizleme"""
        self.screen.fill(COLORS['bg_dark'])
        
        # Kamera Çerçevesi
        cam_rect = pygame.Rect(40, 40, SCREEN_WIDTH-80, SCREEN_HEIGHT-80)
        pygame.draw.rect(self.screen, (0,0,0), cam_rect)
        pygame.draw.rect(self.screen, COLORS['primary'], cam_rect, 4, border_radius=10)
        
        if image is not None:
            # Numpy array (H, W, 3) -> Pygame Surface
            # Pygame surfarray expects (W, H, 3) generally, so we swap axes
            try:
                # image shape check
                if len(image.shape) == 3:
                     # Transpose for Pygame: (Height, Width, Colors) -> (Width, Height, Colors)
                    surf = pygame.surfarray.make_surface(image.swapaxes(0, 1))
                    surf = pygame.transform.scale(surf, (cam_rect.width, cam_rect.height))
                    self.screen.blit(surf, cam_rect)
            except Exception as e:
                print(f"Görüntü çizim hatası: {e}")
        
        text = self.font_md.render("Görüntü Testi (Çıkış için <)", True, COLORS['text_main'])
        self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT-60))
        
        self.draw_button(self.btn_back, "<", primary=False)
        
        self.update()
        
    def show_splash(self, progress):
        """Açılış ekranı - Logo animasyonu (800x480 için optimize edilmiş)
        progress: 0.0 - 1.0 arası animasyon ilerlemesi
        """
        self.screen.fill(COLORS['bg_dark'])
        
        if self.logo is None:
            # Logo yoksa sadece metin göster
            text = self.font_xl.render(APP_NAME, True, COLORS['primary'])
            self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 60))
            
            # Alt metin
            sub_text = self.font_md.render("Akıllı Yemek Tartısı", True, COLORS['text_sec'])
            self.screen.blit(sub_text, (SCREEN_WIDTH//2 - sub_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
        else:
            # Logo animasyonu - fade in + scale
            # Easing function: ease-out cubic
            eased_progress = 1 - pow(1 - progress, 3)
            
            # 800x480 için optimize edilmiş dikdörtgen logo boyutu
            # Genişlik: 600px, Yükseklik: 200px (3:1 oran)
            target_width = 600
            target_height = 200
            
            current_width = int(target_width * (0.7 + 0.3 * eased_progress))  # 70%'den başla, 100%'e git
            current_height = int(target_height * (0.7 + 0.3 * eased_progress))
            
            if current_width > 0 and current_height > 0:
                # Logo'yu dikdörtgen formatta ölçeklendir
                scaled_logo = pygame.transform.smoothscale(self.logo, (current_width, current_height))
                
                # Fade efekti
                alpha = int(255 * eased_progress)
                scaled_logo.set_alpha(alpha)
                
                # Logo'yu merkeze yerleştir (dikey olarak ortala)
                x = (SCREEN_WIDTH - current_width) // 2
                y = (SCREEN_HEIGHT - current_height) // 2
                
                self.screen.blit(scaled_logo, (x, y))
                
            
        
        self.update()

        
    def show_analysis(self):
        """Analiz Animasyonu"""
        self.screen.fill(COLORS['bg_dark'])
        
        text = self.font_xl.render("Yapay Zeka Analizi...", True, COLORS['primary'])
        self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 40))
        
        sub = self.font_sm.render("Besin değerleri hesaplanıyor", True, COLORS['text_sec'])
        self.screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, SCREEN_HEIGHT//2 + 40))
        
        self.update()

        self.update()

    def show_test_menu(self):
        """Donanım Test Menüsü"""
        self.screen.fill(COLORS['bg_dark'])
        
        title = self.font_lg.render("Donanım Testi", True, COLORS['text_main'])
        self.screen.blit(title, (40, 40))
        
        self.draw_button(self.btn_test_scale, "Tartı Testi", primary=False)
        self.draw_button(self.btn_test_cam, "Kamera Testi", primary=False)
        self.draw_button(self.btn_test_spk, "Hoparlör Testi", primary=False)
        self.draw_button(self.btn_test_back, "Geri Dön", primary=True)
        
        self.update()
        
    def show_test_scale(self, weight):
        """Tartı Test Ekranı"""
        self.screen.fill(COLORS['bg_dark'])

        self.draw_button(self.btn_back, "<", primary=False)
        
        title = self.font_lg.render("Tartı Testi", True, COLORS['text_main'])
        self.screen.blit(title, (100, 20))
        
        # Büyük Ağırlık Göstergesi
        w_text = self.font_xl.render(f"{weight} g", True, COLORS['primary'])
        self.screen.blit(w_text, (SCREEN_WIDTH//2 - w_text.get_width()//2, SCREEN_HEIGHT//2 - 40))
        
        info = self.font_sm.render("Sensör üzerine nesne koyun", True, COLORS['text_sec'])
        self.screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, SCREEN_HEIGHT//2 + 60))
        
        self.update()

    def show_test_speaker(self):
        """Hoparlör Test Ekranı"""
        self.screen.fill(COLORS['bg_dark'])
        
        self.draw_button(self.btn_back, "<", primary=False)
        
        title = self.font_lg.render("Hoparlör Testi", True, COLORS['text_main'])
        self.screen.blit(title, (100, 20))
        
        self.draw_button(self.btn_spk_play, "Ses Çal", primary=True)
        
        self.update()
        
    def show_settings_menu(self):
        """Ayarlar Menüsü - Ana Dialog"""
        self.draw_background()
        
        self.draw_button(self.btn_back, "<", primary=False)
        
        title = self.font_lg.render("Ayarlar", True, COLORS['text_main'])
        self.screen.blit(title, (100, 20))
        
        # Ayar seçenekleri
        menu_items = [
            ("Arka Plan Değiştir", "wallpaper"),
            ("Test Modu", "test"),
            # İleride eklenebilir: ("Ses Ayarları", "sound"), ("Ekran Parlaklığı", "brightness")
        ]
        
        # Menü kartları
        card_width = 700
        card_height = 80
        start_y = 120
        spacing = 20
        
        self.settings_menu_buttons = []
        
        for idx, (label, action) in enumerate(menu_items):
            y = start_y + idx * (card_height + spacing)
            x = (SCREEN_WIDTH - card_width) // 2
            
            rect = pygame.Rect(x, y, card_width, card_height)
            self.settings_menu_buttons.append((action, rect))
            
            # Kart arka planı
            self.draw_rounded_rect(self.screen, COLORS['card_bg'], rect, 15)
            pygame.draw.rect(self.screen, COLORS['border'], rect, 2, border_radius=15)
            
            # Metin
            text = self.font_md.render(label, True, COLORS['text_main'])
            text_rect = text.get_rect(midleft=(x + 30, rect.centery))
            self.screen.blit(text, text_rect)
            
            # Ok işareti
            arrow = self.font_md.render("→", True, COLORS['text_sec'])
            arrow_rect = arrow.get_rect(midright=(rect.right - 30, rect.centery))
            self.screen.blit(arrow, arrow_rect)
        
        self.update()
    
    def show_wallpaper_select(self):
        """Arka Plan Seçimi - Scroll Destekli"""
        self.draw_background()
        
        self.draw_button(self.btn_back, "<", primary=False)
        
        title = self.font_lg.render("Arka Plan Seçimi", True, COLORS['text_main'])
        self.screen.blit(title, (100, 20))
        
        # Wallpaper listesi
        all_items = [None] + self.wallpaper_names
        
        # Grid ayarları
        start_y = 100
        col_width = 240
        row_height = 120  # İsim olmadan daha küçük
        cols = 3
        margin_x = 30
        
        # Scroll alanı
        scroll_area_y = 80
        scroll_area_height = SCREEN_HEIGHT - scroll_area_y
        
        # Toplam içerik yüksekliği
        total_rows = (len(all_items) + cols - 1) // cols
        total_content_height = total_rows * row_height
        
        # Maksimum scroll
        self.wallpaper_scroll_max = max(0, total_content_height - scroll_area_height + 100)
        
        # Scroll sınırla
        self.wallpaper_scroll_offset = max(0, min(self.wallpaper_scroll_offset, self.wallpaper_scroll_max))
        
        # Wallpaper butonları
        self.wallpaper_buttons = []
        
        for idx, item in enumerate(all_items):
            row = idx // cols
            col = idx % cols
            x = margin_x + col * col_width
            y = start_y + row * row_height - self.wallpaper_scroll_offset
            
            # Ekran dışındaysa çizme
            if y + row_height < scroll_area_y or y > SCREEN_HEIGHT:
                continue
            
            rect = pygame.Rect(x, y, col_width - 20, row_height - 20)
            self.wallpaper_buttons.append((item, rect))
            
            # Seçili mi?
            is_selected = (item == self.current_wallpaper)
            border_color = COLORS['primary'] if is_selected else COLORS['border']
            border_width = 4 if is_selected else 2
            
            # Çizim
            if item and item in self.wallpapers:
                # Wallpaper Thumbnail
                thumb = pygame.transform.scale(self.wallpapers[item], (rect.width, rect.height))
                self.screen.blit(thumb, rect)
            else:
                # "Varsayılan" Kutusu
                pygame.draw.rect(self.screen, COLORS['card_bg'], rect, border_radius=10)
                text = self.font_sm.render("Varsayılan", True, COLORS['text_sec'])
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
            
            # Çerçeve
            pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=10)
        
        # Scroll göstergesi (sağ tarafta)
        if self.wallpaper_scroll_max > 0:
            scrollbar_height = 200
            scrollbar_y = scroll_area_y + 20
            scrollbar_x = SCREEN_WIDTH - 15
            
            # Scrollbar arka plan
            pygame.draw.rect(self.screen, COLORS['border'], 
                           (scrollbar_x, scrollbar_y, 8, scrollbar_height), border_radius=4)
            
            # Scrollbar thumb
            thumb_height = max(30, scrollbar_height * scroll_area_height / total_content_height)
            thumb_y = scrollbar_y + (scrollbar_height - thumb_height) * (self.wallpaper_scroll_offset / self.wallpaper_scroll_max)
            pygame.draw.rect(self.screen, COLORS['primary'], 
                           (scrollbar_x, thumb_y, 8, thumb_height), border_radius=4)
        
        self.update()
        
    def show_results(self, food_name, nutrition, bmi_status):
        """Sonuç Ekranı"""
        self.screen.fill(COLORS['bg_dark'])
        
        # Yemek Adı (Başlık)
        title = self.font_xl.render(food_name, True, COLORS['primary'])
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 40))
        
        # Besin Değerleri Grid
        grid_y = 120
        grid_gap = 20
        card_w = 170
        
        # Kalori (Büyük)
        self.draw_card(SCREEN_WIDTH//2 - 90, grid_y, 180, 100, "Kalori", f"{nutrition['calorie']} kcal")
        
        # Detaylar
        row2_y = grid_y + 120
        self.draw_card(SCREEN_WIDTH//2 - 250, row2_y, 160, 90, "Protein", f"{nutrition['protein']}g")
        self.draw_card(SCREEN_WIDTH//2 - 80, row2_y, 160, 90, "Karb.", f"{nutrition['carb']}g")
        self.draw_card(SCREEN_WIDTH//2 + 90, row2_y, 160, 90, "Yağ", f"{nutrition['fat']}g")
        
        # Aksiyon Butonları
        self.draw_button(self.btn_retry, "Tekrar", primary=False)
        self.draw_button(self.btn_save, "Kaydet", primary=True)
        
        self.update()
    
    def show_profile_form(self, is_edit=False):
        """Profil Ekleme/Düzenleme Formu"""
        self.screen.fill(COLORS['bg_dark'])
        
        # Geri butonu
        self.draw_button(self.btn_back, "<", primary=False)
        
        # Başlık
        title_text = "Profil Düzenle" if is_edit else "Yeni Profil"
        title = self.font_lg.render(title_text, True, COLORS['text_main'])
        self.screen.blit(title, (100, 20))
        
        # Form alanları
        form_x = 150
        form_y = 100
        field_height = 60
        field_spacing = 70
        
        # İsim
        name_rect = pygame.Rect(form_x, form_y, 500, field_height)
        self.draw_input_field(name_rect, "İsim", self.profile_form_data['name'], self.active_input == 'name')
        
        # Cinsiyet (Butonlar)
        gender_y = form_y + field_spacing
        gender_label = self.font_md.render("Cinsiyet:", True, COLORS['text_sec'])
        self.screen.blit(gender_label, (form_x, gender_y + 15))
        
        btn_male = pygame.Rect(form_x + 150, gender_y, 150, field_height)
        btn_female = pygame.Rect(form_x + 320, gender_y, 150, field_height)
        
        # Erkek butonu
        is_male = self.profile_form_data['gender'] == 'Erkek'
        self.draw_rounded_rect(self.screen, COLORS['primary'] if is_male else COLORS['card_bg'], btn_male, 15)
        male_text = self.font_md.render("♂ Erkek", True, COLORS['text_main'])
        male_rect = male_text.get_rect(center=btn_male.center)
        self.screen.blit(male_text, male_rect)
        
        # Kadın butonu
        is_female = self.profile_form_data['gender'] == 'Kadın'
        self.draw_rounded_rect(self.screen, COLORS['primary'] if is_female else COLORS['card_bg'], btn_female, 15)
        female_text = self.font_md.render("♀ Kadın", True, COLORS['text_main'])
        female_rect = female_text.get_rect(center=btn_female.center)
        self.screen.blit(female_text, female_rect)
        
        # Boy
        height_y = gender_y + field_spacing
        height_rect = pygame.Rect(form_x, height_y, 240, field_height)
        self.draw_input_field(height_rect, "Boy (cm)", self.profile_form_data['height'], self.active_input == 'height')
        
        # Kilo
        weight_rect = pygame.Rect(form_x + 260, height_y, 240, field_height)
        self.draw_input_field(weight_rect, "Kilo (kg)", self.profile_form_data['weight'], self.active_input == 'weight')
        
        # Kaydet butonu
        save_btn = pygame.Rect(SCREEN_WIDTH//2 - 100, height_y + 90, 200, 60)
        self.draw_button(save_btn, "Kaydet", primary=True)
        
        # Sil butonu (sadece düzenleme modunda)
        if is_edit:
            delete_btn = pygame.Rect(SCREEN_WIDTH//2 - 100, height_y + 160, 200, 50)
            self.draw_button(delete_btn, "Sil", primary=False)
        
        # Butonları sakla (event handling için)
        self.form_buttons = {
            'name': name_rect,
            'height': height_rect,
            'weight': weight_rect,
            'male': btn_male,
            'female': btn_female,
            'save': save_btn
        }
        
        if is_edit:
            self.form_buttons['delete'] = delete_btn
        
        # Ekran klavyesini göster (aktif input varsa)
        if self.active_input:
            if self.active_input in ['height', 'weight']:
                self.keyboard.show('number')
            else:
                self.keyboard.show('text')
        else:
            self.keyboard.hide()
        
        # Klavyeyi çiz
        self.keyboard.draw()
        
        self.update()
    
    def draw_input_field(self, rect, label, value, is_active):
        """Input alanı çiz"""
        # Arka plan
        bg_color = COLORS['primary'] if is_active else COLORS['card_bg']
        self.draw_rounded_rect(self.screen, bg_color, rect, 10)
        
        if not is_active:
            pygame.draw.rect(self.screen, COLORS['border'], rect, 2, border_radius=10)
        
        # Label (küçük, üstte)
        label_text = self.font_sm.render(label, True, COLORS['text_sec'])
        self.screen.blit(label_text, (rect.x + 15, rect.y + 8))
        
        # Value (büyük, altta)
        value_text = self.font_md.render(value if value else "", True, COLORS['text_main'])
        self.screen.blit(value_text, (rect.x + 15, rect.y + 30))
        
        # Cursor (aktif ise)
        if is_active:
            cursor_x = rect.x + 15 + value_text.get_width() + 5
            pygame.draw.line(self.screen, COLORS['text_main'], (cursor_x, rect.y + 30), (cursor_x, rect.y + 50), 2)

    def clear(self):
        self.screen.fill(COLORS['bg_dark'])

    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'quit'
                # Fiziksel klavye desteği kaldırıldı - Dokunmatik ekran klavyesi kullanılıyor
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                
                # Dokunmatik scroll başlangıcı (wallpaper seçiminde)
                if self.state == UIState.WALLPAPER_SELECT:
                    self.touch_start_y = pos[1]
                    self.touch_start_scroll = self.wallpaper_scroll_offset
                
                if self.state == UIState.DASHBOARD:
                    # + Butonu (Profil ekle)
                    if self.btn_add_profile.collidepoint(pos):
                        return 'click_add_profile'
                    # Settings butonu
                    elif self.btn_settings.collidepoint(pos):
                        return 'click_settings'
                    # Scan butonu (profil seçiliyse)
                    elif hasattr(self, 'btn_scan') and self.btn_scan.collidepoint(pos):
                        return 'click_scan'
                    # Profil seçimi
                    else:
                        for profile, rect in self.profile_buttons:
                            if rect.collidepoint(pos):
                                # Sol tık: seçim, Sağ tık: düzenleme
                                if event.button == 1:  # Sol tık
                                    return ('select_profile', profile['id'])
                                elif event.button == 3:  # Sağ tık
                                    return ('edit_profile', profile['id'])
                
                elif self.state in [UIState.PROFILE_ADD, UIState.PROFILE_EDIT]:
                    # Önce klavye tıklamasını kontrol et
                    if self.keyboard.visible:
                        key = self.keyboard.handle_click(pos)
                        if key:
                            if key == '✓':
                                # Klavyeyi kapat
                                self.active_input = None
                                self.keyboard.hide()
                            elif key == '←':
                                # Backspace
                                if self.active_input:
                                    self.profile_form_data[self.active_input] = self.profile_form_data[self.active_input][:-1]
                            elif key == ' ':
                                # Boşluk
                                if self.active_input:
                                    self.profile_form_data[self.active_input] += ' '
                            else:
                                # Normal karakter
                                if self.active_input:
                                    self.profile_form_data[self.active_input] += key
                            return None  # Klavye işlendi, başka işlem yapma
                    
                    # Geri butonu
                    if self.btn_back.collidepoint(pos):
                        self.keyboard.hide()
                        return 'click_back'
                    
                    # Form butonları
                    if hasattr(self, 'form_buttons'):
                        if self.form_buttons['name'].collidepoint(pos):
                            self.active_input = 'name'
                        elif self.form_buttons['height'].collidepoint(pos):
                            self.active_input = 'height'
                        elif self.form_buttons['weight'].collidepoint(pos):
                            self.active_input = 'weight'
                        elif self.form_buttons['male'].collidepoint(pos):
                            self.profile_form_data['gender'] = 'Erkek'
                        elif self.form_buttons['female'].collidepoint(pos):
                            self.profile_form_data['gender'] = 'Kadın'
                        elif self.form_buttons['save'].collidepoint(pos):
                            self.keyboard.hide()
                            return 'save_profile'
                        elif 'delete' in self.form_buttons and self.form_buttons['delete'].collidepoint(pos):
                            self.keyboard.hide()
                            return 'delete_profile'
                
                elif self.state == UIState.SETTINGS_MENU:
                    # Geri butonu
                    if self.btn_back.collidepoint(pos):
                        return 'click_back'
                    
                    # Menü seçenekleri
                    if hasattr(self, 'settings_menu_buttons'):
                        for action, rect in self.settings_menu_buttons:
                            if rect.collidepoint(pos):
                                return f'settings_{action}'
                
                elif self.state == UIState.WALLPAPER_SELECT:
                    # Geri butonu
                    if self.btn_back.collidepoint(pos):
                        return 'click_back'
                    
                    # Wallpaper seçimi
                    for wp_name, rect in self.wallpaper_buttons:
                        if rect.collidepoint(pos):
                            return f"select_wallpaper_{wp_name}" if wp_name else "select_wallpaper_none"
            
            elif event.type == pygame.MOUSEMOTION:
                # Dokunmatik sürükleme (scroll)
                if self.state == UIState.WALLPAPER_SELECT and self.touch_start_y is not None:
                    pos = event.pos
                    delta_y = self.touch_start_y - pos[1]
                    self.wallpaper_scroll_offset = self.touch_start_scroll + delta_y
                    self.wallpaper_scroll_offset = max(0, min(self.wallpaper_scroll_offset, self.wallpaper_scroll_max))
            
            elif event.type == pygame.MOUSEBUTTONUP:
                # Dokunmatik scroll bitişi
                if self.state == UIState.WALLPAPER_SELECT:
                    self.touch_start_y = None
                    self.touch_start_scroll = None
            
            elif event.type == pygame.MOUSEWHEEL:
                # Scroll desteği (wallpaper seçiminde - mouse wheel için)
                if self.state == UIState.WALLPAPER_SELECT:
                    scroll_amount = event.y * 30  # Scroll hızı
                    self.wallpaper_scroll_offset -= scroll_amount
                    self.wallpaper_scroll_offset = max(0, min(self.wallpaper_scroll_offset, self.wallpaper_scroll_max))
                
                elif self.state == UIState.TEST_MENU:
                    if self.btn_test_scale.collidepoint(pos):
                        return 'test_scale'
                    elif self.btn_test_cam.collidepoint(pos):
                        return 'test_cam'
                    elif self.btn_test_spk.collidepoint(pos):
                        return 'test_spk'
                    elif self.btn_test_back.collidepoint(pos):
                        return 'click_back'
                        
                elif self.state in [UIState.TEST_SCALE, UIState.TEST_CAMERA, UIState.TEST_SPEAKER]:
                    if self.btn_back.collidepoint(pos):
                        return 'click_back'
                    # Speaker özel durum
                    if self.state == UIState.TEST_SPEAKER and self.btn_spk_play.collidepoint(pos):
                        return 'click_play_sound'
                        
                elif self.state == UIState.RESULT:
                    if self.btn_retry.collidepoint(pos):
                        return 'click_retry'
                    elif self.btn_save.collidepoint(pos):
                        return 'click_save'
        return None

    def cleanup(self):
        pygame.quit()

# Test Bloğu
if __name__ == "__main__":
    display = Display()
    display.show_dashboard(0, 85)
    time.sleep(2)
    display.show_analysis()
    time.sleep(2)
    nutri = {'calorie': 320, 'protein': 25, 'carb': 45, 'fat': 12}
    display.show_results("Izgara Tavuk", nutri, "Normal")
    time.sleep(3)
    display.cleanup()
