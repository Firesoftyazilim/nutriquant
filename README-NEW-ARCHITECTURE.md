# 🎯 Nutriquant v2.0 - Modern Mimari

**Electron + React + Python FastAPI** ile yeniden tasarlandı!

## 🏗️ Mimari

```
┌─────────────────────────────────────────┐
│  FRONTEND (Electron + React)            │
│  - Modern glassmorphism UI              │
│  - Tam ekran kiosk mode                 │
│  - Framer Motion animasyonlar           │
│  - TailwindCSS styling                  │
│  Port: 5173 (dev) / Standalone (prod)   │
└──────────────┬──────────────────────────┘
               │ HTTP/WebSocket
               │ localhost:8000
┌──────────────▼──────────────────────────┐
│  BACKEND (Python FastAPI)               │
│  - RESTful API                          │
│  - WebSocket (gerçek zamanlı ağırlık)   │
│  - TensorFlow AI model                  │
│  - Raspberry Pi sensör kontrolü         │
│  Port: 8000                             │
└─────────────────────────────────────────┘
```

## 📁 Proje Yapısı

```
nutriquant/
├── frontend/              # Electron + React
│   ├── electron/          # Electron main process
│   │   ├── main.js        # Ana pencere (kiosk mode)
│   │   └── preload.js     # Güvenlik katmanı
│   ├── src/
│   │   ├── pages/         # React sayfaları
│   │   │   ├── Dashboard.jsx      # Ana ekran
│   │   │   ├── Scanning.jsx       # Tarama ekranı
│   │   │   ├── Results.jsx        # Sonuç ekranı
│   │   │   ├── Profiles.jsx       # Profil yönetimi
│   │   │   ├── Settings.jsx       # Ayarlar
│   │   │   └── SplashScreen.jsx   # Açılış ekranı
│   │   ├── components/    # Reusable component'ler
│   │   ├── services/      # API servisleri
│   │   │   └── api.js     # Backend iletişimi
│   │   ├── store/         # Zustand state
│   │   ├── App.jsx        # Ana component
│   │   └── main.jsx       # Entry point
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── backend/               # Python FastAPI
│   ├── main.py           # FastAPI app (tüm endpoint'ler)
│   ├── requirements.txt  # Python dependencies
│   ├── hardware/         # Symlink -> ../hardware
│   ├── ai/              # Symlink -> ../ai
│   ├── core/            # Symlink -> ../core
│   ├── data/            # Symlink -> ../data
│   ├── models/          # Symlink -> ../models
│   └── config.py        # Symlink -> ../config.py
│
├── hardware/             # Raspberry Pi sensörler (paylaşılan)
├── ai/                  # TensorFlow model (paylaşılan)
├── core/                # Business logic (paylaşılan)
├── data/                # JSON veritabanı
├── models/              # AI model dosyaları
├── start.sh             # 🚀 ANA BAŞLATMA SCRİPTİ
└── start-dev.sh         # 🔧 Geliştirme modu scripti
```

## 🚀 Hızlı Başlangıç

### İlk Kurulum ve Çalıştırma

```bash
./start.sh
```

Bu script:
1. ✅ Python virtual environment oluşturur
2. ✅ Backend kütüphanelerini yükler
3. ✅ Node.js bağımlılıklarını yükler
4. ✅ Backend'i başlatır (port 8000)
5. ✅ Frontend'i başlatır (Electron - tam ekran)

### Geliştirme Modu

```bash
./start-dev.sh
```

Geliştirme modunda:
- ✅ DevTools açık
- ✅ Hot reload aktif
- ✅ F11 ile tam ekran toggle
- ✅ ESC ile kiosk mode'dan çık

## 🎨 UI Özellikleri

### Glassmorphism Tasarım
- Şeffaf cam efekti
- Backdrop blur
- Gradient arka planlar
- Modern, minimalist

### Animasyonlar
- Sayfa geçişleri (Framer Motion)
- Hover efektleri
- Scale animasyonları
- Smooth transitions

### Tam Ekran Kiosk Mode
- Tarayıcı çubuğu yok
- Adres çubuğu yok
- Çıkış butonu yok (production)
- Raspberry Pi başlangıcında otomatik açılır

## 🔧 Geliştirme

### Frontend Geliştirme

```bash
cd frontend
npm run dev          # Sadece React dev server
npm run electron:dev # React + Electron birlikte
```

### Backend Geliştirme

```bash
cd backend
source venv/bin/activate
python main.py       # FastAPI server
```

API Dokümantasyonu: http://localhost:8000/docs

## 📦 Production Build

```bash
cd frontend
npm run build        # React build
npm run electron:build  # Electron executable
```

## 🔌 API Kullanımı

### WebSocket (Gerçek Zamanlı Ağırlık)

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/weight');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Ağırlık:', data.weight);
};
```

### HTTP Endpoints

```javascript
// Fotoğraf çek
const response = await fetch('http://localhost:8000/api/camera/capture');
const blob = await response.blob();

// Analiz yap
const result = await fetch('http://localhost:8000/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ weight: 150, profile_id: 1 })
});
```

## 🎯 Raspberry Pi Deployment

### Otomatik Başlatma

```bash
# /etc/xdg/autostart/nutriquant.desktop
[Desktop Entry]
Type=Application
Name=Nutriquant
Exec=/home/pi/nutriquant/start.sh
```

### Systemd Service (Alternatif)

```bash
sudo systemctl enable nutriquant
sudo systemctl start nutriquant
```

## 🐛 Sorun Giderme

### Backend başlamıyor
```bash
cd backend
source venv/bin/activate
python main.py
# Hata mesajlarını kontrol edin
```

### Frontend açılmıyor
```bash
cd frontend
npm run dev
# Tarayıcıda http://localhost:5173 açın
```

### Sensörler çalışmıyor
- Raspberry Pi'de çalıştığınızdan emin olun
- Mock mode otomatik aktif olur (macOS/Windows)

## 📝 Notlar

- **Geliştirme**: macOS/Linux/Windows'ta çalışır (mock mode)
- **Production**: Sadece Raspberry Pi 4'te tam özellikli
- **Port 8000**: Backend API
- **Port 5173**: Frontend dev server (sadece geliştirme)

## 🎉 Özellikler

- ✅ Modern, responsive UI
- ✅ Glassmorphism tasarım
- ✅ Smooth animasyonlar
- ✅ Gerçek zamanlı ağırlık gösterimi
- ✅ AI yemek tanıma
- ✅ Profil yönetimi
- ✅ Ölçüm geçmişi
- ✅ Batarya göstergesi
- ✅ LED ve ses kontrolleri
- ✅ Tam ekran kiosk mode
