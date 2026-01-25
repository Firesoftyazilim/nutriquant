# 📂 Nutriquant Proje Yapısı

## 🎯 Genel Bakış

```
nutriquant/
│
├── 🎨 frontend/                    # Electron + React UI
│   ├── electron/                   # Electron main process
│   │   ├── main.js                 # Ana pencere (kiosk mode)
│   │   └── preload.js              # IPC bridge
│   │
│   ├── src/
│   │   ├── pages/                  # React sayfaları
│   │   │   ├── SplashScreen.jsx    # Açılış animasyonu
│   │   │   ├── Dashboard.jsx       # Ana ekran (profil + ağırlık)
│   │   │   ├── Scanning.jsx        # Tarama ve AI analizi
│   │   │   ├── Results.jsx         # Besin değerleri sonucu
│   │   │   ├── Profiles.jsx        # Profil CRUD
│   │   │   └── Settings.jsx        # Ayarlar ve testler
│   │   │
│   │   ├── components/             # Reusable UI
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── WeightDisplay.jsx
│   │   │   ├── NutritionCard.jsx
│   │   │   ├── ProfileCard.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js              # Backend API client
│   │   │
│   │   ├── store/
│   │   │   └── appStore.js         # Zustand global state
│   │   │
│   │   ├── App.jsx                 # Router setup
│   │   ├── main.jsx                # React entry
│   │   └── index.css               # Global styles
│   │
│   ├── package.json                # npm dependencies
│   ├── vite.config.js              # Vite config
│   ├── tailwind.config.js          # TailwindCSS config
│   └── postcss.config.js
│
├── 🐍 backend/                     # Python FastAPI
│   ├── main.py                     # FastAPI app (tüm endpoints)
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example
│   │
│   ├── hardware/                   # Symlink → ../hardware
│   ├── ai/                         # Symlink → ../ai
│   ├── core/                       # Symlink → ../core
│   ├── data/                       # Symlink → ../data
│   ├── models/                     # Symlink → ../models
│   └── config.py                   # Symlink → ../config.py
│
├── 🔧 hardware/                    # Raspberry Pi Sensörler (Paylaşılan)
│   ├── scale.py                    # HX711 tartı sensörü
│   ├── camera.py                   # Picamera2 / rpicam-still
│   ├── battery.py                  # UPS HAT (I2C)
│   ├── led_ring.py                 # WS2812B LED ring
│   ├── speaker.py                  # USB ses kartı
│   └── mock_hardware.py            # Mock sınıfları (dev için)
│
├── 🤖 ai/                          # TensorFlow AI (Paylaşılan)
│   ├── food_recognition.py         # TFLite model wrapper
│   └── __init__.py
│
├── 💼 core/                        # Business Logic (Paylaşılan)
│   ├── nutrition.py                # Besin değeri hesaplama
│   ├── bmi.py                      # BMI hesaplama
│   ├── database.py                 # JSON veritabanı
│   └── __init__.py
│
├── 📊 data/                        # JSON Veritabanı
│   ├── foods.json                  # Yemek besin değerleri
│   ├── profiles.json               # Kullanıcı profilleri
│   ├── measurements.json           # Ölçüm geçmişi
│   └── settings.json               # Uygulama ayarları
│
├── 🧠 models/                      # AI Model Dosyaları
│   ├── model_float16.tflite        # TensorFlow Lite model
│   └── class_indices.json          # Sınıf etiketleri
│
├── 🎨 assets/                      # Medya Dosyaları
│   ├── images/
│   │   └── Wallpapers/             # Arka plan resimleri
│   └── sounds/                     # Ses efektleri
│
├── 🚀 start.sh                     # Ana başlatma scripti
├── 🔧 start-dev.sh                 # Geliştirme modu
├── 🍓 start-pi.sh                  # Raspberry Pi production
├── 🧪 test-backend.sh              # Backend API test
│
├── config.py                       # Global konfigürasyon
├── nutriquant.service              # Systemd service
├── INSTALLATION.md                 # Kurulum rehberi
└── README-NEW-ARCHITECTURE.md      # Mimari dokümantasyon
```

## 🔄 Veri Akışı

### 1. Kullanıcı Profil Seçer (Dashboard)
```
Frontend → GET /api/profiles → Backend → Database
```

### 2. Gerçek Zamanlı Ağırlık
```
Frontend ← WebSocket /ws/weight ← Backend ← HX711 Sensör
```

### 3. Tarama ve Analiz
```
Frontend → POST /api/analyze → Backend
                                  ↓
                            1. Kamera.capture()
                            2. AI.recognize()
                            3. Nutrition.calculate()
                                  ↓
Frontend ← JSON Response ← Backend
```

### 4. Sonuç Kaydetme
```
Frontend → POST /api/measurements → Backend → Database
```

## 🎨 UI Component Hiyerarşisi

```
App (Router)
├── SplashScreen (2 saniye)
│
├── Dashboard
│   ├── WeightDisplay (WebSocket)
│   ├── ProfileCard[] (Liste)
│   └── ScanButton
│
├── Scanning
│   ├── CameraPreview
│   ├── LoadingSpinner
│   └── ProgressBar
│
├── Results
│   ├── FoodName
│   ├── NutritionCard[] (4 adet)
│   ├── BMIInfo
│   └── ActionButtons
│
├── Profiles
│   ├── ProfileList
│   └── ProfileForm (Modal)
│
└── Settings
    └── SettingsGrid
```

## 🔐 Güvenlik

- ✅ CORS middleware (sadece localhost)
- ✅ Context isolation (Electron)
- ✅ No node integration (güvenli)
- ✅ Environment variables (.env)

## 🚀 Performans

- ⚡ WebSocket (10 Hz ağırlık güncellemesi)
- ⚡ Lazy loading (React Router)
- ⚡ Optimized builds (Vite)
- ⚡ Hardware acceleration (Electron)

## 📱 Responsive Design

- 800x480 (Raspberry Pi 4.3" ekran) - Ana hedef
- 1920x1080 (Full HD) - Test için
- Touch-optimized (büyük butonlar)

## 🎯 Sonraki Adımlar

1. ✅ Temel mimari kuruldu
2. ⏳ Tüm UI sayfaları tamamlanacak
3. ⏳ Ek animasyonlar eklenecek
4. ⏳ Ölçüm geçmişi sayfası
5. ⏳ Grafik ve istatistikler (Recharts)
