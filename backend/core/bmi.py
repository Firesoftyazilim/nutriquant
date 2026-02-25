# VKİ (Vücut Kitle İndeksi) Hesaplama

class BMICalculator:
    def __init__(self):
        pass
    
    def calculate(self, weight_kg, height_cm):
        """VKİ hesapla"""
        height_m = height_cm / 100.0
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 2)
    
    def get_category(self, bmi, age):
        """Yaşa göre VKİ kategorisi"""
        if age < 18:
            if bmi < 14:
                return "zayif"
            elif bmi < 18:
                return "normal"
            else:
                return "yuksek"
        
        elif age < 65:
            if bmi < 18.5:
                return "zayif"
            elif bmi < 25:
                return "normal"
            elif bmi < 30:
                return "fazla_kilolu"
            else:
                return "obez"
        
        else:
            if bmi < 22:
                return "zayif"
            elif bmi < 27:
                return "normal"
            else:
                return "yuksek"
    
    def get_comment(self, bmi, age):
        """VKİ yorumu"""
        category = self.get_category(bmi, age)
        
        comments = {
            "zayif": "Zayıf",
            "normal": "Normal",
            "fazla_kilolu": "Fazla Kilolu",
            "yuksek": "Yüksek",
            "obez": "Obez"
        }
        
        return comments.get(category, "Bilinmiyor")
    
    def get_meal_recommendation(self, bmi, age, meal_calories, meal_name="bu yemek"):
        """BMI'ya göre öğün önerisi"""
        category = self.get_category(bmi, age)
        
        # Günlük kalori ihtiyaçları (ortalama)
        daily_calories = {
            "zayif": 2200,      # Kilo almaya odaklan
            "normal": 2000,     # Dengeli beslen
            "fazla_kilolu": 1800, # Hafif kısıtla
            "obez": 1600,       # Daha fazla kısıtla
            "yuksek": 1700      # Yaşlılar için
        }
        
        # Tek öğün için kalori (günlük kalorinın %30-35'i)
        target_meal_calories = daily_calories.get(category, 2000) * 0.33
        
        recommendations = {
            "zayif": {
                "message": f"Kilo almanız gerekiyor. {meal_name} ({meal_calories} kalori) iyi bir seçim!",
                "advice": "Daha fazla porsiyon tüketebilir, sağlıklı yağlar ve protein ekleyebilirsiniz.",
                "portion_advice": "normal_plus"
            },
            "normal": {
                "message": f"Kilonuz ideal aralıkta. {meal_name} ({meal_calories} kalori) dengeli bir öğün.",
                "advice": "Bu porsiyonu koruyun ve düzenli egzersiz yapmaya devam edin.",
                "portion_advice": "normal"
            },
            "fazla_kilolu": {
                "message": f"Hafif kilo vermeniz önerilir. {meal_name} ({meal_calories} kalori) için dikkatli olun.",
                "advice": "Porsiyonu biraz azaltabilir veya daha az yağlı alternatifler seçebilirsiniz.",
                "portion_advice": "reduce"
            },
            "obez": {
                "message": f"Kilo vermeniz gerekiyor. {meal_name} ({meal_calories} kalori) yüksek olabilir.",
                "advice": "Porsiyonu yarıya indirin veya daha düşük kalorili alternatifler tercih edin.",
                "portion_advice": "reduce_significantly"
            },
            "yuksek": {
                "message": f"Yaşınız için kilonuz yüksek. {meal_name} ({meal_calories} kalori) dikkatli tüketin.",
                "advice": "Porsiyonu azaltın ve daha çok sebze ekleyin.",
                "portion_advice": "reduce"
            }
        }
        
        recommendation = recommendations.get(category, recommendations["normal"])
        
        # Kalori karşılaştırması
        if meal_calories > target_meal_calories * 1.3:
            calorie_status = "yuksek"
        elif meal_calories < target_meal_calories * 0.7:
            calorie_status = "dusuk"
        else:
            calorie_status = "uygun"
        
        return {
            "bmi_category": category,
            "target_meal_calories": int(target_meal_calories),
            "meal_calories": meal_calories,
            "calorie_status": calorie_status,
            "message": recommendation["message"],
            "advice": recommendation["advice"],
            "portion_advice": recommendation["portion_advice"]
        }
    
    def should_warn(self, bmi, age):
        """Uyarı verilmeli mi?"""
        category = self.get_category(bmi, age)
        return category in ["yuksek", "obez", "fazla_kilolu"]

# Test fonksiyonu
if __name__ == "__main__":
    calc = BMICalculator()
    
    bmi = calc.calculate(70, 175)
    comment = calc.get_comment(bmi, 30)
    warn = calc.should_warn(bmi, 30)
    
    print(f"VKİ: {bmi}")
    print(f"Durum: {comment}")
    print(f"Uyarı: {'Evet' if warn else 'Hayır'}")
