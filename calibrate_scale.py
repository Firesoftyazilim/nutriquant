# HX711 Kalibrasyon Scripti

import time
import sys
from hardware.scale import Scale
from config import HX711_REFERENCE_UNIT

def cleanAndExit():
    print("Temizleniyor...")
    sys.exit()

print("Nutriquant - Tartı Kalibrasyonu")
print("-------------------------------")



print("\n1. Lütfen tartının üzerini BOŞALTIN.")
input("Devam etmek için Enter'a basın...")

scale.tare()
print("Dara alındı (Sıfırlandı).")

print("\n2. Bilinen bir ağırlığı (örn: telefon, su şişesi) tartıya koyun.")
target_weight = 0
while True:
    try:
        val = input("Koyduğunuz ağırlığı gram cinsinden yazın (örn: 200): ")
        target_weight = float(val)
        if target_weight > 0:
            break
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")

print(f"\n{target_weight}g ağırlık için kalibrasyon yapılıyor...")
print("Lütfen bekleyin...")

# 10 örnek alıp ortalama reference unit hesapla
ref_unit = scale.calibrate(target_weight)

print(f"\n[SONUÇ] Yeni Reference Unit değeri: {getattr(ref_unit, 'real', ref_unit)}") # Karmaşık sayı koruması
print(f"Eski Reference Unit: {HX711_REFERENCE_UNIT}")

print("\n[GÖREV] Bu değeri kullanmak için:")
print(f"1. `config.py` dosyasını açın")
print(f"2. `HX711_REFERENCE_UNIT = {int(ref_unit)}` olarak değiştirin")
print("3. Kaydedip çıkın.")

print("\nTest için ağırlık okunuyor (Ctrl+C ile çıkış)...")
try:
    while True:
        val = scale.read_weight()
        print(f"Okunan: {val}g")
        time.sleep(0.5)
except KeyboardInterrupt:
    cleanAndExit()
