import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Camera, Loader2, ArrowLeft, Scale } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import { connectWeightStream, scanComplete, getWeight } from '../services/api';
import WallpaperBackground from '../components/WallpaperBackground';
import TareModal from '../components/TareModal';

export default function Scanning() {
  const navigate = useNavigate();
  const { selectedProfile, selectedPlate, currentWeight, setCurrentWeight, setLastResult } = useAppStore();
  
  const [status, setStatus] = useState('tare'); // tare, ready, measuring, capturing, analyzing
  const [progress, setProgress] = useState(0);
  const [ws, setWs] = useState(null);
  const [showTareModal, setShowTareModal] = useState(true);

  // WebSocket ile gerçek zamanlı ağırlık
  useEffect(() => {
    const websocket = connectWeightStream((weight) => {
      setCurrentWeight(weight);
    });
    setWs(websocket);

    // Fallback: Her saniye ağırlık güncelle
    const pollInterval = setInterval(async () => {
      try {
        const weight = await getWeight();
        setCurrentWeight(weight);
      } catch (error) {
        console.error('Ağırlık polling hatası:', error);
      }
    }, 1000);

    return () => {
      if (websocket) websocket.close();
      clearInterval(pollInterval);
    };
  }, [setCurrentWeight]);

  const handleTareComplete = (plate) => {
    setShowTareModal(false);
    setStatus('ready');
    // Tara seçimi tamamlandı, taramayı başlat
    setTimeout(() => {
      startScanning(plate);
    }, 500);
  };

  const startScanning = async (plate) => {
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
      
      // 3. Backend'den tam tarama yap (tabak ID'si ile)
      const result = await scanComplete(plate?.id || null);
      
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
      
      // Backend'den gelen hata mesajını al
      let errorMessage = 'Bir hata oluştu. Lütfen tekrar deneyin.';
      
      if (error.response?.data?.detail) {
        // Backend'den gelen özel hata mesajı
        errorMessage = error.response.data.detail;
      } else if (error.response?.status === 400) {
        errorMessage = 'Geçersiz istek. Lütfen kontrol edin.';
      } else if (error.response?.status === 500) {
        errorMessage = 'Sunucu hatası. Lütfen tekrar deneyin.';
      } else if (error.message.includes('timeout')) {
        errorMessage = 'İşlem zaman aşımına uğradı. Lütfen tekrar deneyin.';
      } else if (error.message.includes('Network Error')) {
        errorMessage = 'Bağlantı hatası. Backend çalışıyor mu kontrol edin.';
      }
      
      alert(errorMessage);
      navigate('/');
    }
  };

  return (
    <WallpaperBackground>
    <div className="h-full w-full p-8 flex flex-col">
      {/* Tara Modal */}
      <TareModal
        isOpen={showTareModal}
        onClose={() => {
          setShowTareModal(false);
          navigate('/');
        }}
        onSelectPlate={handleTareComplete}
      />

      {/* Scanning Content - Modal açıkken blur/opacity ile gizle */}
      <div className={`flex flex-col h-full transition-all duration-300 ${showTareModal ? 'opacity-0 pointer-events-none' : 'opacity-100'}`}>
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

        <img 
          src="/icon.png" 
          alt="Nutriquant Logo" 
          className="w-14 h-14 object-contain"
        />

        <div className="w-12" /> {/* Spacer */}
      </div>

      {/* Scanning Animation */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="flex-1 glass rounded-3xl overflow-hidden relative flex items-center justify-center"
      >
        <div className="text-center p-8">
          {/* Dairesel Progress */}
          <div className="relative inline-flex items-center justify-center mb-8">
            {/* Arka plan çember */}
            <svg className="w-48 h-48 transform -rotate-90">
              <circle
                cx="96"
                cy="96"
                r="88"
                stroke="rgba(255, 255, 255, 0.1)"
                strokeWidth="8"
                fill="none"
              />
              {/* Progress çember */}
              <motion.circle
                cx="96"
                cy="96"
                r="88"
                stroke="url(#gradient)"
                strokeWidth="8"
                fill="none"
                strokeLinecap="round"
                initial={{ strokeDasharray: '0 552' }}
                animate={{ strokeDasharray: `${(progress / 100) * 552} 552` }}
                transition={{ duration: 0.5, ease: 'easeInOut' }}
              />
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#10b981" />
                  <stop offset="100%" stopColor="#3b82f6" />
                </linearGradient>
              </defs>
            </svg>
            
            {/* Ortadaki ikon ve yüzde */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              {status === 'tare' && <Scale size={48} className="text-white mb-2" />}
              {status === 'measuring' && <Scale size={48} className="text-white mb-2" />}
              {status === 'capturing' && <Camera size={48} className="text-white mb-2" />}
              {status === 'analyzing' && <Loader2 size={48} className="text-white mb-2" />}
              {status === 'ready' && <Loader2 size={48} className="text-white mb-2" />}
              <span className="text-3xl font-bold text-white">{progress}%</span>
            </div>
          </div>
          
          {/* Durum Mesajı */}
          <p className="text-2xl text-white font-semibold mb-2">
            {status === 'tare' && 'Tara Alma'}
            {status === 'ready' && 'Sistem Hazırlanıyor'}
            {status === 'measuring' && 'Ağırlık Ölçülüyor'}
            {status === 'capturing' && 'Fotoğraf Çekiliyor'}
            {status === 'analyzing' && 'AI Analiz Yapıyor'}
          </p>
          
          <p className="text-lg text-white/60">
            {status === 'tare' ? 'Tabağınızı seçin veya kaydedin' : 'Lütfen bekleyin...'}
          </p>
        </div>
      </motion.div>

      {/* Info */}
      <div className="mt-4 flex justify-between text-white/80 text-lg">
        <span>Ağırlık: {currentWeight.toFixed(0)}g</span>
        <span>Profil: {selectedProfile?.name}</span>
      </div>
      </div> {/* Scanning Content wrapper end */}
    </div>
    </WallpaperBackground>
  );
}
