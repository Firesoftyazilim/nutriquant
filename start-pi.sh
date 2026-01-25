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

# X11 display ayarla
export DISPLAY=:0

# Electron'u tam ekran başlat
NODE_ENV=production npm run electron

# Cleanup
echo "🛑 Kapatılıyor..."
kill $BACKEND_PID 2>/dev/null || true
echo "✅ Tamamlandı"
