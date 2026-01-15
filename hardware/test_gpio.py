import RPi.GPIO as GPIO
import time

DOUT_PIN = 5
SCK_PIN = 6

def test_pins():
    print(f"Testing GPIO Pins: DOUT={DOUT_PIN}, SCK={SCK_PIN}")
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DOUT_PIN, GPIO.IN)
    GPIO.setup(SCK_PIN, GPIO.OUT)
    
    print("Checking DOUT pin state for 5 seconds...")
    start_time = time.time()
    changes = 0
    last_val = -1
    
    try:
        while time.time() - start_time < 5:
            val = GPIO.input(DOUT_PIN)
            if val != last_val:
                print(f"[{time.time()-start_time:.2f}s] DOUT changed to: {val}")
                last_val = val
                changes += 1
            time.sleep(0.1)
            
        print("\nTest Complete.")
        if changes == 0:
            print(f"WARNING: DOUT pin stayed at {last_val} constantly.")
            print("Possible causes:")
            print("1. Sensor broken or not powered")
            print("2. Wiring disconnected")
            print("3. Wrong pin number")
        else:
            print(f"good news: DOUT pin changed state {changes} times.")
            
    except KeyboardInterrupt:
        print("\nTest cancelled.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    test_pins()
