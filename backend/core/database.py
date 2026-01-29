# Veritabanı Yönetimi

import json
import os
from datetime import datetime
from config import DATA_DIR

class Database:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """Data klasörünü oluştur"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_json(self, filename, default=None):
        """JSON dosyası yükle"""
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            if default is not None:
                self.save_json(filename, default)
                return default
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"JSON yükleme hatası ({filename}): {e}")
            return default
    
    def save_json(self, filename, data):
        """JSON dosyası kaydet"""
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"JSON kaydetme hatası ({filename}): {e}")
            return False
    
    def add_measurement(self, user_id, food_name, weight, nutrition, bmi_data):
        """Ölçüm kaydet"""
        measurements = self.load_json("measurements.json", {"measurements": []})
        
        measurement = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "food_name": food_name,
            "food": food_name,  # Backward compatibility
            "weight": weight,
            "calories": nutrition.get("calories", 0),
            "protein": nutrition.get("protein", 0),
            "carbs": nutrition.get("carbs", 0),
            "fat": nutrition.get("fat", 0),
            "confidence": nutrition.get("confidence", 0),
            "nutrition": nutrition,
            "bmi": bmi_data
        }
        
        measurements["measurements"].append(measurement)
        
        if len(measurements["measurements"]) > 100:
            measurements["measurements"] = measurements["measurements"][-100:]
        
        return self.save_json("measurements.json", measurements)
    
    def get_measurements_by_user(self, user_id):
        """Kullanıcıya ait tüm ölçümleri getir"""
        measurements = self.load_json("measurements.json", {"measurements": []})
        user_measurements = [
            m for m in measurements["measurements"] 
            if m.get("user_id") == user_id
        ]
        return user_measurements
    
    def get_user(self, user_id):
        """Kullanıcı bilgisi getir"""
        users = self.load_json("users.json", {"users": {}})
        return users["users"].get(str(user_id))
    
    def save_user(self, user_id, user_data):
        """Kullanıcı bilgisi kaydet"""
        users = self.load_json("users.json", {"users": {}})
        users["users"][str(user_id)] = user_data
        return self.save_json("users.json", users)
    
    def get_all_profiles(self):
        """Tüm profilleri getir"""
        profiles = self.load_json("profiles.json", {"profiles": []})
        return profiles["profiles"]
    
    def add_profile(self, name, gender, height, weight):
        """Yeni profil ekle"""
        profiles = self.load_json("profiles.json", {"profiles": []})
        
        # Yeni ID oluştur
        new_id = max([p.get("id", 0) for p in profiles["profiles"]], default=0) + 1
        
        profile = {
            "id": new_id,
            "name": name,
            "gender": gender,
            "height": height,
            "weight": weight,
            "created_at": datetime.now().isoformat()
        }
        
        profiles["profiles"].append(profile)
        self.save_json("profiles.json", profiles)
        return profile
    
    def update_profile(self, profile_id, name, gender, height, weight):
        """Profil güncelle"""
        profiles = self.load_json("profiles.json", {"profiles": []})
        
        for profile in profiles["profiles"]:
            if profile["id"] == profile_id:
                profile["name"] = name
                profile["gender"] = gender
                profile["height"] = height
                profile["weight"] = weight
                profile["updated_at"] = datetime.now().isoformat()
                break
        
        return self.save_json("profiles.json", profiles)
    
    def delete_profile(self, profile_id):
        """Profil sil"""
        profiles = self.load_json("profiles.json", {"profiles": []})
        profiles["profiles"] = [p for p in profiles["profiles"] if p["id"] != profile_id]
        return self.save_json("profiles.json", profiles)
    
    def get_settings(self):
        """Uygulama ayarlarını getir"""
        default_settings = {
            "wallpaper": None,  # Seçili arka plan (None = varsayılan)
            "sound_enabled": True,
            "brightness": 100
        }
        return self.load_json("settings.json", default_settings)
    
    def save_setting(self, key, value):
        """Tek bir ayarı kaydet"""
        settings = self.get_settings()
        settings[key] = value
        return self.save_json("settings.json", settings)
    
    def get_wallpaper(self):
        """Kayıtlı arka planı getir"""
        settings = self.get_settings()
        return settings.get("wallpaper")
    
    def save_wallpaper(self, wallpaper_name):
        """Arka plan seçimini kaydet"""
        return self.save_setting("wallpaper", wallpaper_name)
    
    def get_all_plates(self):
        """Tüm tabakları getir"""
        plates = self.load_json("plates.json", {"plates": []})
        return plates["plates"]
    
    def add_plate(self, name, weight):
        """Yeni tabak ekle"""
        plates = self.load_json("plates.json", {"plates": []})
        
        # Yeni ID oluştur
        new_id = max([p.get("id", 0) for p in plates["plates"]], default=0) + 1
        
        plate = {
            "id": new_id,
            "name": name,
            "weight": weight,
            "created_at": datetime.now().isoformat()
        }
        
        plates["plates"].append(plate)
        self.save_json("plates.json", plates)
        return plate
    
    def delete_plate(self, plate_id):
        """Tabak sil"""
        plates = self.load_json("plates.json", {"plates": []})
        plates["plates"] = [p for p in plates["plates"] if p["id"] != plate_id]
        return self.save_json("plates.json", plates)

# Test fonksiyonu
if __name__ == "__main__":
    db = Database()
    
    db.save_user(1, {
        "name": "Test Kullanıcı",
        "age": 30,
        "weight": 70,
        "height": 175
    })
    
    user = db.get_user(1)
    print(f"Kullanıcı: {user}")
