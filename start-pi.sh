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

# Venv yolunu belirle (backend içinde veya root'ta)
if [ -f "$BACKEND_DIR/venv/bin/activate" ]; then
    source "$BACKEND_DIR/venv/bin/activate"
elif [ -f "$PROJECT_DIR/venv/bin/activate" ]; then
    source "$PROJECT_DIR/venv/bin/activate"
else
    echo "❌ venv bulunamadı! Oluşturuluyor..."
    python3 -m venv "$PROJECT_DIR/venv"
    source "$PROJECT_DIR/venv/bin/activate"
fi

# Bağımlılıkları kontrol et ve yükle
echo "📦 Bağımlılıklar güncelleniyor..."
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install -r "$PROJECT_DIR/requirements.txt" > /dev/null
fi

cd "$BACKEND_DIR"
nohup python main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend başlatıldı (PID: $BACKEND_PID)"

# Backend hazır olsun - daha uzun bekleme ve health check
echo "⏳ Backend hazırlanıyor..."
sleep 3

# Backend'in hazır olduğunu kontrol et
echo "🔍 Backend health check yapılıyor..."
for i in {1..10}; do
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo "✅ Backend hazır!"
        break
    fi
    echo "   Deneme $i/10..."
    sleep 1
done

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

# Frontend'i build et (production)
echo "🔨 Frontend build ediliyor..."
if ! npm run build; then
    echo "❌ Frontend build hatası!"
    echo "📋 Build log'u kontrol edin"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Build kontrolü
if [ ! -d "dist" ]; then
    echo "❌ dist klasörü oluşmadı!"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

if [ ! -f "dist/index.html" ]; then
    echo "❌ dist/index.html bulunamadı!"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Frontend build başarılı"

# X11 display ayarla
export DISPLAY=:0

# NODE_ENV production olarak ayarla (ZORUNLU)
export NODE_ENV=production

# Electron'u production mode'da başlat
echo "🚀 Electron başlatılıyor (Production Mode)..."
echo "   NODE_ENV=$NODE_ENV"

# Electron'u npx ile çalıştır (global kurulum gerekmez)
NODE_ENV=production npx electron . 2>&1 | tee electron.log

# Cleanup
echo "🛑 Kapatılıyor..."
kill $BACKEND_PID 2>/dev/null || true
echo "✅ Tamamlandı"
