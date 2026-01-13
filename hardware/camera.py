# Kamera Modülü - Görüntü Yakalama

try:
    from picamera2 import Picamera2
except ImportError:
    from hardware.mock_hardware import MockPicamera2 as Picamera2
    print("[Mock] Kamera simülasyon modunda")
import numpy as np
from PIL import Image
from config import CAMERA_RESOLUTION, CAMERA_FORMAT, CAMERA_ROTATION

class Camera:
    def __init__(self):
        self.picam = Picamera2()
        config = self.picam.create_still_configuration(
            main={"size": CAMERA_RESOLUTION, "format": CAMERA_FORMAT}
        )
        self.picam.configure(config)
        self.picam.start()
    
    def capture_image(self):
        """Görüntü yakala ve numpy array döndür"""
        image = self.picam.capture_array()
        
        if CAMERA_ROTATION != 0:
            image = np.rot90(image, k=CAMERA_ROTATION // 90)
        
        return image
    
    def capture_pil_image(self):
        """PIL Image formatında görüntü yakala"""
        array = self.capture_image()
        return Image.fromarray(array)
    
    def save_image(self, filepath):
        """Görüntüyü dosyaya kaydet"""
        image = self.capture_pil_image()
        image.save(filepath)
        return filepath
    
    def cleanup(self):
        """Kamerayı kapat"""
        self.picam.stop()

# Test fonksiyonu
if __name__ == "__main__":
    import time
    
    camera = Camera()
    print("Kamera hazır. 3 saniye sonra fotoğraf çekilecek...")
    time.sleep(3)
    
    try:
        camera.save_image("test_capture.jpg")
        print("Fotoğraf kaydedildi: test_capture.jpg")
    finally:
        camera.cleanup()
