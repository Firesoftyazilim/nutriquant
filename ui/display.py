# 4.3" Dokunmatik Ekran UI - Pygame
# Modern Nutriquant Interface

import pygame
import sys
import time
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, FPS, APP_NAME

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
    SETTINGS = 9

class Display:
    def __init__(self):
        pygame.init()
        
        flags = pygame.FULLSCREEN if FULLSCREEN else 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        pygame.display.set_caption(APP_NAME)
        
        self.clock = pygame.time.Clock()
        
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
        
        # Wallpaper'ları yükle
        self.wallpapers = {}
        self.wallpaper_names = []
        self.current_wallpaper = None
        self.load_wallpapers()
            
        self.state = UIState.SPLASH
        
        # Buton tanımları (Rect objeleri)
        self.btn_scan = pygame.Rect(SCREEN_WIDTH//2 - 120, 280, 240, 80)
        self.btn_back = pygame.Rect(20, 20, 60, 40)
        self.btn_retry = pygame.Rect(SCREEN_WIDTH//2 - 140, 380, 130, 60)
        self.btn_save = pygame.Rect(SCREEN_WIDTH//2 + 10, 380, 130, 60)
        
        # Ayarlar butonu (sol üst)
        self.btn_settings = pygame.Rect(20, 20, 50, 50)
        
        # Test Alanı Butonları
        self.btn_test_mode = pygame.Rect(SCREEN_WIDTH - 160, 20, 140, 50)
        
        self.btn_test_scale = pygame.Rect(SCREEN_WIDTH//2 - 240, 140, 220, 100)
        self.btn_test_cam = pygame.Rect(SCREEN_WIDTH//2 + 20, 140, 220, 100)
        self.btn_test_spk = pygame.Rect(SCREEN_WIDTH//2 - 240, 260, 220, 100)
        self.btn_test_back = pygame.Rect(SCREEN_WIDTH//2 + 20, 260, 220, 100)
        
        self.btn_spk_play = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 40, 200, 80)
        
        # Wallpaper seçim butonları (dinamik olarak oluşturulacak)
        self.wallpaper_buttons = []

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
        except Exception as e:
            print(f"[Uyarı] Wallpaper yükleme hatası: {e}")
    
    def draw_background(self):
        """Arka plan çiz (wallpaper veya düz renk)"""
        if self.current_wallpaper and self.current_wallpaper in self.wallpapers:
            self.screen.blit(self.wallpapers[self.current_wallpaper], (0, 0))
        else:
            self.screen.fill(COLORS['bg_dark'])
    
    def set_wallpaper(self, wallpaper_name):
        """Wallpaper değiştir"""
        if wallpaper_name in self.wallpapers:
            self.current_wallpaper = wallpaper_name
            print(f"[Display] Wallpaper değiştirildi: {wallpaper_name}")
        elif wallpaper_name is None:
            self.current_wallpaper = None
            print("[Display] Wallpaper kaldırıldı")


    def show_dashboard(self, weight, battery):
        """Ana Dashboard Ekranı"""
        self.draw_background()
        
        # Başlık
        title = self.font_lg.render(f"Merhaba, {APP_NAME}", True, COLORS['text_main'])
        self.screen.blit(title, (90, 40))
        
        # Ayarlar butonu (sol üst - dişli ikonu)
        self.draw_button(self.btn_settings, "⚙", primary=False)
        
        # Üst Bilgi Kartları
        self.draw_card(30, 120, 220, 120, "Anlık Ağırlık", f"{weight}g")
        
        # Pil Durumu (Basit grafik)
        pil_color = COLORS['success'] if battery > 20 else COLORS['accent']
        self.draw_card(270, 120, 220, 120, "Pil Durumu", f"%{battery}")
        pygame.draw.rect(self.screen, COLORS['bg_dark'], (430, 140, 40, 20), border_radius=3)
        pygame.draw.rect(self.screen, pil_color, (432, 142, 36 * (battery/100), 16), border_radius=2)

        # Büyük Tara Butonu
        self.draw_button(self.btn_scan, "Yemeği Tara", primary=True)
        
        # Test Modu Butonu (Sağ Üst)
        self.draw_button(self.btn_test_mode, "Test Modu", primary=False)
        
        # Alt Bilgi
        info = self.font_sm.render("Tabağı yerleştirin ve tarama başlatın", True, COLORS['text_sec'])
        self.screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, 400))
        
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
        """Açılış ekranı - Logo animasyonu
        progress: 0.0 - 1.0 arası animasyon ilerlemesi
        """
        self.screen.fill(COLORS['bg_dark'])
        
        if self.logo is None:
            # Logo yoksa sadece metin göster
            text = self.font_xl.render(APP_NAME, True, COLORS['primary'])
            self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 40))
        else:
            # Logo animasyonu - küçükten büyüğe
            # Easing function: ease-out cubic
            eased_progress = 1 - pow(1 - progress, 3)
            
            # Hedef boyut (ekranın %60'ı)
            target_size = min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.6
            current_size = int(target_size * eased_progress)
            
            if current_size > 0:
                # Logo'yu ölçeklendir
                scaled_logo = pygame.transform.smoothscale(self.logo, (current_size, current_size))
                
                # Merkeze yerleştir
                x = (SCREEN_WIDTH - current_size) // 2
                y = (SCREEN_HEIGHT - current_size) // 2
                
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
        self.draw_button(self.btn_back, "<", primary=False)
        
        title = self.font_lg.render("Arka Plan Seçimi", True, COLORS['text_main'])
        self.screen.blit(title, (100, 20))
        
        # Wallpaper grid
        start_y = 100
        col_width = 240
        row_height = 160
        cols = 3
        
        # Butonları oluştur
        self.wallpaper_buttons = []
        
        # "Wallpaper Yok" seçeneği
        no_wp_rect = pygame.Rect(30, start_y, col_width - 20, row_height - 20)
        self.wallpaper_buttons.append((None, no_wp_rect))
        
        # Wallpaper'ları göster
        for idx, wp_name in enumerate(self.wallpaper_names, 1):
            row = idx // cols
            col = idx % cols
            x = 30 + col * col_width
            y = start_y + row * row_height
            
            rect = pygame.Rect(x, y, col_width - 20, row_height - 20)
            self.wallpaper_buttons.append((wp_name, rect))
        
        # Butonları çiz
        for wp_name, rect in self.wallpaper_buttons:
            # Seçili mi kontrol et
            is_selected = (wp_name == self.current_wallpaper)
            border_color = COLORS['primary'] if is_selected else COLORS['border']
            
            # Arka plan
            if wp_name and wp_name in self.wallpapers:
                # Thumbnail göster
                thumbnail = pygame.transform.scale(self.wallpapers[wp_name], (rect.width, rect.height))
                self.screen.blit(thumbnail, rect)
            else:
                # "Wallpaper Yok" kutusu
                pygame.draw.rect(self.screen, COLORS['card_bg'], rect, border_radius=10)
                text = self.font_sm.render("Wallpaper Yok", True, COLORS['text_sec'])
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
            
            # Kenarlık
            pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=10)
        
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if self.state == UIState.DASHBOARD:
                    if self.btn_scan.collidepoint(pos):
                        return 'click_scan'
                    elif self.btn_test_mode.collidepoint(pos):
                        return 'click_test_mode'
                
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
