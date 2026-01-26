#!/bin/bash

# Scriptin bulunduğu dizin (backend)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."

echo "🚀 Nutriquant Backend Başlatıcı"
echo "==============================="

# 1. Sanal Ortamı (venv) Bul ve Aktifleştir
# Önce backend içinde ara, yoksa üst dizinde ara
if [ -d "$SCRIPT_DIR/venv" ]; then
    VENV_PATH="$SCRIPT_DIR/venv"
elif [ -d "$PROJECT_ROOT/venv" ]; then
    VENV_PATH="$PROJECT_ROOT/venv"
else
    echo "❌ Hata: Sanal ortam ('venv') bulunamadı!"
    echo "Lütfen proje ana dizininde 'python3 -m venv venv' komutu ile oluşturun."
    exit 1
fi

echo "✅ Sanal ortam bulundu: $VENV_PATH"
source "$VENV_PATH/bin/activate"

# 2. Kütüphaneleri Yükle
echo "📦 Kütüphaneler kontrol ediliyor ve yükleniyor..."
# Backend dizinindeki requirements.txt'yi öncelikli kullan
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo "   -> Backend dizinindeki requirements.txt kullanılıyor."
    pip install -r "$SCRIPT_DIR/requirements.txt"
elif [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    echo "   -> Ana dizindeki requirements.txt kullanılıyor."
    pip install -r "$PROJECT_ROOT/requirements.txt"
else 
    echo "⚠️ Uyarı: requirements.txt bulunamadı, kütüphane kurulumu atlanıyor."
fi

# 3. Backend'i Başlat
echo "🔥 Sunucu başlatılıyor..."
echo "   -> http://localhost:8000"
echo "   -> http://localhost:8000/docs"
cd "$SCRIPT_DIR" || exit

# Python ile başlat (main.py içindeki uvicorn yapılandırmasını kullanır)
python main.py
