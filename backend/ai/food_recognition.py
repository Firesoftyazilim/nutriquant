# AI Yemek Tanıma - TensorFlow Lite

import numpy as np
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    try:
        import tensorflow.lite as tflite
    except ImportError:
        tflite = None
        print("[Mock] TensorFlow Lite bulunamadı - simülasyon modu")
from PIL import Image
import random
from config import MODEL_PATH, LABELS_PATH, CONFIDENCE_THRESHOLD, INPUT_SIZE

class FoodRecognizer:
    def __init__(self):
        self.interpreter = None
        self.labels = []
        self.input_details = None
        self.output_details = None
        self.load_model()
    
    def load_model(self):
        """TFLite modelini yükle"""
        try:
            if tflite is None:
                raise ImportError("TFLite yok")
            
            self.interpreter = tflite.Interpreter(model_path=MODEL_PATH)
            self.interpreter.allocate_tensors()
            
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            with open(LABELS_PATH, 'r', encoding='utf-8') as f:
                self.labels = [line.strip() for line in f.readlines()]
            
            print(f"Model yüklendi: {len(self.labels)} sınıf")
        except Exception as e:
            print(f"[Mock] Model simülasyon modunda: {e}")
            try:
                with open(LABELS_PATH, 'r', encoding='utf-8') as f:
                    self.labels = [line.strip() for line in f.readlines()]
            except:
                self.labels = ['bulgur_pilavi', 'tavuk_izgara', 'omlet']
    
    def preprocess_image(self, image):
        """Görüntüyü model için hazırla"""
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        image = image.resize(INPUT_SIZE)
        image = image.convert('RGB')
        
        input_data = np.array(image, dtype=np.float32)
        input_data = np.expand_dims(input_data, axis=0)
        input_data = input_data / 255.0
        
        return input_data
    
    def recognize(self, image):
        """Yemek tanı"""
        if self.interpreter is None:
            print("[Mock] Rastgele yemek seçiliyor...")
            if self.labels:
                food_name = random.choice(self.labels)
                confidence = random.uniform(0.75, 0.95)
                return food_name, confidence
            return None, 0.0
        
        try:
            input_data = self.preprocess_image(image)
            
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            predictions = output_data[0]
            
            top_idx = np.argmax(predictions)
            confidence = float(predictions[top_idx])
            
            if confidence >= CONFIDENCE_THRESHOLD:
                food_name = self.labels[top_idx]
                return food_name, confidence
            else:
                return None, confidence
        
        except Exception as e:
            print(f"Tanıma hatası: {e}")
            return None, 0.0
    
    def get_top_predictions(self, image, top_k=3):
        """En yüksek olasılıklı tahminleri getir"""
        if self.interpreter is None:
            return []
        
        try:
            input_data = self.preprocess_image(image)
            
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            predictions = output_data[0]
            
            top_indices = np.argsort(predictions)[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                results.append({
                    'name': self.labels[idx],
                    'confidence': float(predictions[idx])
                })
            
            return results
        
        except Exception as e:
            print(f"Tahmin hatası: {e}")
            return []

# Test fonksiyonu
if __name__ == "__main__":
    recognizer = FoodRecognizer()
    
    test_image = Image.new('RGB', (224, 224), color='red')
    food, confidence = recognizer.recognize(test_image)
    
    if food:
        print(f"Tanınan yemek: {food} (%{confidence*100:.1f})")
    else:
        print("Yemek tanınamadı")
