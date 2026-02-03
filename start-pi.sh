#!/bin/bash

# ============================================
# Nutriquant Raspberry Pi Başlatma Scripti
# Chromium Kiosk Mode
# ============================================

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo "============================================"
echo "🍓 Nutriquant Raspberry Pi Kiosk Modu"
echo "============================================"

# Cleanup fonksiyonu
cleanup() {
    echo ""
    echo "🛑 Kapatılıyor..."
    
    # Frontend'i kapat
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "   Frontend durduruluyor (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    # Backend'i kapat
    if [ ! -z "$BACKEND_PID" ]; then
        echo "   Backend durduruluyor (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    # Chromium'u kapat
    echo "   Chromium kapatılıyor..."
    pkill -f "chromium.*kiosk" 2>/dev/null || true
    
    echo "✅ Tamamlandı"
    exit 0
}

# SIGINT ve SIGTERM yakalandığında cleanup çalıştır
trap cleanup SIGINT SIGTERM

# 1. Backend'i başlat (backend/start.sh kullanarak)
echo ""
echo "� Backend başlatılıyor (backend/start.sh)..."
cd "$BACKEND_DIR"

# Backend start.sh'ı arka planda çalıştır
if [ -f "start.sh" ]; then
    chmod +x start.sh
    nohup ./start.sh > backend.log 2>&1 &
    BACKEND_PID=$!
    echo "✅ Backend başlatıldı (PID: $BACKEND_PID)"
else
    echo "❌ backend/start.sh bulunamadı!"
    exit 1
fi

# Backend hazır olsun
echo "⏳ Backend hazırlanıyor..."
sleep 5

# Backend health check
echo "🔍 Backend health check..."
for i in {1..15}; do
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo "✅ Backend hazır!"
        break
    fi
    echo "   Deneme $i/15..."
    sleep 1
    
    if [ $i -eq 15 ]; then
        echo "❌ Backend başlatılamadı!"
        echo "📋 Backend log:"
        tail -20 backend.log
        cleanup
    fi
done

# 2. Frontend'i başlat (Vite dev server)
echo ""
echo "🎨 Frontend başlatılıyor (Vite dev server)..."
cd "$FRONTEND_DIR"

# Node.js kontrolü
if ! command -v node &> /dev/null; then
    echo "❌ Node.js bulunamadı!"
    echo "Lütfen Node.js kurun: curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt install -y nodejs"
    cleanup
fi

# npm bağımlılıkları kontrolü
if [ ! -d "node_modules" ]; then
    echo "📦 Frontend bağımlılıkları yükleniyor..."
    npm install
fi

# Vite dev server'ı arka planda başlat
echo "� Vite dev server başlatılıyor..."
nohup npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend başlatıldı (PID: $FRONTEND_PID)"

# Frontend hazır olsun
echo "⏳ Frontend hazırlanıyor..."
sleep 5

# Frontend health check
echo "� Frontend health check..."
for i in {1..15}; do
    if curl -s http://localhost:5173 > /dev/null 2>&1; then
        echo "✅ Frontend hazır!"
        break
    fi
    echo "   Deneme $i/15..."
    sleep 1
    
    if [ $i -eq 15 ]; then
        echo "❌ Frontend başlatılamadı!"
        echo "📋 Frontend log:"
        tail -20 frontend.log
        cleanup
    fi
done

# 3. Chromium'u kiosk modda aç
echo ""
echo "🌐 Chromium kiosk mode başlatılıyor..."
echo "   URL: http://localhost:5173"

# X11 display ayarla
export DISPLAY=:0

# Chromium'u kiosk modda başlat (mobil dokunmatik mod)
# Dokunmatik kaydırma ve mobil davranış için optimize edilmiş
chromium-browser \
  --kiosk \
  --app=http://localhost:5173 \
  --user-data-dir=/home/pi/kiosk-profile \
  --window-size=800,480 \
  --window-position=0,0 \
  --force-device-scale-factor=1 \
  --disable-gpu \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --disable-translate \
  --disable-features=Translate,TranslateUI \
  --disable-background-networking \
  --disable-sync \
  --disable-component-update \
  --no-first-run \
  --noerrdialogs \
  --check-for-update-interval=604800 \
  --touch-events=enabled \
  --enable-features=OverlayScrollbar,TouchEventFeatureDetection \
  --enable-blink-features=PointerEvent,TouchEventFeatureDetection \
  --use-mobile-user-agent \
  --user-agent="Mozilla/5.0 (Linux; Android 10; Tablet) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"

# Chromium kapandığında cleanup
cleanup
