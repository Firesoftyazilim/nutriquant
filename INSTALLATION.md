# 📦 Nutriquant Kurulum Rehberi

## 🖥️ Geliştirme Ortamı (macOS/Linux/Windows)

### Gereksinimler
- Python 3.10+ (Python 3.13 önerilir)
- Node.js 18+ ve npm
- Git

### Kurulum

```bash
# 1. Projeyi klonla
git clone <repo-url>
cd nutriquant

# 2. Tek komutla başlat (tüm kurulumları yapar)
./start.sh
```

**İlk çalıştırmada:**
- Python kütüphaneleri yüklenecek (~5 dakika)
- Node.js kütüphaneleri yüklenecek (~3 dakika)
- Backend ve Frontend otomatik başlayacak

**Sonraki çalıştırmalarda:**
- Kurulumlar atlanır, direkt başlar (~5 saniye)

### Geliştirme Modu

```bash
# DevTools açık, hot reload aktif
./start-dev.sh
```

---

## 🍓 Raspberry Pi 4 Kurulumu

### Gereksinimler
- Raspberry Pi 4 (4GB+ RAM önerilir)
- Raspberry Pi OS (Bullseye veya üzeri)
- 4.3" Dokunmatik Ekran
- İnternet bağlantısı (kurulum için)

### 1. Sistem Güncellemesi

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Gerekli Sistem Paketleri

```bash
# Python ve geliştirme araçları
sudo apt install -y python3-pip python3-venv python3-dev

# Node.js ve npm (v18+)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Kamera kütüphaneleri
sudo apt install -y libcamera-apps

# Ses kütüphaneleri
sudo apt install -y ffmpeg

# X11 (Electron için)
sudo apt install -y xserver-xorg xinit
```

### 3. Projeyi Kur

```bash
# Projeyi home dizinine klonla
cd ~
git clone <repo-url> nutriquant
cd nutriquant

# İlk kurulum ve başlatma
./start.sh
```

### 4. Otomatik Başlatma (Opsiyonel)

#### Yöntem 1: Systemd Service (Önerilen)

```bash
# Service dosyasını kopyala
sudo cp nutriquant.service /etc/systemd/system/

# Service'i etkinleştir
sudo systemctl enable nutriquant
sudo systemctl start nutriquant

# Durumu kontrol et
sudo systemctl status nutriquant

# Logları görüntüle
sudo journalctl -u nutriquant -f
```

#### Yöntem 2: Autostart Desktop Entry

```bash
# Autostart dizini oluştur
mkdir -p ~/.config/autostart

# Desktop entry oluştur
cat > ~/.config/autostart/nutriquant.desktop << EOF
[Desktop Entry]
Type=Application
Name=Nutriquant
Exec=/home/pi/nutriquant/start-pi.sh
Terminal=false
EOF
```

### 5. Donanım Bağlantıları

#### HX711 Tartı Sensörü
- **DOUT** → GPIO 5
- **SCK** → GPIO 6
- **VCC** → 3.3V
- **GND** → GND

#### Kamera Modülü
- Raspberry Pi Camera Module v2/v3
- CSI kablo ile bağlı

#### LED Ring (WS2812B)
- **DIN** → GPIO 18
- **VCC** → 5V
- **GND** → GND

#### UPS HAT (Batarya)
- I2C bağlantısı (otomatik)

### 6. Kalibrasyon

```bash
# Tartı kalibrasyonu
cd ~/nutriquant
source backend/venv/bin/activate
python calibrate_scale.py
```

---

## 🔧 Sorun Giderme

### Backend başlamıyor

```bash
cd backend
source venv/bin/activate
python main.py
# Hata mesajlarını okuyun
```

### Frontend açılmıyor

```bash
cd frontend
npm run dev
# Tarayıcıda http://localhost:5173 açın
```

### Kamera çalışmıyor

```bash
# Kamera modülünü test et
rpicam-still -o test.jpg

# Kamera etkin mi kontrol et
vcgencmd get_camera
```

### Tartı okuma yapmıyor

```bash
# GPIO izinlerini kontrol et
sudo usermod -a -G gpio pi
sudo reboot
```

### Electron açılmıyor (Raspberry Pi)

```bash
# X11 çalışıyor mu?
echo $DISPLAY  # :0 olmalı

# X11 başlat
startx
```

---

## 📊 Port Kullanımı

- **8000**: Backend API (FastAPI)
- **5173**: Frontend Dev Server (sadece geliştirme)

---

## 🎯 Kullanım

### İlk Başlatma

1. `./start.sh` çalıştır
2. Splash screen göreceksiniz (2 saniye)
3. Dashboard açılacak
4. Profil ekleyin (sağ üst + butonu)
5. Profil seçin
6. Yemek koyun, "Tara ve Analiz Et" butonuna basın
7. Sonuçları görün ve kaydedin

### Günlük Kullanım

```bash
# Geliştirme (DevTools açık)
./start-dev.sh

# Production (Tam ekran)
./start-pi.sh
```

---

## 🔄 Güncelleme

```bash
cd ~/nutriquant
git pull origin main
./start.sh  # Yeni bağımlılıklar varsa yükler
```

---

## 📝 Notlar

- İlk kurulum 10-15 dakika sürebilir
- Raspberry Pi'de build işlemi uzun sürer (sabırlı olun)
- macOS/Windows'ta mock mode otomatik aktif olur
- Geliştirme için macOS/Linux önerilir

---

## 🆘 Destek

Sorun yaşarsanız:
1. `backend/backend.log` dosyasını kontrol edin
2. Terminal çıktılarını okuyun
3. GitHub Issues'a bildirin
