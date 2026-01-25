#!/bin/bash

# ============================================
# Nutriquant Başlatma Scripti
# Electron + React + Python FastAPI
# ============================================

set -e  # Hata durumunda dur

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo "============================================"
echo "🚀 Nutriquant Başlatılıyor..."
echo "============================================"

# ==================== RENK KODLARI ====================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ==================== BACKEND KURULUM ====================

echo ""
echo -e "${BLUE}📦 Backend Kurulumu Kontrol Ediliyor...${NC}"
echo ""

cd "$BACKEND_DIR"

# Python virtual environment kontrolü
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚙️  Python virtual environment oluşturuluyor...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment oluşturuldu${NC}"
fi

# Virtual environment'ı aktifleştir
source venv/bin/activate

# Pip güncelle
echo -e "${YELLOW}⚙️  Pip güncelleniyor...${NC}"
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo -e "${GREEN}✅ Pip güncellendi${NC}"

# Backend bağımlılıklarını kontrol et
if [ ! -f "venv/.installed" ]; then
    echo -e "${YELLOW}⚙️  Backend kütüphaneleri yükleniyor...${NC}"
    echo -e "${YELLOW}   (Bu işlem birkaç dakika sürebilir)${NC}"
    
    # Raspberry Pi'ye özel paketleri atla (macOS/Linux'ta)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS - Raspberry Pi paketlerini atla
        pip install fastapi uvicorn[standard] python-multipart websockets \
                    opencv-python Pillow numpy tensorflow pydub \
                    python-json-logger python-dotenv pydantic > /dev/null 2>&1
    else
        # Linux (Raspberry Pi) - Tüm paketleri yükle
        pip install -r requirements.txt > /dev/null 2>&1
    fi
    
    touch venv/.installed
    echo -e "${GREEN}✅ Backend kütüphaneleri yüklendi${NC}"
else
    echo -e "${GREEN}✅ Backend kütüphaneleri zaten yüklü${NC}"
fi

# ==================== FRONTEND KURULUM ====================

echo ""
echo -e "${BLUE}📦 Frontend Kurulumu Kontrol Ediliyor...${NC}"
echo ""

cd "$FRONTEND_DIR"

# Node.js kontrolü ve otomatik kurulum
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚙️  Node.js bulunamadı, kuruluyor...${NC}"
    
    # Platform tespiti
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux (Raspberry Pi / Ubuntu / Debian)
        echo -e "${YELLOW}   Node.js 18.x repository ekleniyor...${NC}"
        curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
        echo -e "${YELLOW}   Node.js kuruluyor...${NC}"
        sudo apt install -y nodejs
        echo -e "${GREEN}✅ Node.js kuruldu!${NC}"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo -e "${YELLOW}   Homebrew ile Node.js kuruluyor...${NC}"
            brew install node
            echo -e "${GREEN}✅ Node.js kuruldu!${NC}"
        else
            echo -e "${RED}❌ Homebrew bulunamadı!${NC}"
            echo -e "${YELLOW}   Manuel kurulum: https://nodejs.org${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Desteklenmeyen platform!${NC}"
        echo -e "${YELLOW}   Manuel kurulum: https://nodejs.org${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Node.js bulundu: $(node --version)${NC}"

# npm bağımlılıklarını kontrol et
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚙️  Frontend kütüphaneleri yükleniyor...${NC}"
    echo -e "${YELLOW}   (Bu işlem birkaç dakika sürebilir)${NC}"
    npm install > /dev/null 2>&1
    echo -e "${GREEN}✅ Frontend kütüphaneleri yüklendi${NC}"
else
    echo -e "${GREEN}✅ Frontend kütüphaneleri zaten yüklü${NC}"
fi

# ==================== BACKEND BAŞLAT ====================

echo ""
echo -e "${BLUE}🔧 Backend Başlatılıyor...${NC}"
echo ""

cd "$BACKEND_DIR"
source venv/bin/activate

# Backend'i arka planda başlat
python main.py > backend.log 2>&1 &
BACKEND_PID=$!

echo -e "${GREEN}✅ Backend başlatıldı (PID: $BACKEND_PID)${NC}"
echo -e "${GREEN}   API: http://localhost:8000${NC}"

# Backend'in hazır olmasını bekle
echo -e "${YELLOW}⏳ Backend hazırlanıyor...${NC}"
sleep 3

# ==================== FRONTEND BAŞLAT ====================

echo ""
echo -e "${BLUE}🎨 Frontend Başlatılıyor...${NC}"
echo ""

cd "$FRONTEND_DIR"

# Geliştirme modunda mı yoksa production'da mı?
if [ "$1" == "--dev" ]; then
    echo -e "${YELLOW}🔧 Geliştirme modu (DevTools açık)${NC}"
    NODE_ENV=development npm run electron:dev
else
    echo -e "${GREEN}🚀 Production modu (Tam ekran)${NC}"
    # Önce build yap
    if [ ! -d "dist" ]; then
        echo -e "${YELLOW}⚙️  Frontend build ediliyor...${NC}"
        npm run build > /dev/null 2>&1
        echo -e "${GREEN}✅ Build tamamlandı${NC}"
    fi
    NODE_ENV=production npm run electron
fi

# ==================== CLEANUP ====================

echo ""
echo -e "${YELLOW}🛑 Uygulama kapatılıyor...${NC}"

# Backend'i durdur
if [ ! -z "$BACKEND_PID" ]; then
    kill $BACKEND_PID 2>/dev/null || true
    echo -e "${GREEN}✅ Backend durduruldu${NC}"
fi

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}👋 Nutriquant kapatıldı. Görüşmek üzere!${NC}"
echo -e "${GREEN}============================================${NC}"
