# Nutriquant - Raspberry Pi 4 Konfigürasyon

# Uygulama
APP_NAME = "Nutriquant"
VERSION = "1.0.0"
LANGUAGE = "tr"

# Ekran (4.3" Dokunmatik)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
FULLSCREEN = True
FPS = 30

# HX711 Tartı Modülü GPIO
HX711_DOUT_PIN = 5
HX711_SCK_PIN = 6
HX711_REFERENCE_UNIT = 210  # Kalibrasyon sonrası güncellenecek
MAX_WEIGHT_KG = 5.0
TARE_SAMPLES = 10

# Kamera Modülü
CAMERA_RESOLUTION = (640, 480)
CAMERA_FORMAT = "RGB888"
CAMERA_ROTATION = 0

# AI Model
MODEL_PATH = "models/food_classifier.tflite"
LABELS_PATH = "models/labels.txt"
CONFIDENCE_THRESHOLD = 0.7
INPUT_SIZE = (224, 224)

# LED Ring (WS2812B - GPIO 18)
LED_PIN = 18
LED_COUNT = 24
LED_BRIGHTNESS = 128

# Hoparlör (USB Ses Kartı)
SOUND_DEVICE = "default"
VOLUME = 80

# UPS HAT (I2C)
UPS_I2C_BUS = 1
UPS_I2C_ADDRESS = 0x36
BATTERY_LOW_THRESHOLD = 20
BATTERY_CRITICAL_THRESHOLD = 10

# Ölçüm Limitleri
MEASUREMENT_LIMIT = 50
MIN_WEIGHT_THRESHOLD = 10  # gram

# VKİ Yaş Grupları
AGE_BMI_RULES = {
    "child": (5, 18),
    "adult": (19, 64),
    "senior": (65, 120)
}

# Veri Yolları
DATA_DIR = "data"
ASSETS_DIR = "assets"
MODELS_DIR = "models"
WALLPAPERS_DIR = "assets/images/Wallpapers"

