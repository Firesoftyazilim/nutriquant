"""
Nutriquant Backend API
FastAPI + WebSocket - Raspberry Pi Sensör Kontrolü
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import asyncio
import io
import sys
import os
from typing import Optional, List
from datetime import datetime

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hardware.scale import Scale
from hardware.camera import Camera
from hardware.battery import Battery
from hardware.speaker import Speaker
from ai.food_recognition import FoodRecognizer
from core.nutrition import NutritionCalculator
from core.bmi import BMICalculator
from core.database import Database

# FastAPI App
app = FastAPI(title="Nutriquant API", version="2.0.0")

# CORS - Electron'dan erişim için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hardware ve AI sınıfları (singleton)
scale = Scale()
camera = Camera()
battery = Battery()
speaker = Speaker()
recognizer = FoodRecognizer()
nutrition_calc = NutritionCalculator()
bmi_calc = BMICalculator()
db = Database()

# Pydantic Models
class ProfileCreate(BaseModel):
    name: str
    gender: str
    height: int
    weight: int

class ProfileUpdate(BaseModel):
    name: str
    gender: str
    height: int
    weight: int

class AnalyzeRequest(BaseModel):
    weight: float
    profile_id: Optional[int] = None

class SaveMeasurementRequest(BaseModel):
    user_id: int
    food_name: str
    weight: float
    nutrition: dict
    bmi_data: dict

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    """API Sağlık Kontrolü"""
    return {
        "app": "Nutriquant Backend",
        "version": "2.0.0",
        "status": "running",
        "hardware_mode": scale.mode
    }

@app.get("/api/health")
async def health_check():
    """Sistem sağlık durumu"""
    return {
        "battery": battery.get_percentage(),
        "scale_mode": scale.mode,
        "camera_mode": "mock" if camera.mock_mode else "real",
        "timestamp": datetime.now().isoformat()
    }

# ==================== SCALE ====================

@app.get("/api/scale/weight")
async def get_weight():
    """Anlık ağırlık oku"""
    weight = scale.read_weight()
    return {"weight": weight, "unit": "g"}

@app.post("/api/scale/tare")
async def tare_scale():
    """Tartıyı sıfırla"""
    scale.tare()
    return {"status": "success", "message": "Tartı sıfırlandı"}

@app.websocket("/ws/weight")
async def websocket_weight(websocket: WebSocket):
    """Gerçek zamanlı ağırlık stream'i (WebSocket)"""
    await websocket.accept()
    try:
        while True:
            weight = scale.read_weight()
            await websocket.send_json({
                "weight": weight,
                "timestamp": datetime.now().isoformat()
            })
            await asyncio.sleep(0.1)  # 10 Hz
    except WebSocketDisconnect:
        print("WebSocket bağlantısı kesildi")
    except Exception as e:
        print(f"WebSocket hatası: {e}")

# ==================== CAMERA ====================

