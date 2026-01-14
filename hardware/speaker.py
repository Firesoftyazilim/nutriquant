# Hoparlör - Ses Çıkışı (USB Ses Kartı)

import pygame
import os
from config import SOUND_DEVICE, VOLUME, ASSETS_DIR

class Speaker:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(VOLUME / 100)
        self.sounds_dir = os.path.join(ASSETS_DIR, "sounds")
    
    def play_sound(self, filename):
        """Ses dosyası çal"""
        filepath = os.path.join(self.sounds_dir, filename)
        if os.path.exists(filepath):
            try:
                sound = pygame.mixer.Sound(filepath)
                sound.play()
            except Exception as e:
                print(f"[Mock] Ses çalma: {filename}")
        else:
            print(f"[Mock] Ses çalma: {filename}")
    
    def play_beep(self):
        """Bip sesi"""
        self.play_sound("beep.wav")
    
    def play_success(self):
        """Başarılı işlem sesi"""
        self.play_sound("success.wav")
    
    def play_warning(self):
        """Uyarı sesi"""
        self.play_sound("warning.wav")
    
    def play_error(self):
        """Hata sesi"""
        self.play_sound("error.wav")
    
    def play_ready(self):
        """Hazır sesi"""
        self.play_sound("ready.wav")
    
    def play_startup_music(self):
        """Açılış müziği - En yüksek ses ile"""
        filepath = os.path.join(self.sounds_dir, "start.mp3")
        if os.path.exists(filepath):
            try:
                pygame.mixer.music.set_volume(1.0)  # Maksimum ses
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"[Mock] Açılış müziği çalma: start.mp3")
        else:
            print(f"[Mock] Açılış müziği çalma: start.mp3")
    
    def set_volume(self, volume):
        """Ses seviyesi ayarla (0-100)"""
        pygame.mixer.music.set_volume(volume / 100)
    
    def stop(self):
        """Sesi durdur"""
        pygame.mixer.stop()

# Test fonksiyonu
if __name__ == "__main__":
    import time
    
    speaker = Speaker()
    
    print("Bip...")
    speaker.play_beep()
    time.sleep(1)
    
    print("Başarılı...")
    speaker.play_success()
    time.sleep(1)
    
    print("Uyarı...")
    speaker.play_warning()
