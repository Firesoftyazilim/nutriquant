# Bildirim/Uyarı Sistemi - Dokunmatik Ekran İçin
# Toast bildirimleri ve modal uyarılar

import pygame
import time

# Renk Paleti
COLORS = {
    'bg_dark': (20, 24, 30),
    'card_bg': (32, 38, 48),
    'primary': (0, 122, 255),
    'success': (50, 215, 75),
    'warning': (255, 204, 0),
    'error': (255, 69, 58),
    'text_main': (255, 255, 255),
    'text_sec': (160, 170, 180),
    'border': (60, 65, 75)
}

class Notification:
    def __init__(self, screen, font_md, font_sm):
        self.screen = screen
        self.font_md = font_md
        self.font_sm = font_sm
        
        # Toast bildirimleri
        self.toasts = []  # [(message, type, start_time), ...]
        self.toast_duration = 3.0  # saniye
    
    def show_toast(self, message, toast_type='info'):
        """
        Toast bildirimi göster
        toast_type: 'info', 'success', 'warning', 'error'
        """
        self.toasts.append({
            'message': message,
            'type': toast_type,
            'start_time': time.time()
        })
    
    def draw_toasts(self):
        """Toast bildirimlerini çiz"""
        current_time = time.time()
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Eski toast'ları temizle
        self.toasts = [t for t in self.toasts if current_time - t['start_time'] < self.toast_duration]
        
        # Toast'ları çiz (üstten alta)
        y_offset = 20
        for toast in self.toasts:
            elapsed = current_time - toast['start_time']
            
            # Fade out efekti (son 0.5 saniye)
            if elapsed > self.toast_duration - 0.5:
                alpha = int(255 * (self.toast_duration - elapsed) / 0.5)
            else:
                alpha = 255
            
            # Renk seç
            if toast['type'] == 'success':
                bg_color = COLORS['success']
                icon = '✓'
            elif toast['type'] == 'warning':
                bg_color = COLORS['warning']
                icon = '⚠'
            elif toast['type'] == 'error':
                bg_color = COLORS['error']
                icon = '✕'
            else:
                bg_color = COLORS['primary']
                icon = 'ℹ'
            
            # Toast boyutu
            message_text = self.font_md.render(toast['message'], True, COLORS['text_main'])
            toast_width = min(message_text.get_width() + 100, screen_width - 40)
            toast_height = 60
            
            # Merkeze yerleştir
            x = (screen_width - toast_width) // 2
            y = y_offset
            
            # Arka plan
            toast_rect = pygame.Rect(x, y, toast_width, toast_height)
            toast_surface = pygame.Surface((toast_width, toast_height), pygame.SRCALPHA)
            
            # Yuvarlatılmış dikdörtgen
            pygame.draw.rect(toast_surface, (*bg_color, alpha), (0, 0, toast_width, toast_height), border_radius=15)
            
            # İkon
            icon_text = self.font_md.render(icon, True, COLORS['text_main'])
            icon_text.set_alpha(alpha)
            toast_surface.blit(icon_text, (20, (toast_height - icon_text.get_height()) // 2))
            
            # Mesaj
            message_text.set_alpha(alpha)
            toast_surface.blit(message_text, (60, (toast_height - message_text.get_height()) // 2))
            
            # Ekrana çiz
            self.screen.blit(toast_surface, (x, y))
            
            y_offset += toast_height + 10
    
    def show_modal(self, title, message, buttons=['Tamam']):
        """
        Modal dialog göster
        buttons: ['Tamam'], ['Evet', 'Hayır'], vb.
        Döndürür: Tıklanan buton index'i veya None
        """
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Modal boyutu
        modal_width = 600
        modal_height = 300
        modal_x = (screen_width - modal_width) // 2
        modal_y = (screen_height - modal_height) // 2
        
        # Overlay (yarı saydam arka plan)
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Modal arka plan
        modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
        pygame.draw.rect(self.screen, COLORS['card_bg'], modal_rect, border_radius=20)
        pygame.draw.rect(self.screen, COLORS['border'], modal_rect, 3, border_radius=20)
        
        # Başlık
        title_text = self.font_md.render(title, True, COLORS['text_main'])
        title_x = modal_x + (modal_width - title_text.get_width()) // 2
        self.screen.blit(title_text, (title_x, modal_y + 30))
        
        # Mesaj
        message_text = self.font_sm.render(message, True, COLORS['text_sec'])
        message_x = modal_x + (modal_width - message_text.get_width()) // 2
        self.screen.blit(message_text, (message_x, modal_y + 100))
        
        # Butonlar
        button_rects = []
        button_width = 150
        button_height = 50
        button_spacing = 20
        total_button_width = len(buttons) * button_width + (len(buttons) - 1) * button_spacing
        start_x = modal_x + (modal_width - total_button_width) // 2
        button_y = modal_y + modal_height - 80
        
        for i, btn_text in enumerate(buttons):
            btn_x = start_x + i * (button_width + button_spacing)
            btn_rect = pygame.Rect(btn_x, button_y, button_width, button_height)
            button_rects.append(btn_rect)
            
            # Buton arka plan
            pygame.draw.rect(self.screen, COLORS['primary'], btn_rect, border_radius=15)
            
            # Buton metni
            text = self.font_md.render(btn_text, True, COLORS['text_main'])
            text_rect = text.get_rect(center=btn_rect.center)
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()
        
        # Buton tıklamasını bekle
        waiting = True
        result = None
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(pos):
                            result = i
                            waiting = False
                            break
        
        return result

# Kullanım örneği
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 480))
    font_md = pygame.font.Font(None, 32)
    font_sm = pygame.font.Font(None, 24)
    
    notif = Notification(screen, font_md, font_sm)
    
    # Toast örnekleri
    notif.show_toast("Profil kaydedildi!", "success")
    notif.show_toast("Uyarı: Pil düşük", "warning")
    notif.show_toast("Hata: Bağlantı kesildi", "error")
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((20, 24, 30))
        notif.draw_toasts()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
