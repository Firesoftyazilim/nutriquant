# Raspberry Pi Kiosk Mode Kurulum

Bu dokümanda Raspberry Pi'nin açılışta otomatik olarak Nutriquant uygulamasını tam ekran kiosk modunda başlatması için gerekli adımlar anlatılmaktadır.

## 📋 Gereksinimler

- Raspberry Pi (3/4/5)
- Raspberry Pi OS (Desktop versiyonu)
- İnternet bağlantısı
- Ekran bağlantısı

## 🚀 Kurulum Adımları

### 1. Projeyi Raspberry Pi'ye Kopyalayın

```bash
cd /home/pi
git clone https://github.com/Firesoftyazilim/nutriquant.git
cd nutriquant
```

### 2. Gerekli Paketleri Kurun

```bash
# Sistem güncellemesi
sudo apt update
sudo apt upgrade -y

# Chromium browser
sudo apt install -y chromium-browser

# Python ve pip
sudo apt install -y python3 python3-pip python3-venv

# Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Diğer gereksinimler
sudo apt install -y curl unclutter xdotool
```

### 3. Script İzinlerini Ayarlayın

```bash
cd /home/pi/nutriquant
chmod +x start-pi.sh
chmod +x backend/start.sh
```

### 4. Systemd Service'i Kurun

```bash
# Service dosyasını systemd dizinine kopyalayın
sudo cp nutriquant-kiosk.service /etc/systemd/system/

# Service'i etkinleştirin
sudo systemctl daemon-reload
sudo systemctl enable nutriquant-kiosk.service

# Service'i başlatın (test için)
sudo systemctl start nutriquant-kiosk.service

# Durumu kontrol edin
sudo systemctl status nutriquant-kiosk.service
```

### 5. Otomatik Giriş Ayarlayın (Desktop Görünmemesi İçin)

```bash
# Raspberry Pi Configuration aracını açın
sudo raspi-config
```

**Menüde:**
1. `System Options` → `Boot / Auto Login` seçin
2. `Desktop Autologin` seçin (Desktop GUI, pi kullanıcısı ile otomatik giriş)
3. `Finish` ve `Reboot`

### 6. Masaüstü Ortamını Gizleyin (Opsiyonel)

Eğer masaüstü tamamen görünmesin istiyorsanız:

```bash
# Autostart dizinini oluşturun
mkdir -p /home/pi/.config/lxsession/LXDE-pi

# Autostart dosyasını düzenleyin
nano /home/pi/.config/lxsession/LXDE-pi/autostart
```

**Dosya içeriğini şu şekilde yapın:**
```bash
# Fare imlecini gizle (10 saniye hareketsizlikten sonra)
@unclutter -idle 0.1 -root

# Ekran koruyucuyu devre dışı bırak
@xset s off
@xset -dpms
@xset s noblank

# Masaüstü öğelerini gizle
@pcmanfm --desktop-off
```

Kaydedin ve çıkın (CTRL+X, Y, Enter).

### 7. Raspberry Pi'yi Yeniden Başlatın

```bash
sudo reboot
```

## ✅ Sonuç

Raspberry Pi yeniden başladığında:
1. ✅ Otomatik olarak `pi` kullanıcısı ile giriş yapılır
2. ✅ Backend (`backend/start.sh`) başlatılır
3. ✅ Frontend (Vite dev server) başlatılır
4. ✅ Chromium tam ekran kiosk modunda açılır
5. ✅ Nutriquant uygulaması görüntülenir
6. ✅ Masaüstü, menü çubukları görünmez

## 🔧 Yönetim Komutları

### Service'i Durdur
```bash
sudo systemctl stop nutriquant-kiosk.service
```

### Service'i Yeniden Başlat
```bash
sudo systemctl restart nutriquant-kiosk.service
```

### Service'i Devre Dışı Bırak (Otomatik başlatma)
```bash
sudo systemctl disable nutriquant-kiosk.service
```

### Log'ları Görüntüle
```bash
# Systemd log
sudo journalctl -u nutriquant-kiosk.service -f

# Backend log
tail -f /home/pi/nutriquant/backend/backend.log

# Frontend log
tail -f /home/pi/nutriquant/frontend/frontend.log
```

## 🐛 Sorun Giderme

### Uygulama Başlamıyor

1. Service durumunu kontrol edin:
```bash
sudo systemctl status nutriquant-kiosk.service
```

2. Log'ları inceleyin:
```bash
sudo journalctl -u nutriquant-kiosk.service -n 50
```

3. Manuel olarak test edin:
```bash
cd /home/pi/nutriquant
./start-pi.sh
```

### Chromium Açılmıyor

```bash
# X11 display kontrol
echo $DISPLAY  # :0 olmalı

# Chromium test
DISPLAY=:0 chromium-browser --version
```

### Backend/Frontend Başlamıyor

```bash
# Backend test
cd /home/pi/nutriquant/backend
./start.sh

# Frontend test
cd /home/pi/nutriquant/frontend
npm run dev
```

## 🔄 Güncelleme

```bash
cd /home/pi/nutriquant
git pull origin main
sudo systemctl restart nutriquant-kiosk.service
```

## 🛑 Kiosk Modundan Çıkış

Eğer Raspberry Pi'ye erişmeniz gerekiyorsa:

**Yöntem 1: SSH ile**
```bash
ssh pi@<raspberry-pi-ip>
sudo systemctl stop nutriquant-kiosk.service
```

**Yöntem 2: Klavye ile (Chromium kapatma)**
- `ALT + F4` - Chromium'u kapat
- Service otomatik yeniden başlatır (10 saniye sonra)

**Yöntem 3: Service'i tamamen durdur**
```bash
# SSH veya başka bir terminal ile
sudo systemctl stop nutriquant-kiosk.service
sudo systemctl disable nutriquant-kiosk.service
```

## 📝 Notlar

- Proje yolu: `/home/pi/nutriquant` olarak varsayılmıştır
- Kullanıcı: `pi` olarak varsayılmıştır
- Port: Frontend 5173, Backend 8000
- Service otomatik yeniden başlatma: 10 saniye

## 🆘 Destek

Sorun yaşarsanız log dosyalarını kontrol edin:
- `/home/pi/nutriquant/backend/backend.log`
- `/home/pi/nutriquant/frontend/frontend.log`
- `sudo journalctl -u nutriquant-kiosk.service`
