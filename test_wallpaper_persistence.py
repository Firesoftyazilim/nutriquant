#!/usr/bin/env python3
# Arka Plan Kalıcılık Testi

from core.database import Database

def test_wallpaper_persistence():
    """Arka plan kaydetme ve yükleme testleri"""
    
    print("=" * 50)
    print("ARKA PLAN KALICILIK TESTİ")
    print("=" * 50)
    
    db = Database()
    
    # Test 1: Varsayılan ayarlar
    print("\n1. Varsayılan ayarları kontrol et...")
    settings = db.get_settings()
    print(f"   Ayarlar: {settings}")
    print(f"   Wallpaper: {settings.get('wallpaper')}")
    
    # Test 2: Arka plan kaydet
    print("\n2. Arka plan kaydet (test_wallpaper.jpg)...")
    db.save_wallpaper("test_wallpaper.jpg")
    
    # Test 3: Kaydedilen arka planı yükle
    print("\n3. Kaydedilen arka planı yükle...")
    saved_wallpaper = db.get_wallpaper()
    print(f"   Yüklenen: {saved_wallpaper}")
    
    if saved_wallpaper == "test_wallpaper.jpg":
        print("   ✓ Başarılı!")
    else:
        print("   ✗ Hata: Beklenen değer bulunamadı")
    
    # Test 4: Varsayılana dön (None)
    print("\n4. Varsayılan arka plana dön...")
    db.save_wallpaper(None)
    saved_wallpaper = db.get_wallpaper()
    print(f"   Yüklenen: {saved_wallpaper}")
    
    if saved_wallpaper is None:
        print("   ✓ Başarılı!")
    else:
        print("   ✗ Hata: None bekleniyor")
    
    # Test 5: Farklı bir arka plan
    print("\n5. Farklı arka plan kaydet (nature.png)...")
    db.save_wallpaper("nature.png")
    saved_wallpaper = db.get_wallpaper()
    print(f"   Yüklenen: {saved_wallpaper}")
    
    if saved_wallpaper == "nature.png":
        print("   ✓ Başarılı!")
    else:
        print("   ✗ Hata: Beklenen değer bulunamadı")
    
    # Test 6: Tüm ayarları göster
    print("\n6. Tüm ayarlar:")
    all_settings = db.get_settings()
    for key, value in all_settings.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 50)
    print("TEST TAMAMLANDI")
    print("=" * 50)
    print("\nNot: Ayarlar 'data/settings.json' dosyasında saklanıyor.")
    print("Uygulama kapanıp açıldığında bu ayarlar korunacak.")

if __name__ == "__main__":
    test_wallpaper_persistence()
