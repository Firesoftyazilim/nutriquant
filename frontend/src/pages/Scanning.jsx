import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Camera, Loader2, ArrowLeft } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import { captureImage, connectWeightStream, testModel } from '../services/api';

export default function Scanning() {
  const navigate = useNavigate();
  const { selectedProfile, currentWeight, setCurrentWeight, setLastResult } = useAppStore();
  
  const [status, setStatus] = useState('preview'); // preview, capturing, analyzing
  const [cameraImage, setCameraImage] = useState(null);
  const [progress, setProgress] = useState(0);
  const [ws, setWs] = useState(null);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  // WebSocket ile gerçek zamanlı ağırlık
  useEffect(() => {
    const websocket = connectWeightStream((weight) => {
      setCurrentWeight(weight);
    });
    setWs(websocket);

    return () => {
      if (websocket) websocket.close();
    };
  }, [setCurrentWeight]);

  // Kamera önizlemesi başlat
  useEffect(() => {
    startCameraPreview();
    return () => {
      stopCameraPreview();
    };
  }, []);

  const startCameraPreview = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' } 
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
      }
    } catch (error) {
      console.error('Kamera erişim hatası:', error);
      alert('Kamera erişimi reddedildi veya kullanılamıyor');
    }
  };

  const stopCameraPreview = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
  };

  const captureFromCamera = async () => {
    if (!videoRef.current) return null;

    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoRef.current, 0, 0);

    return new Promise((resolve) => {
      canvas.toBlob((blob) => {
        resolve(blob);
      }, 'image/jpeg', 0.95);
    });
  };

  const startScanning = async () => {
    try {
      // 1. Fotoğraf çek
      setStatus('capturing');
      setProgress(20);
      
      const imageBlob = await captureFromCamera();
      if (!imageBlob) {
        throw new Error('Fotoğraf çekilemedi');
      }

      // Önizleme için URL oluştur
      const imageUrl = URL.createObjectURL(imageBlob);
      setCameraImage(imageUrl);
      
      // Kamera önizlemesini durdur
      stopCameraPreview();
      
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // 2. Model ile analiz yap
      setStatus('analyzing');
      setProgress(60);
      
      const modelResult = await testModel(imageBlob);
      
      setProgress(100);
      
      if (modelResult.status === 'success' && modelResult.predictions.length > 0) {
        // En yüksek tahmin
        const topPrediction = modelResult.top_match;
        
        // Sonucu kaydet
        setLastResult({
          status: 'success',
          food_name: topPrediction.food_name,
          confidence: topPrediction.confidence,
          percentage: topPrediction.percentage,
          weight: currentWeight,
          predictions: modelResult.predictions,
          image: imageUrl,
          profile: selectedProfile
        });
        
        await new Promise(resolve => setTimeout(resolve, 500));
        navigate('/results');
      } else {
        // Tanınamadı
        alert('Yemek tanınamadı. Lütfen tekrar deneyin.');
        navigate('/');
      }
    } catch (error) {
      console.error('Tarama hatası:', error);
      alert('Bir hata oluştu: ' + error.message);
      navigate('/');
    }
  };

  return (
    <div className="h-screen w-screen bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-500 p-8 flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => navigate('/')}
          className="glass rounded-full p-3 text-white"
        >
          <ArrowLeft size={28} />
        </motion.button>

        <h1 className="text-3xl font-bold text-white">
          {status === 'preview' && 'Kamera Önizlemesi'}
          {status === 'capturing' && 'Fotoğraf Çekiliyor...'}
          {status === 'analyzing' && 'Analiz Ediliyor...'}
        </h1>

        <div className="w-12" /> {/* Spacer */}
      </div>

      {/* Camera Preview */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="flex-1 glass rounded-3xl overflow-hidden relative"
      >
        {cameraImage ? (
          <img 
            src={cameraImage} 
            alt="Captured" 
            className="w-full h-full object-cover"
          />
        ) : (
          <video
            ref={videoRef}
            autoPlay
            playsInline
            className="w-full h-full object-cover"
          />
        )}

        {/* Scanning overlay */}
        {status !== 'preview' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="absolute inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center"
          >
            <div className="text-center">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                className="inline-block mb-4"
              >
                <Loader2 size={60} className="text-white" />
              </motion.div>
              <p className="text-2xl text-white font-semibold">
                {status === 'capturing' && 'Görüntü yakalanıyor...'}
                {status === 'analyzing' && 'AI analiz yapıyor...'}
              </p>
            </div>
          </motion.div>
        )}

        {/* Capture Button - Only show in preview mode */}
        {status === 'preview' && (
          <motion.button
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={startScanning}
            className="absolute bottom-8 left-1/2 transform -translate-x-1/2 bg-white text-purple-600 rounded-full p-6 shadow-2xl"
          >
            <Camera size={40} />
          </motion.button>
        )}
      </motion.div>

      {/* Progress Bar */}
      {progress > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-6 glass rounded-full h-4 overflow-hidden"
        >
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.5 }}
            className="h-full bg-gradient-to-r from-green-400 to-blue-500"
          />
        </motion.div>
      )}

      {/* Info */}
      <div className="mt-4 flex justify-between text-white/80 text-lg">
        <span>Ağırlık: {currentWeight.toFixed(0)}g</span>
        <span>Profil: {selectedProfile?.name}</span>
      </div>
    </div>
  );
}
