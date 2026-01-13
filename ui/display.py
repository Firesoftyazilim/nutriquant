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
    DASHBOARD = 0
    SCANNING = 1
    ANALYZING = 2
    RESULT = 3
    ERROR = 4

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
            
        self.state = UIState.DASHBOARD
        
        # Buton tanımları (Rect objeleri)
        self.btn_scan = pygame.Rect(SCREEN_WIDTH//2 - 120, 280, 240, 80)
        self.btn_back = pygame.Rect(20, 20, 60, 40)
        self.btn_retry = pygame.Rect(SCREEN_WIDTH//2 - 140, 380, 130, 60)
        self.btn_save = pygame.Rect(SCREEN_WIDTH//2 + 10, 380, 130, 60)

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

    def show_dashboard(self, weight, battery):
        """Ana Dashboard Ekranı"""
        self.screen.fill(COLORS['bg_dark'])
        
        # Başlık
        title = self.font_lg.render(f"Merhaba, {APP_NAME}", True, COLORS['text_main'])
        self.screen.blit(title, (30, 40))
        
        # Üst Bilgi Kartları
        self.draw_card(30, 120, 220, 120, "Anlık Ağırlık", f"{weight}g")
        
        # Pil Durumu (Basit grafik)
        pil_color = COLORS['success'] if battery > 20 else COLORS['accent']
        self.draw_card(270, 120, 220, 120, "Pil Durumu", f"%{battery}")
        pygame.draw.rect(self.screen, COLORS['bg_dark'], (430, 140, 40, 20), border_radius=3)
        pygame.draw.rect(self.screen, pil_color, (432, 142, 36 * (battery/100), 16), border_radius=2)

        # Büyük Tara Butonu
        self.draw_button(self.btn_scan, "Yemeği Tara", primary=True)
        
        # Alt Bilgi
        info = self.font_sm.render("Tabağı yerleştirin ve tarama başlatın", True, COLORS['text_sec'])
        self.screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, 400))
        
        self.update()

    def show_camera_feed(self):
        """Kamera Önizleme (Simüle edilmiş)"""
        self.screen.fill(COLORS['bg_dark'])
        
        # Kamera Çerçevesi
        cam_rect = pygame.Rect(40, 40, SCREEN_WIDTH-80, SCREEN_HEIGHT-80)
        pygame.draw.rect(self.screen, (0,0,0), cam_rect)
        pygame.draw.rect(self.screen, COLORS['primary'], cam_rect, 4, border_radius=10)
        
        text = self.font_md.render("Görüntü Yakalanıyor...", True, COLORS['text_main'])
        self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT-60))
        
        self.update()
        
    def show_analysis(self):
        """Analiz Animasyonu"""
        self.screen.fill(COLORS['bg_dark'])
        
        text = self.font_xl.render("Yapay Zeka Analizi...", True, COLORS['primary'])
        self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 40))
        
        sub = self.font_sm.render("Besin değerleri hesaplanıyor", True, COLORS['text_sec'])
        self.screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, SCREEN_HEIGHT//2 + 40))
        
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
