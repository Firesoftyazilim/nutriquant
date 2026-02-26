#!/usr/bin/env python3
"""
GPIO3 Pin Test Script - Dokunmatik buton sinyalini test et
"""

import time
import sys

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    print("❌ RPi.GPIO bulunamadı - Raspberry Pi'de çalıştırın")
    sys.exit(1)

def test_gpio3_pin():
    """GPIO3 pininin durumunu sürekli oku"""
    
    pin = 3
    
    try:
        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        print(f"🔍 GPIO{pin} Pin Test Başlatıldı")
        print("📌 Pull-up resistor aktif")
        print("🔘 Dokunmatik butona bas/bırak - değişiklikleri gözlemle")
        print("❌ Ctrl+C ile çıkış\n")
        
        last_state = None
        press_count = 0
        
        while True:
            # Pin durumunu oku
            current_state = GPIO.input(pin)
            
            # Durum değişikliği varsa rapor et
            if current_state != last_state:
                state_text = "HIGH (3.3V)" if current_state == GPIO.HIGH else "LOW (0V/GND)"
                timestamp = time.strftime("%H:%M:%S")
                
                if current_state == GPIO.LOW:
                    press_count += 1
                    print(f"🔘 [{timestamp}] GPIO{pin}: {state_text} - BUTON BASILDI! (#{press_count})")
                else:
                    print(f"⚪ [{timestamp}] GPIO{pin}: {state_text} - Buton bırakıldı")
                
                last_state = current_state
            
            time.sleep(0.01)  # 10ms polling
            
    except KeyboardInterrupt:
        print(f"\n✅ Test tamamlandı. Toplam basma: {press_count}")
    except Exception as e:
        print(f"❌ GPIO hatası: {e}")
    finally:
        try:
            GPIO.cleanup()
            print("🧹 GPIO temizlendi")
        except:
            pass

def test_interrupt_detection():
    """Interrupt tabanlı test"""
    
    pin = 3
    press_count = 0
    
    def button_callback(channel):
        nonlocal press_count
        press_count += 1
        timestamp = time.strftime("%H:%M:%S")
        print(f"🚨 [{timestamp}] INTERRUPT! GPIO{pin} - Basma #{press_count}")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Hem FALLING hem RISING edge'i test et
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=button_callback, bouncetime=50)
        
        print(f"🎯 GPIO{pin} Interrupt Test Başlatıldı")
        print("📌 BOTH edge detection (FALLING + RISING)")
        print("🔘 Dokunmatik butona bas - interrupt'ları gözlemle")
        print("❌ Ctrl+C ile çıkış\n")
        
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print(f"\n✅ Interrupt test tamamlandı. Toplam interrupt: {press_count}")
    except Exception as e:
        print(f"❌ Interrupt hatası: {e}")
    finally:
        try:
            GPIO.remove_event_detect(pin)
            GPIO.cleanup()
            print("🧹 GPIO temizlendi")
        except:
            pass

if __name__ == "__main__":
    print("GPIO3 Dokunmatik Buton Test Menüsü")
    print("=" * 40)
    print("1. Pin durumu test (sürekli okuma)")
    print("2. Interrupt test (event detection)")
    print("3. Her ikisi de")
    
    choice = input("\nSeçiminiz (1/2/3): ").strip()
    
    if choice == "1":
        test_gpio3_pin()
    elif choice == "2":
        test_interrupt_detection()
    elif choice == "3":
        print("\n1. Pin durumu testi:")
        test_gpio3_pin()
        print("\n2. Interrupt testi:")
        test_interrupt_detection()
    else:
        print("❌ Geçersiz seçim")
