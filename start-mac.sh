#!/bin/bash

# ============================================
# Nutriquant Mac Development Mode
# Backend + Frontend (Browser)
# ============================================

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo "============================================"
echo "💻 Nutriquant Mac Development Mode"
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
echo "   → http://localhost:8000"
echo "   → http://localhost:8000/docs"

# Backend hazır olsun
sleep 2

# Frontend başlat
echo ""
echo "🎨 Frontend başlatılıyor..."
cd "$FRONTEND_DIR"

# npm bağımlılıkları kontrolü
if [ ! -d "node_modules" ]; then
    echo "⚙️  Frontend kütüphaneleri yükleniyor..."
    npm install
fi

echo ""
echo "✅ Hazır!"
echo "   → Frontend: http://localhost:5173"
echo "   → Backend API: http://localhost:8000"
echo ""
echo "Ctrl+C ile durdurun"
echo ""

# Vite dev server'ı başlat (foreground)
npm run dev

# Cleanup (Ctrl+C sonrası)
echo ""
echo "🛑 Kapatılıyor..."
kill $BACKEND_PID 2>/dev/null || true
echo "✅ Tamamlandı"
