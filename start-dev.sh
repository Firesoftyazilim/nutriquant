#!/bin/bash

# ============================================
# Nutriquant Geliştirme Modu
# Backend + Frontend (DevTools açık)
# ============================================

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo "============================================"
echo "🔧 Nutriquant Geliştirme Modu"
echo "============================================"

# Backend başlat (arka planda)
echo "🐍 Backend başlatılıyor..."
cd "$BACKEND_DIR"

if [ -d "venv" ]; then
    source venv/bin/activate
    python main.py &
    BACKEND_PID=$!
    echo "✅ Backend başlatıldı (PID: $BACKEND_PID)"
else
    echo "❌ Backend venv bulunamadı. Önce ./start.sh çalıştırın"
    exit 1
fi

# Frontend başlat
echo "⚛️  Frontend başlatılıyor..."
cd "$FRONTEND_DIR"

if [ -d "node_modules" ]; then
    # Vite dev server + Electron
    npm run electron:dev
else
    echo "❌ Frontend node_modules bulunamadı. Önce ./start.sh çalıştırın"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Cleanup
echo "🛑 Kapatılıyor..."
kill $BACKEND_PID 2>/dev/null || true
echo "✅ Tamamlandı"
