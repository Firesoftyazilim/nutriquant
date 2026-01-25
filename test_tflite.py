"""
TFLite model test scripti
"""
import numpy as np
import json
from PIL import Image
import tensorflow as tf
import os


class TFLitePredictor:
    """TFLite model ile tahmin yapma"""
    
    def __init__(self, tflite_path, class_indices_path):
        """
        Args:
            tflite_path: TFLite model dosya yolu
            class_indices_path: Sınıf indeksleri JSON dosyası
        """
        # TFLite interpreter yükle
        self.interpreter = tf.lite.Interpreter(model_path=tflite_path)
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
    
    def preprocess_image(self, image_path):
        """Görüntüyü model için hazırlar"""
        # Görüntüyü yükle
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))
        
        # NumPy array'e çevir
        img_array = np.array(img, dtype=np.float32)
        
        # Normalizasyon
        img_array = img_array / 255.0
        
        # Batch dimension ekle
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def predict(self, image_path, top_k=5):
        """
        Görüntüden tahmin yapar
        
        Args:
            image_path: Görüntü dosya yolu
            top_k: En yüksek K tahmin
            
        Returns:
            Tahmin sonuçları
        """
        # Görüntüyü hazırla
        img_array = self.preprocess_image(image_path)
        
        # Tahmin yap
        self.interpreter.set_tensor(self.input_details[0]['index'], img_array)
        self.interpreter.invoke()
        predictions = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        
        # Top-K tahminleri al
        top_indices = np.argsort(predictions)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                'class': self.class_names[idx],
                'confidence': float(predictions[idx]),
                'percentage': float(predictions[idx] * 100)
            })
        
        return results


def test_all_models():
    """Tüm TFLite modellerini test eder"""
    
    print("\n" + "="*60)
    print("🧪 TFLITE MODEL TEST")
    print("="*60 + "\n")
    
    # Model dosyaları
    models = {
        'Standard (Tam Doğruluk)': 'models/model_standard.tflite',
        'Float16 (Önerilen)': 'models/model_float16.tflite',
        'Integer Quantized (En Küçük)': 'models/model_int8.tflite'
    }
    
    class_indices_path = 'models/class_indices.json'
    
    # Test görüntüsü iste
    print("📸 Test etmek için bir görüntü yolu girin:")
    print("   (Örnek: data/train/pizza/123456.jpg)")
    image_path = input("\nGörüntü yolu: ").strip()
    
    if not os.path.exists(image_path):
        print(f"\n❌ Dosya bulunamadı: {image_path}")
        
        # Otomatik örnek bul
        print("\n🔍 Otomatik örnek görüntü aranıyor...")
        for category in os.listdir('data/train'):
            cat_path = os.path.join('data/train', category)
            if os.path.isdir(cat_path):
                images = [f for f in os.listdir(cat_path) if f.endswith('.jpg')]
                if images:
                    image_path = os.path.join(cat_path, images[0])
                    print(f"✅ Örnek bulundu: {image_path}")
                    break
    
    if not os.path.exists(image_path):
        print("❌ Test görüntüsü bulunamadı!")
        return
    
    # Görüntüyü göster
    print(f"\n📷 Test edilen görüntü: {image_path}")
    actual_category = os.path.basename(os.path.dirname(image_path))
    print(f"🎯 Gerçek kategori: {actual_category}")
    
    print("\n" + "-"*60)
    
    # Her modeli test et
    for model_name, model_path in models.items():
        if not os.path.exists(model_path):
            print(f"\n⚠️  {model_name}: Dosya bulunamadı")
            continue
        
        print(f"\n🔬 {model_name}")
        print(f"   Dosya: {model_path}")
        
        # Dosya boyutu
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"   Boyut: {size_mb:.2f} MB")
        
        try:
            # Predictor oluştur
            predictor = TFLitePredictor(model_path, class_indices_path)
            
            # Tahmin yap
            import time
            start_time = time.time()
            results = predictor.predict(image_path, top_k=5)
            inference_time = (time.time() - start_time) * 1000  # ms
            
            print(f"   ⚡ Tahmin süresi: {inference_time:.2f} ms")
            print(f"\n   📊 Tahmin Sonuçları:")
            
            for i, result in enumerate(results, 1):
                emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
                correct = "✅" if result['class'] == actual_category else ""
                print(f"      {emoji} {i}. {result['class']}: {result['percentage']:.2f}% {correct}")
            
            # Doğruluk kontrolü
            if results[0]['class'] == actual_category:
                print(f"\n   ✅ DOĞRU TAHMİN!")
            else:
                print(f"\n   ❌ Yanlış tahmin (Beklenen: {actual_category})")
            
        except Exception as e:
            print(f"   ❌ Hata: {str(e)}")
        
        print("-"*60)
    
    print("\n" + "="*60)
    print("✅ TEST TAMAMLANDI!")
    print("="*60)