@app.get("/api/camera/capture")
async def capture_image():
    """Fotoğraf çek ve döndür"""
    try:
        image_array = camera.capture_image()
        from PIL import Image
        
        # Numpy array'i PIL Image'e çevir
        pil_image = Image.fromarray(image_array)
        
        # BytesIO'ya kaydet
        img_io = io.BytesIO()
        pil_image.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        
        return StreamingResponse(img_io, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kamera hatası: {str(e)}")

@app.post("/api/camera/preview/start")
async def start_camera_preview():
    """Kamera önizlemesi başlat"""
    success = camera.start_preview()
    return {"status": "success" if success else "failed"}

@app.post("/api/camera/preview/stop")
async def stop_camera_preview():
    """Kamera önizlemesi durdur"""
    camera.stop_preview()
    return {"status": "success"}

# ==================== AI & ANALYSIS ====================

@app.post("/api/analyze")
async def analyze_food(request: AnalyzeRequest):
    """Yemek analizi yap (AI + Besin Hesaplama)"""
    try:
        # Ses efekti
        speaker.play_beep()
        
        # Fotoğraf çek
        image = camera.capture_image()
        
        # AI ile tanı
        food_key, confidence = recognizer.recognize(image)
        
        if not food_key:
            speaker.play_warning()
            return {
                "status": "not_recognized",
                "confidence": confidence,
                "message": "Yemek tanınamadı"
            }
        
        # Besin değerlerini hesapla
        nutrition = nutrition_calc.calculate(food_key, max(request.weight, 100))
        
        if not nutrition:
            return {
                "status": "error",
                "message": "Besin değerleri bulunamadı"
            }
        
        # BMI hesapla (profil varsa)
        bmi_data = None
        if request.profile_id:
            profiles = db.get_all_profiles()
            profile = next((p for p in profiles if p['id'] == request.profile_id), None)
            if profile:
                bmi = bmi_calc.calculate(profile['weight'], profile['height'])
                bmi_comment = bmi_calc.get_comment(bmi, 30)  # Yaş varsayılan
                bmi_data = {"bmi": bmi, "comment": bmi_comment}
        
        # Başarı efekti
        speaker.play_success()
        
        return {
            "status": "success",
            "food_key": food_key,
            "confidence": confidence,
            "nutrition": nutrition,
            "bmi": bmi_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== PROFILES ====================

@app.get("/api/profiles")
async def get_profiles():
    """Tüm profilleri getir"""
    profiles = db.get_all_profiles()
    return {"profiles": profiles}

@app.post("/api/profiles")
async def create_profile(profile: ProfileCreate):
    """Yeni profil oluştur"""
    new_profile = db.add_profile(
        profile.name,
        profile.gender,
        profile.height,
        profile.weight
    )
    speaker.play_success()
    return new_profile

@app.put("/api/profiles/{profile_id}")
async def update_profile(profile_id: int, profile: ProfileUpdate):
    """Profil güncelle"""
    db.update_profile(
        profile_id,
        profile.name,
        profile.gender,
        profile.height,
        profile.weight
    )
    speaker.play_success()
    return {"status": "success", "profile_id": profile_id}

@app.delete("/api/profiles/{profile_id}")
async def delete_profile(profile_id: int):
    """Profil sil"""
    db.delete_profile(profile_id)
    speaker.play_success()
    return {"status": "success"}

# ==================== DATABASE ====================

@app.post("/api/measurements")
async def save_measurement(request: SaveMeasurementRequest):
    """Ölçüm kaydet"""
    success = db.add_measurement(
        request.user_id,
        request.food_name,
        request.weight,
        request.nutrition,
        request.bmi_data
    )
    return {"status": "success" if success else "failed"}

@app.get("/api/measurements")
async def get_measurements():
    """Tüm ölçümleri getir"""
    measurements = db.load_json("measurements.json", {"measurements": []})
    return measurements

# ==================== SETTINGS ====================

@app.get("/api/settings")
async def get_settings():
    """Ayarları getir"""
    settings = db.get_settings()
    return settings

@app.post("/api/settings/wallpaper")
async def set_wallpaper(wallpaper: dict):
    """Arka plan ayarla"""
    db.save_wallpaper(wallpaper.get("name"))
    return {"status": "success"}

# ==================== HARDWARE CONTROL ====================



@app.post("/api/speaker/{sound}")
async def play_sound(sound: str):
    """Ses çal"""
    sounds = {
        "beep": speaker.play_beep,
        "success": speaker.play_success,
        "warning": speaker.play_warning,
        "ready": speaker.play_ready,
        "startup": speaker.play_startup_music
    }
    
    if sound in sounds:
        sounds[sound]()
        return {"status": "success", "sound": sound}
    else:
        raise HTTPException(status_code=400, detail="Geçersiz ses")

@app.get("/api/battery")
async def get_battery():
    """Batarya durumu"""
    return {
        "percentage": battery.get_percentage(),
        "voltage": battery.get_voltage(),
        "is_charging": battery.is_charging()
    }

# ==================== STARTUP & SHUTDOWN ====================

@app.on_event("startup")
async def startup_event():
    """Uygulama başlangıcı"""
    print("🚀 Nutriquant Backend başlatıldı")
    print(f"   Scale Mode: {scale.mode}")
    print(f"   Camera Mode: {'Mock' if camera.mock_mode else 'Real'}")

@app.on_event("shutdown")
async def shutdown_event():
    """Uygulama kapanışı"""
    print("🛑 Nutriquant Backend kapatılıyor...")
    scale.cleanup()
    camera.cleanup()

# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Production'da False
        log_level="info"
    )
