import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Camera, Loader2, ArrowLeft } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import { analyzeFood, captureImage } from '../services/api';

export default function Scanning() {
  const navigate = useNavigate();
  const { selectedProfile, currentWeight, setLastResult } = useAppStore();
  
  const [status, setStatus] = useState('ready'); // ready, capturing, analyzing
  const [cameraImage, setCameraImage] = useState(null);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // Otomatik başlat
    startScanning();
  }, []);

  const startScanning = async () => {
    try {
      // 1. Fotoğraf çek
      setStatus('capturing');
      setProgress(30);
      
      const imageUrl = await captureImage();
      setCameraImage(imageUrl);
      
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // 2. Analiz yap
      setStatus('analyzing');
      setProgress(60);
      
      const result = await analyzeFood(currentWeight, selectedProfile?.id);
      
      setProgress(100);
      
      if (result.status === 'success') {
        setLastResult(result);
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
          {status === 'capturing' && 'Fotoğraf Çekiliyor...'}
          {status === 'analyzing' && 'Analiz Ediliyor...'}
          {status === 'ready' && 'Hazırlanıyor...'}
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
          <div className="w-full h-full flex items-center justify-center">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
            >
              <Camera size={80} className="text-white/40" />
            </motion.div>
          </div>
        )}

        {/* Scanning overlay */}
        {status !== 'ready' && (
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
      </motion.div>

      {/* Progress Bar */}
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

      {/* Info */}
      <div className="mt-4 flex justify-between text-white/80 text-lg">
        <span>Ağırlık: {currentWeight.toFixed(0)}g</span>
        <span>Profil: {selectedProfile?.name}</span>
      </div>
    </div>
  );
}
