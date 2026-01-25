# Nutriquant Backend

Python FastAPI + Raspberry Pi Sensör Kontrolü

## Özellikler

- 🚀 **FastAPI**: Modern, hızlı Python web framework
- 🔌 **WebSocket**: Gerçek zamanlı ağırlık stream'i
- 🤖 **TensorFlow**: Yemek tanıma AI modeli
- 🔧 **Raspberry Pi Sensörler**: HX711, Kamera, LED, Batarya
- 📊 **RESTful API**: Tüm işlevler için endpoint'ler

## Kurulum

```bash
# Virtual environment oluştur
python3 -m venv venv
source venv/bin/activate

# Kütüphaneleri yükle
pip install -r requirements.txt
```

## Çalıştırma

```bash
# Geliştirme
python main.py

# Production (uvicorn)
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health
- `GET /` - API sağlık kontrolü
- `GET /api/health` - Sistem durumu

### Scale
- `GET /api/scale/weight` - Anlık ağırlık
- `POST /api/scale/tare` - Tartıyı sıfırla
- `WS /ws/weight` - Gerçek zamanlı ağırlık stream'i

### Camera
- `GET /api/camera/capture` - Fotoğraf çek
- `POST /api/camera/preview/start` - Önizleme başlat
- `POST /api/camera/preview/stop` - Önizleme durdur

### AI & Analysis
- `POST /api/analyze` - Yemek analizi (AI + Besin hesaplama)

### Profiles
- `GET /api/profiles` - Tüm profiller
- `POST /api/profiles` - Yeni profil
- `PUT /api/profiles/{id}` - Profil güncelle
- `DELETE /api/profiles/{id}` - Profil sil

### Measurements
- `POST /api/measurements` - Ölçüm kaydet
- `GET /api/measurements` - Tüm ölçümler

### Hardware
- `POST /api/led/{color}` - LED kontrolü
- `POST /api/speaker/{sound}` - Ses çal
- `GET /api/battery` - Batarya durumu

## Mock Mode

Raspberry Pi dışı platformlarda (macOS, Windows) otomatik olarak mock mode aktif olur.
Sensörler simüle edilir.
