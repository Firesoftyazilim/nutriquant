import numpy as np
import json
from PIL import Image
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    try:
        import tensorflow.lite as tflite
    except ImportError:
        tflite = None
class RaspberryPiPredictor:
    def __init__(self):
        # Float16 model (önerilen)
        model_path = 'models/model_float16.tflite'
        
        # TFLite Runtime kullan (daha hafif)
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        # Sınıf isimleri
        with open('models/class_indices.json', 'r') as f:
            class_indices = json.load(f)
        self.class_names = {v: k for k, v in class_indices.items()}
    
    def predict(self, image_path):
        # Görüntü hazırlama
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Tahmin
        self.interpreter.set_tensor(self.input_details[0]['index'], img_array)
        self.interpreter.invoke()
        predictions = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        
        # En iyi tahmin
        top_idx = np.argmax(predictions)
        return {
            'food': self.class_names[top_idx],
            'confidence': float(predictions[top_idx])
        }

# Kullanım
predictor = RaspberryPiPredictor()
result = predictor.predict('Desktop/foto.jpg')
print(f"Yemek: {result['food']}, Güven: {result['confidence']:.2%}")