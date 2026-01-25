#!/bin/bash

# ============================================
# Sadece Backend Başlatma Scripti
# ============================================

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"

echo "============================================"
echo "🐍 Backend Başlatılıyor..."
echo "============================================"

cd "$BACKEND_DIR"

# Virtual environment kontrolü
if [ ! -d "venv" ]; then
    echo "❌ Backend venv bulunamadı!"
    echo "   Lütfen önce ./start.sh çalıştırın (ilk kurulum için)"
    exit 1
fi

# Virtual environment'ı aktifleştir
source venv/bin/activate

# Backend'i başlat
echo ""
echo "✅ Backend başlatılıyor..."
echo "📡 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo ""
echo "Durdurmak için: Ctrl+C"
echo ""

python main.py
