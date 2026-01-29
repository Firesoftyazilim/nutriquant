import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Calendar, Clock, Apple, TrendingUp, TrendingDown } from 'lucide-react';
import { getProfileHistory } from '../services/api';
import WallpaperBackground from '../components/WallpaperBackground';

export default function History() {
  const navigate = useNavigate();
  const { profileId } = useParams();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [profileName, setProfileName] = useState('');

  useEffect(() => {
    loadHistory();
  }, [profileId]);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const data = await getProfileHistory(profileId);
      setHistory(data.history || []);
      setProfileName(data.profile_name || 'Kullanıcı');
    } catch (error) {
      console.error('Geçmiş yükleme hatası:', error);
      setHistory([]);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('tr-TR', { 
      day: 'numeric', 
      month: 'long', 
      year: 'numeric' 
    });
  };

  const formatTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('tr-TR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <WallpaperBackground>
    <div className="h-screen w-screen p-4 overflow-hidden flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => navigate('/')}
          className="glass rounded-full p-3 text-white"
        >
          <ArrowLeft size={24} />
        </motion.button>
        
        <h1 className="text-2xl font-bold text-white">
          {profileName} - Geçmiş Taramalar
        </h1>
        
        <div className="w-12"></div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-white text-xl">Yükleniyor...</div>
          </div>
        ) : history.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-white">
            <Apple size={64} className="mb-4 opacity-50" />
            <p className="text-xl font-semibold mb-2">Henüz tarama yok</p>
            <p className="text-white/70">İlk taramanızı yapmak için ana sayfaya dönün</p>
          </div>
        ) : (
          <div className="h-full overflow-y-auto pb-4 overscroll-contain scroll-smooth touch-pan-y">
            <div className="space-y-3">
              {history.map((item, index) => (
                <motion.div
                  key={item.id || index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="glass-ios rounded-2xl p-4"
                >
                  {/* Tarih ve Saat */}
                  <div className="flex items-center gap-4 mb-3 text-white/80 text-sm">
                    <div className="flex items-center gap-1">
                      <Calendar size={16} />
                      <span>{formatDate(item.timestamp)}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Clock size={16} />
                      <span>{formatTime(item.timestamp)}</span>
                    </div>
                  </div>

                  {/* Yemek Bilgisi */}
                  <div className="flex items-start gap-3">
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-white mb-1">
                        {item.food_name}
                      </h3>
                      <p className="text-white/70 text-sm mb-2">
                        {item.weight}g • {item.calories} kcal
                      </p>
                      
                      {/* Besin Değerleri */}
                      <div className="grid grid-cols-3 gap-2 text-xs">
                        <div className="bg-white/10 rounded-lg p-2 text-center">
                          <p className="text-white/60">Protein</p>
                          <p className="text-white font-semibold">{item.protein}g</p>
                        </div>
                        <div className="bg-white/10 rounded-lg p-2 text-center">
                          <p className="text-white/60">Karb.</p>
                          <p className="text-white font-semibold">{item.carbs}g</p>
                        </div>
                        <div className="bg-white/10 rounded-lg p-2 text-center">
                          <p className="text-white/60">Yağ</p>
                          <p className="text-white font-semibold">{item.fat}g</p>
                        </div>
                      </div>
                    </div>

                    {/* Güven Skoru */}
                    <div className="text-right">
                      <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        item.confidence >= 80 
                          ? 'bg-green-500/20 text-green-300' 
                          : item.confidence >= 60 
                          ? 'bg-yellow-500/20 text-yellow-300'
                          : 'bg-red-500/20 text-red-300'
                      }`}>
                        %{item.confidence}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
    </WallpaperBackground>
  );
}