def compare_models_speed():
    """Model hızlarını karşılaştır"""
    
    print("\n" + "="*60)
    print("⚡ MODEL HIZ KARŞILAŞTIRMASI")
    print("="*60 + "\n")
    
    models = {
        'Standard': 'models/model_standard.tflite',
        'Float16': 'models/model_float16.tflite',
        'Int8': 'models/model_int8.tflite'
    }
    
    class_indices_path = 'models/class_indices.json'
    
    # Test görüntüsü bul
    test_image = None
    for category in os.listdir('data/train'):
        cat_path = os.path.join('data/train', category)
        if os.path.isdir(cat_path):
            images = [f for f in os.listdir(cat_path) if f.endswith('.jpg')]
            if images:
                test_image = os.path.join(cat_path, images[0])
                break
    
    if not test_image:
        print("❌ Test görüntüsü bulunamadı!")
        return
    
    print(f"📷 Test görüntüsü: {test_image}\n")
    
    results = []
    
    for model_name, model_path in models.items():
        if not os.path.exists(model_path):
            continue
        
        try:
            predictor = TFLitePredictor(model_path, class_indices_path)
            
            # 10 kez çalıştır, ortalama al
            import time
            times = []
            for _ in range(10):
                start = time.time()
                predictor.predict(test_image, top_k=1)
                times.append((time.time() - start) * 1000)
            
            avg_time = np.mean(times)
            size_mb = os.path.getsize(model_path) / (1024 * 1024)
            
            results.append({
                'name': model_name,
                'time': avg_time,
                'size': size_mb
            })
            
        except Exception as e:
            print(f"❌ {model_name}: {str(e)}")
    
    # Sonuçları göster
    print("\n📊 Karşılaştırma Sonuçları:\n")
    print(f"{'Model':<15} {'Boyut':<12} {'Hız':<15} {'Hız/Boyut'}")
    print("-"*60)
    
    for r in sorted(results, key=lambda x: x['time']):
        ratio = r['time'] / r['size']
        print(f"{r['name']:<15} {r['size']:>6.2f} MB   {r['time']:>6.2f} ms   {ratio:>6.2f}")
    
    print("\n💡 Öneriler:")
    fastest = min(results, key=lambda x: x['time'])
    smallest = min(results, key=lambda x: x['size'])
    
    print(f"   ⚡ En hızlı: {fastest['name']} ({fastest['time']:.2f} ms)")
    print(f"   💾 En küçük: {smallest['name']} ({smallest['size']:.2f} MB)")
    print(f"   ⭐ Önerilen: Float16 (hız ve boyut dengesi)")


def main():
    """Ana fonksiyon"""
    
    print("\n🎯 TFLite Test Seçenekleri:\n")
    print("1. Tek görüntü ile tüm modelleri test et")
    print("2. Model hızlarını karşılaştır")
    print("3. İnteraktif test (birden fazla görüntü)")
    
    choice = input("\nSeçiminiz (1-3): ").strip()
    
    if choice == '1':
        test_all_models()
    elif choice == '2':
        compare_models_speed()
    elif choice == '3':
        interactive_test()
    else:
        print("❌ Geçersiz seçim!")


def interactive_test():
    """İnteraktif test modu"""
    
    print("\n" + "="*60)
    print("🎮 İNTERAKTİF TEST MODU")
    print("="*60 + "\n")
    
    # Model seç
    print("Hangi modeli kullanmak istersiniz?")
    print("1. Standard (Tam doğruluk)")
    print("2. Float16 (Önerilen)")
    print("3. Int8 (En küçük)")
    
    model_choice = input("\nSeçim (1-3): ").strip()
    
    model_map = {
        '1': 'models/model_standard.tflite',
        '2': 'models/model_float16.tflite',
        '3': 'models/model_int8.tflite'
    }
    
    model_path = model_map.get(model_choice)
    if not model_path or not os.path.exists(model_path):
        print("❌ Geçersiz seçim veya model bulunamadı!")
        return
    
    # Predictor oluştur
    predictor = TFLitePredictor(model_path, 'models/class_indices.json')
    
    print("\n✅ Model hazır! Test etmeye başlayabilirsiniz.")
    print("   (Çıkmak için 'q' yazın)\n")
    
    while True:
        image_path = input("Görüntü yolu: ").strip()
        
        if image_path.lower() == 'q':
            print("\n👋 Çıkılıyor...")
            break
        
        if not os.path.exists(image_path):
            print(f"❌ Dosya bulunamadı: {image_path}\n")
            continue
        
        try:
            # Tahmin yap
            import time
            start = time.time()
            results = predictor.predict(image_path, top_k=5)
            inference_time = (time.time() - start) * 1000
            
            print(f"\n⚡ Tahmin süresi: {inference_time:.2f} ms")
            print(f"📊 Sonuçlar:")
            
            for i, result in enumerate(results, 1):
                emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
                print(f"   {emoji} {i}. {result['class']}: {result['percentage']:.2f}%")
            
            print()
            
        except Exception as e:
            print(f"❌ Hata: {str(e)}\n")


if __name__ == "__main__":
    main()
