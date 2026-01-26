import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Camera, Loader2, ArrowLeft } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import { connectWeightStream, scanComplete } from '../services/api';

export default function Scanning() {
  const navigate = useNavigate();
  const { selectedProfile, currentWeight, setCurrentWeight, setLastResult } = useAppStore();
  
  const [status, setStatus] = useState('ready'); // ready, measuring, capturing, analyzing
  const [progress, setProgress] = useState(0);
  const [ws, setWs] = useState(null);

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

  // Otomatik tarama başlat
  useEffect(() => {
    startScanning();
  }, []);

  const startScanning = async () => {
    try {
      // 1. Ağırlık ölçümü
      setStatus('measuring');
      setProgress(20);
      
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // 2. Fotoğraf çekme ve analiz
      setStatus('capturing');
      setProgress(40);
      
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setStatus('analyzing');
      setProgress(60);
      
      // 3. Backend'den tam tarama yap
      const result = await scanComplete();
      
      setProgress(100);
      
      if (result.status === 'success') {
        // Sonucu kaydet
        setLastResult({
          status: 'success',
          food_name: result.food_name,
          confidence: result.confidence,
          percentage: result.percentage,
          weight: result.weight,
          nutrition: result.nutrition,
          predictions: result.predictions,
          profile: selectedProfile,
          timestamp: result.timestamp
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
          {status === 'ready' && 'Hazırlanıyor...'}
          {status === 'measuring' && 'Ağırlık Ölçülüyor...'}
          {status === 'capturing' && 'Fotoğraf Çekiliyor...'}
          {status === 'analyzing' && 'Analiz Ediliyor...'}
        </h1>

        <div className="w-12" /> {/* Spacer */}
      </div>

      {/* Scanning Animation */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="flex-1 glass rounded-3xl overflow-hidden relative flex items-center justify-center"
      >
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
            className="inline-block mb-8"
          >
            <Camera size={120} className="text-white/60" />
          </motion.div>
          
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
            className="inline-block mb-6"
          >
            <Loader2 size={60} className="text-white" />
          </motion.div>
          
          <p className="text-3xl text-white font-semibold mb-4">
            {status === 'ready' && 'Sistem hazırlanıyor...'}
            {status === 'measuring' && 'Ağırlık ölçülüyor...'}
            {status === 'capturing' && 'Fotoğraf çekiliyor...'}
            {status === 'analyzing' && 'AI analiz yapıyor...'}
          </p>
          
          <p className="text-xl text-white/70">
            Lütfen bekleyin
          </p>
        </div>
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
