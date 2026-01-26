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

# Mac için sadece gerekli bağımlılıkları yükle (Pi donanım kütüphaneleri hariç)
echo "📦 Mac için bağımlılıklar yükleniyor..."
pip install --quiet fastapi==0.115.0 uvicorn[standard]==0.32.0 python-multipart==0.0.12 \
    websockets==13.1 opencv-python-headless>=4.8.0 Pillow>=10.2.0 numpy>=1.26.0 \
    pydantic==2.10.0 python-json-logger==2.0.7 python-dotenv==1.0.0 pydub==0.25.1

# TensorFlow Lite için tensorflow yükle (Mac'te tflite-runtime yok)
echo "📦 TensorFlow yükleniyor (AI için)..."
pip install --quiet tensorflow>=2.16.0

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
