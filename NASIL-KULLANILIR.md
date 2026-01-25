# 🎯 Nutriquant Nasıl Kullanılır?

## ⚡ Hızlı Başlangıç

### 1️⃣ İlk Kurulum (Sadece Bir Kez)

```bash
cd /Users/hasankoc/Desktop/Proje/Bionluk/nutriquant
./start.sh
```

**Ne olacak?**
- ✅ Python kütüphaneleri yüklenecek (~5 dk)
- ✅ Node.js kütüphaneleri yüklenecek (~3 dk)
- ✅ Backend başlayacak (port 8000)
- ✅ Electron app açılacak (tam ekran)

**İlk çalıştırma:** ~10 dakika  
**Sonraki çalıştırmalar:** ~5 saniye

---

## 🖥️ macOS'ta Geliştirme

### Geliştirme Modu (Önerilen)

```bash
./start-dev.sh
```

**Avantajları:**
- ✅ DevTools açık (hata ayıklama)
- ✅ Hot reload (kod değişince otomatik güncellenir)
- ✅ Pencere modu (tam ekran değil)
- ✅ F11: Tam ekran toggle
- ✅ ESC: Kiosk mode'dan çık

### Production Modu

```bash
./start.sh
```

**Farkları:**
- Tam ekran açılır
- DevTools kapalı
- Raspberry Pi'deki gibi çalışır

---

## 🍓 Raspberry Pi'de Kullanım

### Manuel Başlatma

```bash
cd ~/nutriquant
./start-pi.sh
```

### Otomatik Başlatma (Boot'ta)

```bash
# Systemd service kur
sudo cp nutriquant.service /etc/systemd/system/
sudo systemctl enable nutriquant
sudo systemctl start nutriquant

# Durumu kontrol et
sudo systemctl status nutriquant
```

---

## 🎮 Uygulama Kullanımı

### Adım 1: Profil Oluştur

1. Dashboard açıldığında sağ üstteki **👤** (Profiller) ikonuna tıkla
2. Sağ üstteki **+** butonuna bas
3. Bilgileri doldur:
   - İsim: Örn. "Ahmet"
   - Cinsiyet: Erkek/Kadın
   - Boy: Örn. 175 cm
   - Kilo: Örn. 70 kg
4. **Kaydet** butonuna bas

### Adım 2: Profil Seç

1. Dashboard'a dön (sol üst **←** ok)
2. Sağ taraftaki profil listesinden profilini seç
3. Seçili profil **beyaz** renkte görünecek

### Adım 3: Yemek Tart ve Analiz Et

1. Yemeği tartıya koy
2. Sol tarafta ağırlık **gerçek zamanlı** gösterilir
3. **"Tara ve Analiz Et"** butonuna bas
4. Kamera fotoğraf çeker
5. AI yemeği tanır
6. Besin değerleri hesaplanır

### Adım 4: Sonuçları Gör ve Kaydet

1. Sonuç ekranında:
   - Yemek adı
   - Kalori, protein, karbonhidrat, yağ
   - BMI bilgisi
2. **Kaydet** butonuna bas → Veritabanına kaydedilir
3. **Tekrar Tara** butonuna bas → Yeni ölçüm

---

## 🔧 Geliştirme İpuçları

### Backend'i Ayrı Test Et

```bash
cd backend
source venv/bin/activate
python main.py

# Başka terminalde:
./test-backend.sh

# API dokümantasyonu:
# http://localhost:8000/docs
```

### Frontend'i Ayrı Test Et

```bash
cd frontend
npm run dev

# Tarayıcıda:
# http://localhost:5173
```

### Sadece React (Electron olmadan)

```bash
cd frontend
npm run dev
# Tarayıcıda açılır, Electron olmadan test edebilirsiniz
```

---

## 🐛 Sorun Giderme

### "npm: command not found"

**macOS:**
```bash
brew install node
```

**Raspberry Pi:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### "Backend başlamıyor"

```bash
cd backend
source venv/bin/activate
python main.py
# Hata mesajlarını okuyun
```

### "Port 8000 kullanımda"

```bash
# Çalışan backend'i durdur
lsof -ti:8000 | xargs kill -9

# Veya
pkill -f "python main.py"
```

### "Frontend açılmıyor"

```bash
cd frontend

# node_modules'u sil ve yeniden yükle
rm -rf node_modules package-lock.json
npm install

# Tekrar dene
npm run electron:dev
```

### "Kamera çalışmıyor (macOS)"

macOS'ta kamera mock mode'da çalışır (simülasyon).
Gerçek kamera sadece Raspberry Pi'de çalışır.

### "Tartı 0 gösteriyor (macOS)"

macOS'ta tartı mock mode'da çalışır (0 gösterir).
Gerçek tartı sadece Raspberry Pi'de çalışır.

---

## 📊 Port Kullanımı

| Port | Servis | Açıklama |
|------|--------|----------|
| 8000 | Backend API | FastAPI server |
| 5173 | Frontend Dev | Vite dev server (sadece geliştirme) |

---

## 🎨 Ekran Boyutları

- **Raspberry Pi:** 800x480 (4.3" dokunmatik)
- **Geliştirme:** Herhangi bir boyut (responsive)

---

## 🚀 Hızlı Komutlar

```bash
# İlk kurulum
./start.sh

# Geliştirme (DevTools açık)
./start-dev.sh

# Raspberry Pi production
./start-pi.sh

# Backend test
./test-backend.sh

# Sadece backend
cd backend && source venv/bin/activate && python main.py

# Sadece frontend
cd frontend && npm run dev
```

---

## 📝 Notlar

- **İlk kurulum uzun sürer** - Sabırlı olun
- **macOS/Windows:** Mock mode (sensörler simüle edilir)
- **Raspberry Pi:** Gerçek donanım kullanılır
- **Geliştirme:** `start-dev.sh` kullanın (daha hızlı)
- **Production:** `start-pi.sh` kullanın (tam ekran)

---

## ✅ Başarılı Kurulum Kontrolü

Şunları görüyorsanız başarılı:

1. ✅ Terminal'de: "Backend başlatıldı (PID: XXXX)"
2. ✅ Terminal'de: "Frontend başlatılıyor..."
3. ✅ Electron penceresi açıldı
4. ✅ 2 saniyelik splash screen animasyonu
5. ✅ Dashboard ekranı göründü
6. ✅ Sol tarafta ağırlık gösterimi (0g)
7. ✅ Sağ tarafta profil listesi

**Tebrikler! Nutriquant çalışıyor! 🎉**

---

## 🆘 Yardım

Sorun yaşarsanız:
1. `backend/backend.log` dosyasını kontrol edin
2. Terminal çıktılarını okuyun
3. `./test-backend.sh` çalıştırın
4. GitHub Issues'a bildirin
