# 🍓 Raspberry Pi Kurulum Rehberi

## ⚡ Hızlı Kurulum (Tek Komut)

```bash
cd ~/nutriquant
./start.sh
```

**Bu komut otomatik olarak:**
1. ✅ Python virtual environment oluşturur
2. ✅ Python kütüphanelerini yükler
3. ✅ Node.js'i kurar (yoksa)
4. ✅ npm kütüphanelerini yükler
5. ✅ Backend'i başlatır
6. ✅ Frontend'i başlatır (tam ekran)

**İlk kurulum:** 15-20 dakika  
**Sonraki:** 5 saniye

---

## 📋 Adım Adım Kurulum

### 1. Sistem Güncellemesi

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Python Kurulumu

```bash
# Python 3.9+ (genelde yüklü)
python3 --version

# Gerekli paketler
sudo apt install -y python3-pip python3-venv python3-dev
```

### 3. Sistem Kütüphaneleri

```bash
# Kamera
sudo apt install -y libcamera-apps

# Ses
sudo apt install -y ffmpeg

# X11 (Electron için)
sudo apt install -y xserver-xorg xinit

# GPIO izinleri
sudo usermod -a -G gpio $USER
sudo usermod -a -G i2c $USER
```

### 4. Projeyi Klonla

```bash
cd ~
git clone https://github.com/Firesoftyazilim/nutriquant.git
cd nutriquant
```

### 5. İlk Başlatma

```bash
./start.sh
```

**Bu komut:**
- Node.js yoksa otomatik kurar
- Tüm Python ve npm kütüphanelerini yükler
- Backend ve Frontend'i başlatır

**Bekleme süresi:** 15-20 dakika (ilk seferde)

---

## 🎯 Kullanım

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

# Logları izle
sudo journalctl -u nutriquant -f

# Durdur
sudo systemctl stop nutriquant

# Yeniden başlat
sudo systemctl restart nutriquant
```

---

## 🔧 Donanım Bağlantıları

### HX711 Tartı Sensörü
```
HX711          Raspberry Pi
------         ------------
VCC    →       3.3V (Pin 1)
GND    →       GND (Pin 6)
DOUT   →       GPIO 5 (Pin 29)
SCK    →       GPIO 6 (Pin 31)
```

### Kamera Modülü
- Raspberry Pi Camera Module v2 veya v3
- CSI kablo ile bağlı
- `sudo raspi-config` → Interface → Camera → Enable

### LED Ring (WS2812B)
```
WS2812B        Raspberry Pi
-------        ------------
VCC    →       5V (Pin 2)
GND    →       GND (Pin 14)
DIN    →       GPIO 18 (Pin 12)
```

### UPS HAT (Batarya)
- I2C bağlantısı (otomatik)
- `sudo raspi-config` → Interface → I2C → Enable

---

## 🧪 Test

### Backend Test

```bash
cd ~/nutriquant
./test-backend.sh
```

### Manuel Test

```bash
# Backend
cd ~/nutriquant/backend
source venv/bin/activate
python main.py

# Başka terminalde:
curl http://localhost:8000/api/health
```

### Kamera Test

```bash
rpicam-still -o test.jpg
```

### Tartı Test

```bash
cd ~/nutriquant
source backend/venv/bin/activate
python calibrate_scale.py
```

---

## 🐛 Sorun Giderme

### "Node.js bulunamadı"

```bash
# Manuel kurulum
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Kontrol
node --version
npm --version
```

### "venv bulunamadı"

```bash
# İlk kurulum için start.sh kullanın
./start.sh

# start-pi.sh sadece kurulum yapıldıktan sonra kullanılır
```

### "Permission denied: GPIO"

```bash
# GPIO grubuna ekle
sudo usermod -a -G gpio $USER
sudo usermod -a -G i2c $USER

# Yeniden giriş yap veya reboot
sudo reboot
```

### "Kamera çalışmıyor"

```bash
# Kamera etkin mi?
vcgencmd get_camera

# Kamera interface'i etkinleştir
sudo raspi-config
# Interface Options → Camera → Enable

# Reboot
sudo reboot
```

### "Port 8000 kullanımda"

```bash
# Çalışan backend'i durdur
sudo lsof -ti:8000 | xargs sudo kill -9

# Veya systemd ile
sudo systemctl stop nutriquant
```

### "Electron açılmıyor"

```bash
# X11 çalışıyor mu?
echo $DISPLAY  # :0 olmalı

# X11 başlat
startx

# Veya otomatik login ayarla
sudo raspi-config
# System Options → Boot / Auto Login → Desktop Autologin
```

---

## 📊 Performans İpuçları

### Raspberry Pi 4 Optimizasyonu

```bash
# GPU memory artır (kamera için)
sudo nano /boot/config.txt
# Ekle: gpu_mem=256

# Overclock (opsiyonel)
# arm_freq=2000
# over_voltage=6

# Reboot
sudo reboot
```

### Swap Artır (Build için)

```bash
# Build sırasında bellek yetersizse
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# CONF_SWAPSIZE=2048

sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

---

## 🔄 Güncelleme

```bash
cd ~/nutriquant

# Git pull
git pull origin main

# Yeniden başlat (yeni bağımlılıklar varsa yükler)
./start.sh
```

---

## 📝 Kullanım Akışı

### İlk Kullanım

1. `./start.sh` çalıştır (ilk kurulum)
2. Splash screen (2 saniye)
3. Dashboard açılır
4. Profil ekle (+ butonu)
5. Profil seç
6. Yemek koy, tara
7. Sonuçları kaydet

### Günlük Kullanım

```bash
# Raspberry Pi açıldığında otomatik başlar (systemd ile)
# Veya manuel:
./start-pi.sh
```

---

## 🎯 Önemli Notlar

- ⚠️ **İlk kurulum uzun sürer** - Raspberry Pi'de npm install 10-15 dakika sürebilir
- ⚠️ **İnternet gerekli** - Kurulum için internet bağlantısı şart
- ⚠️ **Önce start.sh** - İlk kurulum için `start.sh`, sonra `start-pi.sh` kullanın
- ✅ **Otomatik kurulum** - Node.js yoksa otomatik kurar
- ✅ **Mock mode yok** - Raspberry Pi'de gerçek donanım kullanılır

---

## ✅ Başarılı Kurulum Kontrolü

Şunları görüyorsanız başarılı:

```
✅ Backend başlatıldı (PID: XXXX)
✅ Node.js bulundu: v18.x.x
✅ Frontend kütüphaneleri yüklendi
🎨 Frontend başlatılıyor (TAM EKRAN)...
```

Ardından:
- Electron penceresi tam ekran açılır
- Splash screen animasyonu (2 saniye)
- Dashboard ekranı görünür

**Tebrikler! Nutriquant Raspberry Pi'de çalışıyor! 🎉**
