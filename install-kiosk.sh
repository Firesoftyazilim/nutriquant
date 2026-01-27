#!/bin/bash

# ============================================
# Nutriquant Kiosk Mode Otomatik Kurulum
# ============================================

echo "============================================"
echo "🍓 Nutriquant Kiosk Mode Kurulum"
echo "============================================"
echo ""

# Root kontrolü
if [ "$EUID" -eq 0 ]; then 
    echo "❌ Bu scripti root olarak çalıştırmayın!"
    echo "   Kullanım: ./install-kiosk.sh"
    exit 1
fi

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "📍 Proje dizini: $PROJECT_DIR"
echo ""

# 1. Gerekli paketleri kur
echo "📦 Gerekli paketler kuruluyor..."
echo ""

# Chromium
if ! command -v chromium-browser &> /dev/null; then
    echo "   → Chromium browser kuruluyor..."
    sudo apt install -y chromium-browser
else
    echo "   ✅ Chromium zaten kurulu"
fi

# Python
if ! command -v python3 &> /dev/null; then
    echo "   → Python3 kuruluyor..."
    sudo apt install -y python3 python3-pip python3-venv
else
    echo "   ✅ Python3 zaten kurulu"
fi

# Node.js
if ! command -v node &> /dev/null; then
    echo "   → Node.js 18.x kuruluyor..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt install -y nodejs
else
    echo "   ✅ Node.js zaten kurulu: $(node --version)"
fi

# Diğer araçlar
echo "   → Yardımcı araçlar kuruluyor..."
sudo apt install -y curl unclutter xdotool

echo ""
echo "✅ Tüm paketler kuruldu"
echo ""

# 2. Script izinlerini ayarla
echo "🔐 Script izinleri ayarlanıyor..."
chmod +x "$PROJECT_DIR/start-pi.sh"
chmod +x "$PROJECT_DIR/backend/start.sh"
echo "✅ İzinler ayarlandı"
echo ""

# 3. Systemd service'i kur
echo "⚙️  Systemd service kuruluyor..."

# Service dosyasını güncelle (proje yolunu dinamik yap)
cat > /tmp/nutriquant-kiosk.service << EOF
[Unit]
Description=Nutriquant Kiosk Application
After=network.target graphical.target

[Service]
Type=simple
User=$USER
Environment="DISPLAY=:0"
Environment="XAUTHORITY=/home/$USER/.Xauthority"
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/start-pi.sh
Restart=always
RestartSec=10

[Install]
WantedBy=graphical.target
EOF

# Service'i kopyala ve etkinleştir
sudo cp /tmp/nutriquant-kiosk.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable nutriquant-kiosk.service

echo "✅ Service kuruldu ve etkinleştirildi"
echo ""

# 4. Autostart ayarları
echo "🖥️  Masaüstü ayarları yapılandırılıyor..."

# Autostart dizini
AUTOSTART_DIR="/home/$USER/.config/lxsession/LXDE-pi"
mkdir -p "$AUTOSTART_DIR"

# Autostart dosyası
cat > "$AUTOSTART_DIR/autostart" << 'EOF'
# Fare imlecini gizle
@unclutter -idle 0.1 -root

# Ekran koruyucuyu devre dışı bırak
@xset s off
@xset -dpms
@xset s noblank

# Masaüstü öğelerini gizle
@pcmanfm --desktop-off
EOF

echo "✅ Masaüstü ayarları yapılandırıldı"
echo ""

# 5. Özet
echo "============================================"
echo "✅ Kurulum Tamamlandı!"
echo "============================================"
echo ""
echo "📋 Yapılanlar:"
echo "   ✅ Gerekli paketler kuruldu"
echo "   ✅ Script izinleri ayarlandı"
echo "   ✅ Systemd service oluşturuldu"
echo "   ✅ Otomatik başlatma etkinleştirildi"
echo "   ✅ Masaüstü gizleme ayarları yapıldı"
echo ""
echo "🔄 Sonraki Adımlar:"
echo ""
echo "1. Otomatik giriş ayarlayın:"
echo "   sudo raspi-config"
echo "   → System Options → Boot / Auto Login → Desktop Autologin"
echo ""
echo "2. Raspberry Pi'yi yeniden başlatın:"
echo "   sudo reboot"
echo ""
echo "3. Yeniden başladıktan sonra uygulama otomatik açılacak!"
echo ""
echo "============================================"
echo "📚 Yönetim Komutları:"
echo "============================================"
echo ""
echo "Service'i durdur:"
echo "  sudo systemctl stop nutriquant-kiosk.service"
echo ""
echo "Service'i başlat:"
echo "  sudo systemctl start nutriquant-kiosk.service"
echo ""
echo "Service durumunu gör:"
echo "  sudo systemctl status nutriquant-kiosk.service"
echo ""
echo "Log'ları görüntüle:"
echo "  sudo journalctl -u nutriquant-kiosk.service -f"
echo ""
echo "============================================"
