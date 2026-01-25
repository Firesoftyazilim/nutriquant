# Nutriquant - Geliştirme Ortamı Kurulumu

## Önemli Not

Bu proje **Raspberry Pi 4** için geliştirilmiştir. Bazı kütüphaneler (picamera2, RPi.GPIO, rpi-ws281x, vb.) sadece Raspberry Pi donanımında çalışır.

## macOS/Linux/Windows'ta Geliştirme

Geliştirme yapmak için aşağıdaki adımları takip edin:

### 1. Virtual Environment Oluşturma

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# veya
venv\Scripts\activate  # Windows
```

### 2. Geliştirme Bağımlılıklarını Yükleme

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements-dev.txt
```

**Not:** `requirements.txt` dosyası Raspberry Pi için, `requirements-dev.txt` dosyası geliştirme ortamı içindir.

### 3. Python Sürümü

- **Raspberry Pi:** Python 3.9+
- **Geliştirme Ortamı:** Python 3.13 (veya 3.10+)

## Kurulu Kütüphaneler (Geliştirme)

- **opencv-python:** Görüntü işleme
- **Pillow:** Resim manipülasyonu
- **numpy:** Sayısal hesaplamalar
- **pygame:** UI geliştirme
- **pydub:** Ses işleme
- **python-json-logger:** Loglama
- **python-dotenv:** Ortam değişkenleri
- **pytest:** Test framework
- **pytest-cov:** Test coverage

## Raspberry Pi'ye Deployment

Raspberry Pi'ye kurulum için:

```bash
pip install -r requirements.txt
```

## Sorun Giderme

### Pillow veya NumPy Kurulum Hatası

Python 3.13 kullanıyorsanız, en güncel versiyonları kullanın:
- Pillow >= 10.2.0
- NumPy >= 1.26.0

### Pygame Kurulum Hatası

Python 3.13 için pygame >= 2.6.0 gereklidir.
