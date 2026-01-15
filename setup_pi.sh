#!/bin/bash

print_message() {
    echo "========================================="
    echo "$1"
    echo "========================================="
}

print_message "Nutriquant Kurulum Sihirbazı"

# Sanal ortam kontrolü
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_message "UYARI: Sanal ortam (venv) aktif değil!"
    echo "Lütfen önce 'source venv/bin/activate' komutunu çalıştırın."
    exit 1
fi

print_message "Gerekli Paketler Yükleniyor..."
pip3 install pygame hx711 RPi.GPIO numpy pillow

print_message "Ek Paketler Yükleniyor..."
# requirements.txt varsa oradan da dene
if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt
fi

print_message "Kurulum Tamamlandı!"
echo "Uygulamayı başlatmak için:"
echo "python3 main.py"
