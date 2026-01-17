# Ekran Klavyesi - Dokunmatik Ekran İçin
# Raspberry Pi 4.3" Dokunmatik Ekran

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

# Renk Paleti
COLORS = {
    'bg_dark': (20, 24, 30),
    'card_bg': (32, 38, 48),
    'primary': (0, 122, 255),
    'text_main': (255, 255, 255),
    'text_sec': (160, 170, 180),
    'border': (60, 65, 75)
}

class OnScreenKeyboard:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.visible = False
        self.input_type = 'text'  # 'text' veya 'number'
        
        # Klavye düzenleri
        self.layouts = {
            'text': [
                ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
                ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '←'],
                ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ' ', '✓']
            ],
            'number': [
                ['1', '2', '3'],
                ['4', '5', '6'],
                ['7', '8', '9'],
                ['←', '0', '✓']
            ]
        }
        
        self.keys = []
        self.setup_keyboard()
    
    def setup_keyboard(self):
        """Klavye tuşlarını oluştur"""
        # Klavye pozisyonu (ekranın alt kısmı)
        kb_height = 200
        kb_y = SCREEN_HEIGHT - kb_height
        
        # Tuş boyutları
        key_width = 70
        key_height = 45
        key_spacing = 5
        
        self.keyboard_rect = pygame.Rect(0, kb_y, SCREEN_WIDTH, kb_height)
    
    def show(self, input_type='text'):
        """Klavyeyi göster"""
        self.visible = True
        self.input_type = input_type
    
    def hide(self):
        """Klavyeyi gizle"""
        self.visible = False
    
    def draw(self):
        """Klavyeyi çiz"""
        if not self.visible:
            return
        
        # Arka plan
        pygame.draw.rect(self.screen, COLORS['card_bg'], self.keyboard_rect)
        pygame.draw.rect(self.screen, COLORS['border'], self.keyboard_rect, 2)
        
        # Klavye düzenini seç
        layout = self.layouts[self.input_type]
        
        # Tuşları çiz
        self.keys = []
        kb_y = self.keyboard_rect.y + 10
        
        for row_idx, row in enumerate(layout):
            # Satır genişliğini hesapla
            if self.input_type == 'number':
                key_width = 100
                key_height = 45
                total_width = len(row) * key_width + (len(row) - 1) * 5
                start_x = (SCREEN_WIDTH - total_width) // 2
            else:
                key_width = 70
                key_height = 40
                total_width = len(row) * key_width + (len(row) - 1) * 5
                start_x = (SCREEN_WIDTH - total_width) // 2
            
            for col_idx, key in enumerate(row):
                # Özel tuşlar için genişlik ayarla
                if key == ' ':
                    w = key_width * 2
                elif key in ['←', '✓']:
                    w = key_width
                else:
                    w = key_width
                
                x = start_x + col_idx * (key_width + 5)
                y = kb_y + row_idx * (key_height + 5)
                
                rect = pygame.Rect(x, y, w, key_height)
                self.keys.append((key, rect))
                
                # Tuş arka planı
                if key == '✓':
                    color = COLORS['primary']
                else:
                    color = COLORS['bg_dark']
                
                pygame.draw.rect(self.screen, color, rect, border_radius=8)
                pygame.draw.rect(self.screen, COLORS['border'], rect, 2, border_radius=8)
                
                # Tuş metni
                text = self.font.render(key, True, COLORS['text_main'])
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
    
    def handle_click(self, pos):
        """Klavye tıklamasını işle"""
        if not self.visible:
            return None
        
        for key, rect in self.keys:
            if rect.collidepoint(pos):
                return key
        
        return None
