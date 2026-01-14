# Kamera Modülü - Görüntü Yakalama (rpicam-still CLI Wrapper)

import os
import subprocess
import time
import numpy as np
from PIL import Image
from config import CAMERA_RESOLUTION, CAMERA_FORMAT, CAMERA_ROTATION

class Camera:
    def __init__(self):
        # rpicam-still komutunun varlığını kontrol et (opsiyonel)
        self.cmd = "rpicam-still"
        try:
            subprocess.run([self.cmd, "--help"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            print(f"[Uyarı] '{self.cmd}' bulunamadı. 'libcamera-still' deneniyor...")
            self.cmd = "libcamera-still"
            
        print(f"[Camera] CLI modu kullanılıyor ({self.cmd})")
        
        # Geçici dosya yolu
        self.temp_file = "/tmp/nutriquant_cam_capture.jpg"

    def capture_image(self):
        """rpicam-still ile görüntü yakala ve numpy array döndür"""
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
        """Hata durumunda siyah/gürültülü görüntü döndür"""
        return np.random.randint(0, 256, (CAMERA_RESOLUTION[1], CAMERA_RESOLUTION[0], 3), dtype=np.uint8)
    
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
    
    def cleanup(self):
        """Temizlik"""
        if os.path.exists(self.temp_file):
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
