# 4.3" Dokunmatik Ekran UI - Pygame

import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, FPS, APP_NAME

class Display:
    def __init__(self):
        pygame.init()
        
        flags = pygame.FULLSCREEN if FULLSCREEN else 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        pygame.display.set_caption(APP_NAME)
        
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'gray': (128, 128, 128),
            'light_gray': (200, 200, 200),
            'green': (0, 200, 0),
            'red': (200, 0, 0),
            'blue': (0, 100, 200),
            'yellow': (255, 200, 0)
        }
    
    def clear(self, color='white'):
        """Ekranı temizle"""
        self.screen.fill(self.colors[color])
    
    def draw_text(self, text, x, y, font='medium', color='black', center=False):
        """Metin çiz"""
        font_obj = {
            'large': self.font_large,
            'medium': self.font_medium,
            'small': self.font_small
        }.get(font, self.font_medium)
        
        text_surface = font_obj.render(str(text), True, self.colors[color])
        text_rect = text_surface.get_rect()
        
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        
        self.screen.blit(text_surface, text_rect)
    
    def draw_button(self, text, x, y, width, height, color='blue', text_color='white'):
        """Buton çiz"""
        pygame.draw.rect(self.screen, self.colors[color], (x, y, width, height), border_radius=10)
        self.draw_text(text, x + width // 2, y + height // 2, 'medium', text_color, center=True)
        return pygame.Rect(x, y, width, height)
    
    def draw_progress_bar(self, x, y, width, height, progress, color='green'):
        """İlerleme çubuğu çiz"""
        pygame.draw.rect(self.screen, self.colors['light_gray'], (x, y, width, height), border_radius=5)
        
        fill_width = int(width * (progress / 100))
        if fill_width > 0:
            pygame.draw.rect(self.screen, self.colors[color], (x, y, fill_width, height), border_radius=5)
    
    def show_home_screen(self, battery_percent):
        """Ana ekran"""
        self.clear()
        
        self.draw_text(APP_NAME, SCREEN_WIDTH // 2, 100, 'large', 'blue', center=True)
        self.draw_text("Yemek Tartısı", SCREEN_WIDTH // 2, 180, 'medium', 'gray', center=True)
        
        self.draw_text("Tabağı tartıya yerleştirin", SCREEN_WIDTH // 2, 300, 'medium', 'black', center=True)
        
        self.draw_text(f"Pil: %{battery_percent}", 20, SCREEN_HEIGHT - 40, 'small', 'gray')
        
        self.update()
    
    def show_measuring_screen(self, weight):
        """Ölçüm ekranı"""
        self.clear()
        
        self.draw_text("Ölçüm Yapılıyor...", SCREEN_WIDTH // 2, 80, 'large', 'blue', center=True)
        
        self.draw_text(f"{weight}g", SCREEN_WIDTH // 2, 240, 'large', 'black', center=True)
        
        self.draw_text("Lütfen bekleyin", SCREEN_WIDTH // 2, 350, 'medium', 'gray', center=True)
        
        self.update()
    
    def show_result_screen(self, food_name, nutrition, bmi_comment):
        """Sonuç ekranı"""
        self.clear()
        
        self.draw_text(food_name, SCREEN_WIDTH // 2, 60, 'large', 'blue', center=True)
        
        y = 150
        self.draw_text(f"{nutrition['weight']}g", SCREEN_WIDTH // 2, y, 'medium', 'black', center=True)
        
        y += 80
        self.draw_text(f"Kalori: {nutrition['calorie']} kcal", 100, y, 'medium', 'black')
        
        y += 50
        self.draw_text(f"Protein: {nutrition['protein']}g", 100, y, 'small', 'gray')
        
        y += 40
        self.draw_text(f"Karbonhidrat: {nutrition['carb']}g", 100, y, 'small', 'gray')
        
        y += 40
        self.draw_text(f"Yağ: {nutrition['fat']}g", 100, y, 'small', 'gray')
        
        y += 60
        color = 'red' if bmi_comment in ['Yüksek', 'Obez'] else 'green'
        self.draw_text(f"VKİ Durumu: {bmi_comment}", SCREEN_WIDTH // 2, y, 'medium', color, center=True)
        
        self.update()
    
    def show_error_screen(self, message):
        """Hata ekranı"""
        self.clear()
        
        self.draw_text("Hata!", SCREEN_WIDTH // 2, 150, 'large', 'red', center=True)
        self.draw_text(message, SCREEN_WIDTH // 2, 250, 'medium', 'black', center=True)
        
        self.update()
    
    def update(self):
        """Ekranı güncelle"""
        pygame.display.flip()
        self.clock.tick(FPS)
    
    def handle_events(self):
        """Olayları işle"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'quit'
        return None
    
    def cleanup(self):
        """Pygame'i kapat"""
        pygame.quit()

# Test fonksiyonu
if __name__ == "__main__":
    display = Display()
    
    try:
        display.show_home_screen(75)
        pygame.time.wait(2000)
        
        display.show_measuring_screen(180)
        pygame.time.wait(2000)
        
        nutrition = {
            'name': 'Bulgur Pilavı',
            'weight': 180,
            'calorie': 216,
            'protein': 5.6,
            'carb': 46.1,
            'fat': 3.6
        }
        display.show_result_screen('Bulgur Pilavı', nutrition, 'Normal')
        pygame.time.wait(3000)
        
    finally:
        display.cleanup()
