# 🍓 Nutriquant - Akıllı Yemek Tartısı

Raspberry Pi tabanlı, AI destekli besin analiz sistemi.

## 🚀 Hızlı Başlangıç

### Raspberry Pi (Production)
```bash
./start-pi.sh
```
- Backend + Frontend (Electron, tam ekran kiosk mode)
- Production build kullanır
- Raspberry Pi için optimize edilmiş

### Development (Raspberry Pi)
```bash
./start-dev.sh
```
- Backend + Frontend (Electron + Vite dev server)
- Hot reload aktif
- DevTools açık

### Mac/Linux Development (Browser)
```bash
./start-mac.sh
```
- Backend + Frontend (Vite dev server)
- Tarayıcıda açılır: http://localhost:5173
- API: http://localhost:8000

## 📦 Manuel Kurulum

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev              # Development
npm run build            # Production build
npm run electron         # Electron (production)
npm run electron:dev     # Electron (development)
```

## 🔧 Sistem Gereksinimleri

### Raspberry Pi
- Raspberry Pi 4 (4GB+ RAM önerilir)
- Raspberry Pi OS (64-bit)
- Python 3.11+
- Node.js 18+
- Donanım:
  - HX711 Load Cell (tartı)
  - Raspberry Pi Camera Module
  - UPS HAT (opsiyonel)
  - Speaker (ses efektleri)

### Geliştirme (Mac/Linux/Windows)
- Python 3.11+
- Node.js 18+

## 📁 Proje Yapısı

```
nutriquant/
├── backend/              # FastAPI backend
│   ├── hardware/         # Donanım kontrolleri
│   ├── ai/              # AI model (TFLite)
│   ├── core/            # İş mantığı
│   └── main.py          # API server
├── frontend/            # React + Electron
│   ├── src/             # React components
│   ├── electron/        # Electron main/preload
│   └── dist/            # Build çıktısı
├── models/              # AI modelleri
├── start-pi.sh          # Pi production
├── start-dev.sh         # Pi development
└── start-mac.sh         # Mac/Linux dev
```

## 🔑 Özellikler

- ✅ AI ile yemek tanıma (TFLite)
- ✅ Besin değeri hesaplama
- ✅ BMI takibi
- ✅ Kullanıcı profilleri
- ✅ Ölçüm geçmişi
- ✅ Tam ekran kiosk mode
- ✅ Ses geri bildirimleri
- ✅ WebSocket ile canlı ağırlık

## 🛠️ Sorun Giderme

### "ModuleNotFoundError: No module named 'fastapi'"
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### "Failed to build 'python-prctl'"
```bash
sudo apt-get install libcap-dev
```

### Frontend boş ekran
```bash
cd frontend
npm run build
```

### Electron CSP uyarısı
CSP meta tag'i `index.html` içinde mevcut, uyarı normal.

## 📝 API Dokümantasyonu

Backend çalışırken:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔐 Güvenlik

- Content Security Policy aktif
- Electron sandbox mode
- Context isolation
- No node integration in renderer

## 📄 Lisans

MIT License
