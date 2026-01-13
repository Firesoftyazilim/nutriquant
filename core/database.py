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
            "food": food_name,
            "weight": weight,
            "nutrition": nutrition,
            "bmi": bmi_data
        }
        
        measurements["measurements"].append(measurement)
        
        if len(measurements["measurements"]) > 100:
            measurements["measurements"] = measurements["measurements"][-100:]
        
        return self.save_json("measurements.json", measurements)
    
    def get_user(self, user_id):
        """Kullanıcı bilgisi getir"""
        users = self.load_json("users.json", {"users": {}})
        return users["users"].get(str(user_id))
    
    def save_user(self, user_id, user_data):
        """Kullanıcı bilgisi kaydet"""
        users = self.load_json("users.json", {"users": {}})
        users["users"][str(user_id)] = user_data
        return self.save_json("users.json", users)

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
