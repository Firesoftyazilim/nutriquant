# Nutriquant - Akıllı Yemek Tartısı

Raspberry Pi 4 tabanlı, yapay zeka destekli besin analiz sistemi. Kamera ile yemek tanıma, ağırlık ölçümü ve besin değerleri hesaplama.

## Donanım Bileşenleri

### Ana Sistem
- **Raspberry Pi 4B** - Ana işlemci
- **5V/5A USB-C Adaptör** - Güç kaynağı
- **2x 18650 Li-ion Pil** - Taşınabilir güç

### Sensörler ve Modüller
- **HX711 Tartı Modülü** - Ağırlık sensörü (GPIO 5, 6)
- **Kamera Modülü** - Yemek görüntü yakalama
- **UPS HAT** - Pil yönetimi (I2C)

### Çıkış Birimleri
- **4.3" Dokunmatik Ekran** - 800x480 çözünürlük (Mini HDMI)
- **LED Ring (WS2812B)** - 24 LED, görsel geri bildirim (GPIO 18)
- **Gigagus GG-AUS1 USB Ses Kartı** - Hoparlör çıkışı

## Proje Yapısı

```
project/
├── main.py                 # Ana uygulama
├── config.py              # Sistem konfigürasyonu
├── requirements.txt       # Python bağımlılıkları
├── setup.sh              # Kurulum scripti
│
├── hardware/             # Donanım sürücüleri
│   ├── scale.py         # HX711 tartı modülü
│   ├── camera.py        # Picamera2 kamera kontrolü
│   ├── battery.py       # UPS HAT pil yönetimi
│   ├── led_ring.py      # WS2812B LED kontrolü
│   └── speaker.py       # Ses çıkışı
│
├── ai/                   # Yapay zeka
│   └── food_recognition.py  # TensorFlow Lite yemek tanıma
│
├── core/                 # İş mantığı
│   ├── nutrition.py     # Besin değerleri hesaplama
│   ├── bmi.py          # VKİ hesaplama
│   └── database.py     # Veri yönetimi
│
├── ui/                   # Kullanıcı arayüzü
│   └── display.py       # Pygame ekran kontrolü
│
├── data/                 # Veri dosyaları
│   ├── foods.json       # Yemek besin değerleri (18 yemek)
│   └── users.json       # Kullanıcı bilgileri
│
├── models/               # AI modelleri
│   ├── food_classifier.tflite  # TFLite model (eklenecek)
│   └── labels.txt       # Sınıf etiketleri
│
└── assets/               # Medya dosyaları
    ├── sounds/          # Ses efektleri
    ├── fonts/           # Yazı tipleri
    ├── icons/           # İkonlar
    └── images/          # Görseller
```

## Kurulum

### 1. Raspberry Pi OS Kurulumu
```bash
# Raspberry Pi Imager ile Raspberry Pi OS (64-bit) yükleyin
```

### 2. Sistem Hazırlığı
```bash
cd project
chmod +x setup.sh
./setup.sh
source venv/bin/activate
```

### 3. AI Model Yerleştirme
Projenin çalışması için bir TensorFlow Lite modeline ihtiyacı vardır. Eğer kendi modelinizi eğitmediyseniz, sistem **simülasyon modunda** (rastgele yemek seçerek) çalışmaya devam edecektir. 

