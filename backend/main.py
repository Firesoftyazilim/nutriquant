"""
Nutriquant Backend API
FastAPI + WebSocket - Raspberry Pi Sensör Kontrolü
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import asyncio
import io
import sys
import os
import json
import numpy as np
import subprocess
from typing import Optional, List
from datetime import datetime
from PIL import Image

# Backend dizinini path'e ekle (artık her şey backend içinde)
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from hardware.scale import Scale
from hardware.camera import Camera
from hardware.battery import Battery
from hardware.speaker import Speaker
from ai.food_recognition import FoodRecognizer
from core.nutrition import NutritionCalculator
from core.bmi import BMICalculator
from core.database import Database

try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    print("⚠️ tflite_runtime bulunamadı, tensorflow kullanılıyor...")
    import tensorflow.lite as tflite

# ==================== TFLITE PREDICTOR CLASS ====================

class TFLitePredictor:
    """TFLite model ile tahmin yapma"""
    
    def __init__(self, tflite_path, class_indices_path):
        """
        Args:
            tflite_path: TFLite model dosya yolu
            class_indices_path: Sınıf indeksleri JSON dosyası
        """
        # TFLite interpreter yükle
        self.interpreter = tflite.Interpreter(model_path=tflite_path)
        self.interpreter.allocate_tensors()
        
        # Giriş/çıkış detayları
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        # Sınıf isimlerini yükle
        with open(class_indices_path, 'r', encoding='utf-8') as f:
            class_indices = json.load(f)
        self.class_names = {v: k for k, v in class_indices.items()}
        
        print(f"✅ TFLite model yüklendi: {tflite_path}")
        print(f"   Giriş boyutu: {self.input_details[0]['shape']}")
        print(f"   Çıkış boyutu: {self.output_details[0]['shape']}")
        print(f"   Kategori sayısı: {len(self.class_names)}")
    
    def preprocess_image(self, image_data):
        """Görüntüyü model için hazırlar"""
        # PIL Image'e çevir
        if isinstance(image_data, bytes):
            img = Image.open(io.BytesIO(image_data)).convert('RGB')
        elif isinstance(image_data, str):
            img = Image.open(image_data).convert('RGB')
        else:
            img = image_data.convert('RGB')
        
        img = img.resize((224, 224))
        
        # NumPy array'e çevir
        img_array = np.array(img, dtype=np.float32)
        
        # Normalizasyon
        img_array = img_array / 255.0
        
        # Batch dimension ekle
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def predict(self, image_data, top_k=5):
        """
        Görüntüden tahmin yapar
        
        Args:
            image_data: Görüntü dosya yolu veya bytes
            top_k: En yüksek K tahmin
            
        Returns:
            Tahmin sonuçları
        """
        try:
            # Görüntüyü hazırla
            img_array = self.preprocess_image(image_data)
            print(f"🔍 Preprocessed image shape: {img_array.shape}")
            
            # Tahmin yap
            self.interpreter.set_tensor(self.input_details[0]['index'], img_array)
            self.interpreter.invoke()
            predictions = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
            print(f"📊 Predictions shape: {predictions.shape}, min: {predictions.min():.4f}, max: {predictions.max():.4f}")
            
            # Top-K tahminleri al
            top_indices = np.argsort(predictions)[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                if idx not in self.class_names:
                    print(f"⚠️ Index {idx} not found in class_names")
                    continue
                results.append({
                    'class': self.class_names[idx],
                    'confidence': float(predictions[idx]),
                    'percentage': float(predictions[idx] * 100)
                })
            
            return results
        except Exception as e:
            print(f"❌ TFLitePredictor.predict error: {type(e).__name__}: {str(e)}")
            raise

# FastAPI App
app = FastAPI(title="Nutriquant API", version="2.0.0")

# CORS - Tüm origin'lerden erişim için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm origin'lere izin ver
    allow_credentials=False,  # Wildcard origin kullanırken False olmalı
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

# TFLite model predictor
try:
    # Backend klasörü içindeki models klasörü
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(backend_dir, "models", "model_float16.tflite")
    class_indices_path = os.path.join(backend_dir, "models", "class_indices.json")
    
    print(f"🔍 Model yolu: {model_path}")
    print(f"🔍 Class indices yolu: {class_indices_path}")
    
    tflite_predictor = TFLitePredictor(model_path, class_indices_path)
except Exception as e:
    print(f"⚠️ TFLite model yüklenemedi: {e}")
    tflite_predictor = None

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
    """
    Ağırlık sensöründen anlık veri oku
    
    Returns:
        weight: Ağırlık değeri (gram)
        unit: Birim (g)
        timestamp: Okuma zamanı
        status: Sensör durumu
    """
    try:
        weight = scale.read_weight()
        
        # Ağırlık durumu kontrolü
        status = "empty" if weight < 5 else "measuring"
        
        return {
            "weight": weight,
            "unit": "g",
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "scale_mode": scale.mode
        }
    except Exception as e:
        print(f"❌ Ağırlık okuma hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Ağırlık okuma hatası: {str(e)}")

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

@app.post("/api/model-test")
async def test_model(file: UploadFile = File(...)):
    """
    Model test endpoint - model_float16.tflite ile görüntü analizi
    
    Args:
        file: Yüklenen görüntü dosyası (multipart/form-data)
    
    Returns:
        Top 5 tahmin ve güven skorları (class_indices.json kullanarak)
    """
    try:
        # TFLite model kontrolü
        if tflite_predictor is None:
            raise HTTPException(status_code=503, detail="TFLite model yüklenmedi")
        
        # Dosya içeriğini oku
        contents = await file.read()
        print(f"📸 Görüntü yüklendi: {len(contents)} bytes, dosya: {file.filename}")
        
        # TFLite predictor ile tahmin yap (top 5)
        predictions = tflite_predictor.predict(contents, top_k=5)
        
        if not predictions:
            return {
                "status": "error",
                "message": "Model tahmin yapamadı",
                "predictions": []
            }
        
        # Sonuçları formatla
        results = []
        for pred in predictions:
            results.append({
                "food_name": pred['class'],
                "confidence": pred['confidence'],
                "percentage": pred['percentage']
            })
        
        return {
            "status": "success",
            "model": "model_float16.tflite",
            "predictions": results,
            "top_match": results[0] if results else None
        }
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"{type(e).__name__}: {str(e)}"
        print(f"❌ Model test hatası: {error_detail}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Model test hatası: {error_detail}")

@app.post("/api/capture-and-analyze")
async def capture_and_analyze():
    """
    Raspberry Pi kamerasıyla fotoğraf çek ve model ile analiz et
    
    Returns:
        Model tahminleri ve güven skorları
    """
    try:
        # TFLite model kontrolü
        if tflite_predictor is None:
            raise HTTPException(status_code=503, detail="TFLite model yüklenmedi")
        
        # Fotoğraf dosya yolu (backend klasörü içinde)
        photo_path = os.path.join(backend_dir, "foto.jpg")
        
        # rpicam-still komutu ile fotoğraf çek
        print(f"📸 Fotoğraf çekiliyor: {photo_path}")
        
        cmd = [
            "rpicam-still",
            "--mode", "3280:2464",
            "--roi", "0,0,1,1",
            "-o", photo_path
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
                check=True
            )
            print(f"✅ Fotoğraf çekildi: {photo_path}")
            print(f"   Çıktı: {result.stdout}")
        except subprocess.TimeoutExpired:
            raise HTTPException(status_code=500, detail="Kamera zaman aşımı (10 saniye)")
        except subprocess.CalledProcessError as e:
            print(f"❌ rpicam-still hatası: {e.stderr}")
            raise HTTPException(status_code=500, detail=f"Kamera hatası: {e.stderr}")
        except FileNotFoundError:
            print("⚠️ rpicam-still bulunamadı, mock mode")
            # Mock mode - test için boş bir görsel oluştur
            img = Image.new('RGB', (224, 224), color='gray')
            img.save(photo_path)
        
        # Fotoğrafın var olduğunu kontrol et
        if not os.path.exists(photo_path):
            raise HTTPException(status_code=500, detail="Fotoğraf oluşturulamadı")
        
        # Model ile tahmin yap
        print(f"🔍 Model analizi yapılıyor...")
        predictions = tflite_predictor.predict(photo_path, top_k=5)
        
        if not predictions:
            return {
                "status": "error",
                "message": "Model tahmin yapamadı",
                "predictions": []
            }
        
        # Sonuçları formatla
        results = []
        for pred in predictions:
            results.append({
                "food_name": pred['class'],
                "confidence": pred['confidence'],
                "percentage": pred['percentage']
            })
        
        print(f"✅ Analiz tamamlandı. En yüksek tahmin: {results[0]['food_name']} (%{results[0]['percentage']:.1f})")
        
        return {
            "status": "success",
            "model": "model_float16.tflite",
            "photo_path": photo_path,
            "predictions": results,
            "top_match": results[0] if results else None
        }
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"{type(e).__name__}: {str(e)}"
        print(f"❌ Capture and analyze hatası: {error_detail}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Capture and analyze hatası: {error_detail}")

@app.post("/api/scan-complete")
async def scan_complete():
    """
    Tam tarama işlemi: Ağırlık ölç + Fotoğraf çek + Model tahmini + Besin değerleri hesapla
    
    Returns:
        Ağırlık, tahmin edilen yemek, ve hesaplanmış besin değerleri
    """
    try:
        # 1. Ağırlık ölç
        weight = scale.read_weight()
        print(f"📊 Ölçülen ağırlık: {weight}g")
        
        if weight < 5:
            raise HTTPException(status_code=400, detail="Tartıda yeterli ağırlık yok (minimum 5g)")
        
        # 2. Fotoğraf çek ve model tahmini yap
        print(f"📸 Fotoğraf çekiliyor ve analiz ediliyor...")
        
        # TFLite model kontrolü
        if tflite_predictor is None:
            raise HTTPException(status_code=503, detail="TFLite model yüklenmedi")
        
        # Fotoğraf dosya yolu (backend klasörü içinde)
        photo_path = os.path.join(backend_dir, "foto.jpg")
        
        # rpicam-still komutu ile fotoğraf çek
        cmd = [
            "rpicam-still",
            "--mode", "3280:2464",
            "--roi", "0,0,1,1",
            "-o", photo_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, check=True)
            print(f"✅ Fotoğraf çekildi: {photo_path}")
        except subprocess.TimeoutExpired:
            raise HTTPException(status_code=500, detail="Kamera zaman aşımı")
        except subprocess.CalledProcessError as e:
            print(f"❌ rpicam-still hatası: {e.stderr}")
            raise HTTPException(status_code=500, detail=f"Kamera hatası: {e.stderr}")
        except FileNotFoundError:
            print("⚠️ rpicam-still bulunamadı, mock mode")
            img = Image.new('RGB', (224, 224), color='gray')
            img.save(photo_path)
        
        # Fotoğrafın var olduğunu kontrol et
        if not os.path.exists(photo_path):
            raise HTTPException(status_code=500, detail="Fotoğraf oluşturulamadı")
        
        # 3. Model ile tahmin yap
        predictions = tflite_predictor.predict(photo_path, top_k=5)
        
        if not predictions:
            raise HTTPException(status_code=500, detail="Model tahmin yapamadı")
        
        top_prediction = predictions[0]
        food_name = top_prediction['class']
        confidence = top_prediction['confidence']
        
        print(f"🍽️ Tahmin edilen yemek: {food_name} (%{top_prediction['percentage']:.1f})")
        
        # 4. Besin değerlerini yükle (datas.json)
        nutrition_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "datas.json")
        
        with open(nutrition_db_path, 'r', encoding='utf-8') as f:
            nutrition_db = json.load(f)
        
        # 5. Yemek için besin değerlerini bul
        if food_name not in nutrition_db:
            print(f"⚠️ {food_name} için besin değeri bulunamadı, varsayılan değerler kullanılıyor")
            base_nutrition = {
                "name": food_name,
                "calorie": 150,
                "protein": 5.0,
                "carbohydrate": 20.0,
                "sugar": 5.0
            }
        else:
            base_nutrition = nutrition_db[food_name]
        
        # 6. Ağırlığa göre besin değerlerini hesapla (100g bazında)
        weight_ratio = weight / 100.0
        
        calculated_nutrition = {
            "name": food_name,
            "weight": weight,
            "calorie": round(base_nutrition["calorie"] * weight_ratio, 1),
            "protein": round(base_nutrition["protein"] * weight_ratio, 1),
            "carbohydrate": round(base_nutrition["carbohydrate"] * weight_ratio, 1),
            "sugar": round(base_nutrition.get("sugar", 0) * weight_ratio, 1),
            "base_values_per_100g": base_nutrition
        }
        
        print(f"📊 Hesaplanan besin değerleri:")
        print(f"   Kalori: {calculated_nutrition['calorie']} kcal")
        print(f"   Protein: {calculated_nutrition['protein']}g")
        print(f"   Karbonhidrat: {calculated_nutrition['carbohydrate']}g")
        
        # 7. Tüm tahminleri formatla
        all_predictions = []
        for pred in predictions:
            all_predictions.append({
                "food_name": pred['class'],
                "confidence": pred['confidence'],
                "percentage": pred['percentage']
            })
        
        return {
            "status": "success",
            "weight": weight,
            "food_name": food_name,
            "confidence": confidence,
            "percentage": top_prediction['percentage'],
            "nutrition": calculated_nutrition,
            "predictions": all_predictions,
            "photo_path": photo_path,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"{type(e).__name__}: {str(e)}"
        print(f"❌ Scan complete hatası: {error_detail}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Scan complete hatası: {error_detail}")

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

@app.get("/api/profiles/{profile_id}/history")
async def get_profile_history(profile_id: int):
    """Profil geçmiş taramalarını getir"""
    try:
        # Profil bilgisini al
        profiles = db.get_all_profiles()
        profile = next((p for p in profiles if p['id'] == profile_id), None)
        
        if not profile:
            raise HTTPException(status_code=404, detail="Profil bulunamadı")
        
        # Ölçümleri al
        measurements = db.get_measurements_by_user(profile_id)
        
        # Tarihe göre sırala (en yeni en üstte)
        measurements.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return {
            "profile_name": profile['name'],
            "history": measurements
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Geçmiş yükleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
        app,  # Direct app object instead of "main:app"
        host="0.0.0.0",
        port=8000,
        reload=False,  # Production'da False
        log_level="info"
    )
