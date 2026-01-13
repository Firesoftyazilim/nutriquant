#!/bin/bash
# Nutriquant Kurulum Scripti - Raspberry Pi 4

echo "Nutriquant kurulumu başlatılıyor..."

# Sistem güncellemesi
echo "Sistem güncelleniyor..."
sudo apt-get update
sudo apt-get upgrade -y

# Python ve pip
echo "Python kurulumu kontrol ediliyor..."
sudo apt-get install -y python3 python3-pip python3-dev

# Sistem kütüphaneleri
echo "Sistem kütüphaneleri kuruluyor..."
sudo apt-get install -y \
    libatlas-base-dev \
    libopenjp2-7 \
    libtiff5 \
    libhdf5-dev \
    libportaudio2 \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev

# I2C ve GPIO aktifleştir
echo "I2C ve GPIO aktifleştiriliyor..."
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_camera 0

# Python bağımlılıkları
echo "Python paketleri kuruluyor..."
pip3 install -r requirements.txt

# Data klasörü oluştur
mkdir -p data
mkdir -p models
mkdir -p assets/sounds
mkdir -p assets/fonts
mkdir -p assets/icons
mkdir -p assets/images

# İzinler
chmod +x main.py

echo ""
echo "Kurulum tamamlandı!"
echo ""
echo "Kullanım:"
echo "  python3 main.py"
echo ""
echo "Not: TensorFlow Lite modelini models/food_classifier.tflite yoluna yerleştirin"