Kendi modelinizi eğitmek için [Teachable Machine](https://teachablemachine.withgoogle.com/) kullanabilir ve çıktıyı `models/food_classifier.tflite` olarak kaydedebilirsiniz.

## GPIO Bağlantıları

| Bileşen | GPIO Pin | Açıklama |
|---------|----------|----------|
| HX711 DOUT | GPIO 5 | Tartı veri |
| HX711 SCK | GPIO 6 | Tartı saat |
| LED Ring | GPIO 18 (PWM) | WS2812B veri |
| UPS HAT | I2C (SDA/SCL) | Pil yönetimi |
| Kamera | CSI | Kamera portu |
| Ekran | HDMI | Mini HDMI |
| Hoparlör | USB | Ses kartı |

## Kullanım

### Başlatma
```bash
source venv/bin/activate
python3 main.py
```

### Çalışma Akışı
1. **Bekleme** - Ana ekran gösterilir, pil durumu izlenir
2. **Ölçüm** - Tabak tartıya yerleştirilir (>10g)
3. **Görüntü** - Kamera yemeği yakalar
4. **Tanıma** - AI modeli yemeği tanır
5. **Hesaplama** - Besin değerleri hesaplanır
6. **Sonuç** - Ekranda kalori, protein, karbonhidrat, yağ gösterilir
7. **VKİ Kontrolü** - Kullanıcı VKİ'sine göre uyarı verilir

### LED Renk Kodları
- **Yeşil** - Sistem hazır / Başarılı
- **Mavi** - İşlem yapılıyor
- **Beyaz** - Görüntü yakalama
- **Sarı** - Yemek tanınamadı
- **Kırmızı** - Hata / VKİ uyarısı

### Ses Geri Bildirimleri
- `beep.wav` - Ölçüm başladı
- `success.wav` - İşlem başarılı
- `warning.wav` - VKİ uyarısı
- `error.wav` - Hata oluştu
- `ready.wav` - Sistem hazır

## Modül Açıklamaları

### hardware/scale.py
HX711 load cell ile ağırlık ölçümü. Kalibrasyon, tare (sıfırlama) ve okuma fonksiyonları.

### hardware/camera.py
Picamera2 ile görüntü yakalama. RGB array ve PIL Image formatlarında çıktı.

### hardware/battery.py
INA219 sensörü ile voltaj, akım, güç ve pil yüzdesi ölçümü. Şarj durumu kontrolü.

### hardware/led_ring.py
WS2812B LED ring kontrolü. Renk, nabız ve gökkuşağı efektleri.

### hardware/speaker.py
Pygame mixer ile ses çıkışı. WAV dosyaları çalma.

### ai/food_recognition.py
TensorFlow Lite ile yemek sınıflandırma. Görüntü ön işleme ve tahmin.

### core/nutrition.py
Yemek veritabanından besin değerleri hesaplama (100g bazlı).

### core/bmi.py
Vücut Kitle İndeksi hesaplama. Yaş gruplarına göre (çocuk, yetişkin, yaşlı) kategorizasyon.

### core/database.py
JSON tabanlı veri yönetimi. Kullanıcı ve ölçüm kayıtları.

### ui/display.py
Pygame ile 4.3" dokunmatik ekran UI. Ana ekran, ölçüm, sonuç ve hata ekranları.

### main.py
Ana uygulama döngüsü. Tüm modülleri koordine eder, ölçüm akışını yönetir.

## Konfigürasyon

`config.py` dosyasından ayarlanabilir parametreler:

- **Ekran**: Çözünürlük, FPS, tam ekran modu
- **Tartı**: GPIO pinleri, kalibrasyon değeri, maksimum ağırlık
- **Kamera**: Çözünürlük, format, rotasyon
- **AI**: Model yolu, güven eşiği, giriş boyutu
- **LED**: Pin, LED sayısı, parlaklık
- **Pil**: I2C adresi, düşük pil eşikleri
- **VKİ**: Yaş grupları ve aralıkları

## Kalibrasyon

### Tartı Kalibrasyonu
```python
from hardware.scale import Scale

scale = Scale()
# Bilinen ağırlık (örn: 500g) koyun
reference_unit = scale.calibrate(500)
print(f"Reference Unit: {reference_unit}")
# config.py'de HX711_REFERENCE_UNIT değerini güncelleyin
```

## Veri Formatları

### foods.json
```json
{
  "yemek_key": {
    "name": "Yemek Adı",
    "calorie": 120,
    "protein": 3.1,
    "carb": 25.6,
    "fat": 2.0
  }
}
```

### users.json
```json
{
  "users": {
    "1": {
      "name": "Kullanıcı Adı",
      "age": 30,
      "weight": 70,
      "height": 175
    }
  }
}
```

## Sorun Giderme

### Tartı Okuma Hatası
- GPIO pinlerini kontrol edin
- Kabloları kontrol edin
- Kalibrasyon yapın

### Kamera Çalışmıyor
```bash
sudo raspi-config
# Interface Options > Camera > Enable
```

### I2C Hatası
```bash
sudo raspi-config
# Interface Options > I2C > Enable
sudo i2cdetect -y 1
```

### LED Çalışmıyor
- GPIO 18 (PWM) kullanıldığından emin olun
- Güç kaynağı yeterli mi kontrol edin

### Model Bulunamadı
`models/food_classifier.tflite` dosyasını yerleştirin.

## Geliştirme

### Yeni Yemek Ekleme
1. `data/foods.json` dosyasına ekleyin
2. `models/labels.txt` dosyasına ekleyin
3. AI modelini yeniden eğitin

### Test Modları
Her modül bağımsız test edilebilir:
```bash
python3 hardware/scale.py
python3 hardware/camera.py
python3 hardware/battery.py
python3 ui/display.py
```

### Kalibrasyon
Tartı kalibrasyonu için:
```bash
python3 calibrate_scale.py
```

## Teknik Özellikler

- **İşlemci**: Raspberry Pi 4B (1.5GHz quad-core)
- **Bellek**: 2GB+ RAM önerilir
- **Tartı Hassasiyeti**: ±1g
- **Kamera Çözünürlük**: 640x480
- **Ekran**: 800x480, 60Hz
- **Pil Ömrü**: ~4-6 saat (kullanıma göre)
- **AI Çıkarım Süresi**: ~200-500ms

## Lisans

Bu proje İsmail Mert Ulakoğlu tarafından geliştirilmiştir.

## Versiyon

v1.0.0 - 2026
