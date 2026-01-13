# Besin Değerleri Hesaplama

import json
import os
from config import DATA_DIR

class NutritionCalculator:
    def __init__(self):
        self.food_db = {}
        self.load_database()
    
    def load_database(self):
        """Yemek veritabanını yükle"""
        db_path = os.path.join(DATA_DIR, "foods.json")
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                self.food_db = json.load(f)
            print(f"Veritabanı yüklendi: {len(self.food_db)} yemek")
        except Exception as e:
            print(f"Veritabanı yükleme hatası: {e}")
    
    def get_food_info(self, food_key):
        """Yemek bilgilerini getir"""
        return self.food_db.get(food_key)
    
    def calculate(self, food_key, weight_grams):
        """Besin değerlerini hesapla (100g bazlı)"""
        food = self.get_food_info(food_key)
        
        if not food:
            return None
        
        factor = weight_grams / 100.0
        
        result = {
            'name': food['name'],
            'weight': weight_grams,
            'calorie': round(food['calorie'] * factor, 1),
            'protein': round(food['protein'] * factor, 1),
            'carb': round(food['carb'] * factor, 1),
            'fat': round(food['fat'] * factor, 1)
        }
        
        return result
    
    def search_food(self, query):
        """Yemek ara"""
        results = []
        query_lower = query.lower()
        
        for key, food in self.food_db.items():
            if query_lower in food['name'].lower() or query_lower in key:
                results.append({
                    'key': key,
                    'name': food['name']
                })
        
        return results
    
    def get_all_foods(self):
        """Tüm yemekleri listele"""
        return [{'key': k, 'name': v['name']} for k, v in self.food_db.items()]

# Test fonksiyonu
if __name__ == "__main__":
    calc = NutritionCalculator()
    
    result = calc.calculate("bulgur_pilavi", 180)
    if result:
        print(f"{result['name']}: {result['weight']}g")
        print(f"Kalori: {result['calorie']} kcal")
        print(f"Protein: {result['protein']}g")
        print(f"Karbonhidrat: {result['carb']}g")
        print(f"Yağ: {result['fat']}g")
