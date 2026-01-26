#!/bin/bash

# ============================================
# Nutriquant Development Mode
# Vite Dev Server + Electron
# ============================================

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo "============================================"
echo "🔧 Nutriquant Development Mode"
echo "============================================"

# Backend başlat (arka planda)
echo "🐍 Backend başlatılıyor..."

# Venv yolunu belirle
if [ -f "$BACKEND_DIR/venv/bin/activate" ]; then
    source "$BACKEND_DIR/venv/bin/activate"
elif [ -f "$PROJECT_DIR/venv/bin/activate" ]; then
    source "$PROJECT_DIR/venv/bin/activate"
else
    echo "❌ venv bulunamadı! Oluşturuluyor..."
    python3 -m venv "$PROJECT_DIR/venv"
    source "$PROJECT_DIR/venv/bin/activate"
fi

# Bağımlılıkları kontrol et
echo "📦 Bağımlılıklar güncelleniyor..."
if [ -f "$BACKEND_DIR/requirements.txt" ]; then
    pip install -r "$BACKEND_DIR/requirements.txt" > /dev/null
fi

cd "$BACKEND_DIR"
python main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend başlatıldı (PID: $BACKEND_PID)"

# Backend hazır olsun
echo "⏳ Backend hazırlanıyor..."
sleep 3

# Frontend başlat (development mode)
echo "🎨 Frontend başlatılıyor (Development Mode)..."
cd "$FRONTEND_DIR"

# npm bağımlılıkları kontrolü
if [ ! -d "node_modules" ]; then
    echo "⚙️  Frontend kütüphaneleri yükleniyor..."
    npm install
fi

# X11 display ayarla (Linux için)
export DISPLAY=:0

# NODE_ENV development olarak ayarla
export NODE_ENV=development

# Vite dev server + Electron'u başlat
echo "🚀 Vite + Electron başlatılıyor..."
npm run electron:dev

# Cleanup
echo "🛑 Kapatılıyor..."
kill $BACKEND_PID 2>/dev/null || true
echo "✅ Tamamlandı"
