#!/bin/bash

# Hızlı Github Yükleme Scripti
# Kullanım: ./push.sh "commit mesajınız"

if [ -z "$1" ]
then
    echo "Hata: Lütfen bir commit mesajı girin."
    echo "Örnek: ./push.sh \"yeni özellik eklendi\""
    exit 1
fi

echo "==================================="
echo "Github'a yükleniyor..."
echo "Mesaj: $1"
echo "==================================="

# Git komutları
git add .
git commit -m "$1"
git push origin main

if [ $? -eq 0 ]; then
    echo "==================================="
    echo "BAŞARILI! Değişiklikler yüklendi."
    echo "==================================="
else
    echo "==================================="
    echo "HATA! Yükleme başarısız oldu."
    echo "==================================="
fi
