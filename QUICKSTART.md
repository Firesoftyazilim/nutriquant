# ⚡ Nutriquant Hızlı Başlangıç

## 🎯 Tek Komutla Başlat

```bash
./start.sh
```

**İlk çalıştırma:** 5-10 dakika (kütüphane kurulumları)  
**Sonraki çalıştırmalar:** 5 saniye

---

## 📋 Ne Olacak?

### 1️⃣ Kurulum (İlk Seferde)
- ✅ Python virtual environment oluşturulur
- ✅ Backend kütüphaneleri yüklenir (FastAPI, TensorFlow, vb.)
- ✅ Node.js kütüphaneleri yüklenir (React, Electron, vb.)

### 2️⃣ Başlatma
- ✅ Backend API başlar (http://localhost:8000)
- ✅ Frontend Electron app açılır (tam ekran)

### 3️⃣ Kullanım
- ✅ 2 saniyelik splash screen
- ✅ Dashboard açılır
- ✅ Profil ekleyin ve kullanmaya başlayın!

---

## 🔧 Geliştirme Modu

```bash
./start-dev.sh
```

**Farklar:**
- DevTools açık
- Hot reload aktif
- Tam ekran değil (pencere modu)
- F11: Tam ekran toggle
- ESC: Kiosk mode'dan çık

---

## 🧪 Backend Test

```bash
# Backend'i test et
./test-backend.sh

# API dokümantasyonu
# Tarayıcıda: http://localhost:8000/docs
```

---

## 📱 Kullanım Akışı

### 1. Profil Ekle
- Dashboard'da sağ üst **+** butonuna bas
- İsim, cinsiyet, boy, kilo gir
- Kaydet

### 2. Profil Seç
- Dashboard'da profil kartına tıkla
- Seçili profil beyaz renkte görünür

### 3. Yemek Tara
- Yemeği tartıya koy
- Ağırlık gösterilir (gerçek zamanlı)
- **"Tara ve Analiz Et"** butonuna bas

### 4. Sonuçları Gör
- AI yemeği tanır
- Besin değerleri hesaplanır
- BMI bilgisi gösterilir

### 5. Kaydet veya Tekrar Tara
- **Kaydet**: Veritabanına kaydeder
- **Tekrar Tara**: Yeni ölçüm yapar

---

## 🎨 Ekran Görünümü

### Dashboard (Ana Ekran)
```
┌─────────────────────────────────────┐
│ Nutriquant        🔋 85%            │
├─────────────┬───────────────────────┤
│             │                       │
│   AĞIRLIK   │      PROFİLLER        │
│             │                       │
│    250g     │  ✓ Ahmet              │
│             │    Ayşe               │
│ [TARA VE    │    Mehmet             │
│  ANALİZ ET] │                       │
│             │  [+ Yeni Profil]      │
└─────────────┴───────────────────────┘
       👤 Profiller    ⚙️ Ayarlar
```

### Scanning (Tarama)
```
┌─────────────────────────────────────┐
│ ← Fotoğraf Çekiliyor...             │
├─────────────────────────────────────┤
│                                     │
│        [KAMERA GÖRÜNTÜSÜ]           │
│                                     │
│         🔄 Analiz yapılıyor...      │
│                                     │
├─────────────────────────────────────┤
│ ████████████░░░░░░░░░░ %60          │
└─────────────────────────────────────┘
```

### Results (Sonuç)
```
┌─────────────────────────────────────┐
│ ←  Analiz Sonucu                    │
├─────────────────────────────────────┤
│         Tavuk Izgara                │
│         150g • %92 güven            │
├─────────────────────────────────────┤
│  🔥 Kalori    🥩 Protein            │
│  247.5 kcal   46.5g                 │
│                                     │
│  🌾 Karbonhidrat  💧 Yağ            │
│  0.0g             5.4g              │
├─────────────────────────────────────┤
│ VKİ: 22.5 - Normal                  │
├─────────────────────────────────────┤
│ [🔄 Tekrar Tara]  [💾 Kaydet]       │
└─────────────────────────────────────┘
```

---

## 🛠️ Komutlar Özeti

| Komut | Açıklama |
|-------|----------|
| `./start.sh` | İlk kurulum + başlatma (production) |
| `./start-dev.sh` | Geliştirme modu (DevTools) |
| `./start-pi.sh` | Raspberry Pi production |
| `./test-backend.sh` | Backend API test |

---

## 🎯 İlk Kullanımda Yapılacaklar

1. ✅ `./start.sh` çalıştır
2. ✅ Splash screen'i izle
3. ✅ Dashboard açılınca **+ Profil Ekle**
4. ✅ Bilgilerini gir ve kaydet
5. ✅ Profilini seç (beyaz olacak)
6. ✅ Bir şey koy tartıya (simülasyonda 0g gösterir)
7. ✅ **Tara ve Analiz Et** butonuna bas
8. ✅ Sonuçları gör ve kaydet!

---

## 💡 İpuçları

- **macOS/Windows'ta:** Mock mode otomatik aktif (sensörler simüle edilir)
- **Raspberry Pi'de:** Gerçek sensörler kullanılır
- **Geliştirme:** `start-dev.sh` kullanın (daha hızlı)
- **Production:** `start.sh` veya `start-pi.sh`
- **API Test:** http://localhost:8000/docs (Swagger UI)

---

## 🐛 Hata Aldıysanız

### "Node.js bulunamadı"
```bash
# Node.js yükleyin
brew install node  # macOS
```

### "Python bulunamadı"
```bash
# Python 3.10+ yükleyin
brew install python@3.13  # macOS
```

### "Port 8000 kullanımda"
```bash
# Çalışan backend'i durdurun
lsof -ti:8000 | xargs kill -9
```

### "npm install hatası"
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 🎉 Başarılı Kurulum

Eğer şunları görüyorsanız başarılı:
- ✅ Terminal'de "Backend başlatıldı" mesajı
- ✅ Electron penceresi açıldı
- ✅ Splash screen animasyonu oynatıldı
- ✅ Dashboard ekranı göründü

**Tebrikler! Nutriquant çalışıyor! 🚀**
