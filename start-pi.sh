#!/bin/bash

# ============================================
# Nutriquant Raspberry Pi Başlatma Scripti
# Production Mode - Tam Ekran Kiosk
# ============================================

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo "============================================"
echo "🍓 Nutriquant Raspberry Pi Modu"
echo "============================================"

# Backend başlat (arka planda)
echo "🐍 Backend başlatılıyor..."
cd "$BACKEND_DIR"

# Virtual environment kontrolü
if [ ! -d "venv" ]; then
    echo "❌ Backend venv bulunamadı!"
    echo "   Lütfen önce ./start.sh çalıştırın (ilk kurulum için)"
    exit 1
fi

source venv/bin/activate
python main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend başlatıldı (PID: $BACKEND_PID)"

# Backend hazır olsun
echo "⏳ Backend hazırlanıyor..."
sleep 5

# Frontend başlat (tam ekran)
echo "🎨 Frontend başlatılıyor (TAM EKRAN)..."
cd "$FRONTEND_DIR"

# Node.js kontrolü ve otomatik kurulum
if ! command -v node &> /dev/null; then
    echo "⚙️  Node.js bulunamadı, kuruluyor..."
    echo "   Node.js 18.x repository ekleniyor..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    echo "   Node.js kuruluyor..."
    sudo apt install -y nodejs
    
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js kurulumu başarısız!"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
    echo "✅ Node.js kuruldu: $(node --version)"
fi

# npm bağımlılıkları kontrolü
if [ ! -d "node_modules" ]; then
    echo "⚙️  Frontend kütüphaneleri yükleniyor..."
    npm install
fi

# X11 display ayarla
export DISPLAY=:0

# Electron'u tam ekran başlat (build dahil)
npm run electron

# Cleanup
echo "🛑 Kapatılıyor..."
kill $BACKEND_PID 2>/dev/null || true
echo "✅ Tamamlandı"
