# VKİ (Vücut Kitle İndeksi) Hesaplama

from config import AGE_BMI_RULES

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
