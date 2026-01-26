# Kamera Modülü - Görüntü Yakalama (rpicam-still CLI Wrapper)

import os
import subprocess
import time
import platform
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from config import CAMERA_RESOLUTION, CAMERA_FORMAT, CAMERA_ROTATION

class Camera:
    def __init__(self):
        # Platform tespiti - Raspberry Pi dışında mock mod kullan
        self.is_raspberry_pi = self._detect_raspberry_pi()
        self.mock_mode = not self.is_raspberry_pi
        self.preview_process = None  # rpicam-vid process for live preview
        
        if self.mock_mode:
            print("[Camera] Mock mod aktif (Raspberry Pi dışı platform)")
            self.temp_file = None
        else:
            # rpicam-still komutunun varlığını kontrol et
            self.cmd = "rpicam-still"
            self.vid_cmd = "rpicam-vid"  # Video önizleme için
            try:
                subprocess.run([self.cmd, "--help"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            except (FileNotFoundError, subprocess.CalledProcessError):
                print(f"[Uyarı] '{self.cmd}' bulunamadı. 'libcamera-still' deneniyor...")
                self.cmd = "libcamera-still"
                self.vid_cmd = "libcamera-vid"
                
            print(f"[Camera] CLI modu kullanılıyor ({self.cmd})")
            
            # Geçici dosya yolu
            self.temp_file = "/tmp/nutriquant_cam_capture.jpg"
    
    def _detect_raspberry_pi(self):
        """Raspberry Pi platformunu tespit et"""
        system = platform.system()
        if system != "Linux":
            return False
        
        # /proc/device-tree/model dosyasını kontrol et (Raspberry Pi'ye özgü)
        try:
            with open('/proc/device-tree/model', 'r') as f:
                model = f.read()
                return 'Raspberry Pi' in model
        except:
            return False

    def capture_image(self):
        """Görüntü yakala ve numpy array döndür"""
        # Mock modda gerçek kamera kullanma
        if self.mock_mode:
            return self._get_mock_image()
        
        try:
            # Komut: rpicam-still -n (preview yok) -t 100 (100ms gecikme) --width W --height H -o output.jpg
            # --nopreview (-n) önemli, yoksa ekrana basmaya çalışır
            # -t süresi pozlama ve AWB için biraz zaman tanır. Çok kısa olursa karanlık/yeşil çıkabilir.
            cmd_args = [
                self.cmd,
                "-n",
                "-t", "200", 
                "--width", str(CAMERA_RESOLUTION[0]),
                "--height", str(CAMERA_RESOLUTION[1]),
                "-o", self.temp_file,
                "--force" # Dosya varsa üzerine yaz
            ]
            
            # Komutu çalıştır
            subprocess.run(cmd_args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Dosyayı oku
            if os.path.exists(self.temp_file):
                pil_image = Image.open(self.temp_file)
                pil_image = pil_image.convert("RGB")
                
                # Döndürme işlemi
                if CAMERA_ROTATION != 0:
                    pil_image = pil_image.rotate(CAMERA_ROTATION)
                
                # Numpy array'e çevir
                image_array = np.array(pil_image)
                return image_array
            else:
                print("Hata: Görüntü dosyası oluşturulamadı.")
                return self._get_mock_image()
                
        except Exception as e:
            print(f"Kamera yakalama hatası: {e}")
            return self._get_mock_image()

    def _get_mock_image(self):
        """Mock kamera görüntüsü - Renkli test deseni"""
        # Renkli gradient oluştur
        width, height = CAMERA_RESOLUTION
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)
        
        # Gradient arka plan (mavi-mor-pembe)
        for y in range(height):
            r = int(100 + (y / height) * 155)
            g = int(50 + (y / height) * 100)
            b = int(200 - (y / height) * 50)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Metin ekle
        try:
            # Büyük font kullan
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
        except:
            font = ImageFont.load_default()
        
        text = "MOCK CAMERA"
        # Metin boyutunu al
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Merkeze yerleştir
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Gölge efekti
        draw.text((x+2, y+2), text, fill=(0, 0, 0), font=font)
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        # Numpy array'e çevir
        return np.array(image)
    
    def capture_pil_image(self):
        """PIL Image formatında görüntü yakala"""
        array = self.capture_image()
        return Image.fromarray(array)
    
    def save_image(self, filepath):
        """Görüntüyü dosyaya kaydet"""
        # Zaten dosyaya kaydediyoruz ama istenen yere kopyalayalım/taşıyalım
        # Veya yeniden capture yapalım
        array = self.capture_image()
        image = Image.fromarray(array)
        image.save(filepath)
        return filepath
    
    def start_preview(self):
        """Canlı kamera önizlemesi başlat (rpicam-vid)"""
        if self.mock_mode:
            print("[Camera] Mock modda önizleme yok")
            return False
        
        if self.preview_process is not None:
            print("[Camera] Önizleme zaten çalışıyor")
            return True
        
        try:
            # rpicam-vid -t 0 (sonsuz süre) --fullscreen
            cmd_args = [
                self.vid_cmd,
                "-t", "0",  # Sonsuz süre (manuel durdurulana kadar)
                "--width", str(CAMERA_RESOLUTION[0]),
                "--height", str(CAMERA_RESOLUTION[1]),
                "--fullscreen"
            ]
            
            self.preview_process = subprocess.Popen(
                cmd_args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"[Camera] Önizleme başlatıldı (PID: {self.preview_process.pid})")
            return True
            
        except Exception as e:
            print(f"[Camera] Önizleme başlatma hatası: {e}")
            self.preview_process = None
            return False
    
    def stop_preview(self):
        """Canlı kamera önizlemesini durdur"""
        if self.preview_process is None:
            return
        
        try:
            self.preview_process.terminate()
            self.preview_process.wait(timeout=2)
            print("[Camera] Önizleme durduruldu")
        except:
            # Terminate çalışmazsa kill
            try:
                self.preview_process.kill()
            except:
                pass
        finally:
            self.preview_process = None
    
    def cleanup(self):
        """Temizlik"""
        # Önizleme varsa durdur
        self.stop_preview()
        
        if not self.mock_mode and self.temp_file and os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
            except:
                pass

# Test fonksiyonu
if __name__ == "__main__":
    camera = Camera()
    print("Kamera hazır. Fotoğraf çekiliyor...")
    
    try:
        start = time.time()
        camera.save_image("test_capture_cli.jpg")
        end = time.time()
        print(f"Fotoğraf kaydedildi: test_capture_cli.jpg (Süre: {end-start:.2f}s)")
    finally:
        camera.cleanup()
