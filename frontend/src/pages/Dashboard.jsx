import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Scale, Camera, Users, Settings as SettingsIcon, Battery, Zap } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import { getProfiles, getBattery, connectWeightStream, getWeight, playSound } from '../services/api';
import WallpaperBackground from '../components/WallpaperBackground';

export default function Dashboard() {
  console.log('🎯 Dashboard component rendering...');
  
  const navigate = useNavigate();
  const { selectedProfile, setSelectedProfile, currentWeight, setCurrentWeight, batteryPercent, setBatteryPercent } = useAppStore();
  
  const [profiles, setProfiles] = useState([]);
  const [ws, setWs] = useState(null);
  
  console.log('🎯 Dashboard state:', { selectedProfile, currentWeight, batteryPercent, profilesCount: profiles.length });

  // Profilleri yükle
  useEffect(() => {
    console.log('🔄 Dashboard mounting - loading data...');
    loadProfiles().catch(err => console.error('Profile load failed:', err));
    loadBattery().catch(err => console.error('Battery load failed:', err));
  }, []);

  // Ağırlık gösterimi kaldırıldı - WebSocket ve polling artık gerekli değil
  // useEffect(() => {
  //   console.log('🔌 Connecting to weight WebSocket...');
  //   let websocket = null;
  //   
  //   try {
  //     websocket = connectWeightStream((weight) => {
  //       setCurrentWeight(weight);
  //     });
  //     setWs(websocket);
  //     console.log('✅ WebSocket connected');
  //   } catch (error) {
  //     console.error('❌ WebSocket connection failed:', error);
  //   }
  //
  //   // Fallback: Her saniye ağırlık güncelle (WebSocket bağlantısı kesilirse)
  //   const pollInterval = setInterval(async () => {
  //     try {
  //       const weight = await getWeight();
  //       setCurrentWeight(weight);
  //     } catch (error) {
  //       console.error('Ağırlık polling hatası:', error);
  //     }
  //   }, 1000);
  //
  //   return () => {
  //     if (websocket) {
  //       try {
  //         websocket.close();
  //       } catch (e) {
  //         console.error('WebSocket close error:', e);
  //       }
  //     }
  //     clearInterval(pollInterval);
  //   };
  // }, [setCurrentWeight]);

  const loadProfiles = async () => {
    try {
      const data = await getProfiles();
      setProfiles(data);
    } catch (error) {
      console.error('Profil yükleme hatası:', error);
    }
  };

  const loadBattery = async () => {
    try {
      const data = await getBattery();
      setBatteryPercent(data.percentage);
    } catch (error) {
      console.error('Batarya hatası:', error);
    }
  };

  const handleScan = async () => {
    if (!selectedProfile) {
      await playSound('warning');
      return;
    }
    await playSound('beep');
    navigate('/scanning');
  };

  console.log('🎨 Dashboard rendering JSX...');
  
  return (
    <WallpaperBackground gradient="from-blue-600 via-purple-600 to-pink-500">
    <div className="h-full w-full p-3 overflow-hidden flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center mb-2">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <img 
            src="/icon.png" 
            alt="Nutriquant Logo" 
            className="w-18 h-12 object-contain"
          />
        </motion.div>

        {/* Settings & Battery */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-2"
        >
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => navigate('/settings')}
            className="glass rounded-full p-2 text-white"
          >
            <SettingsIcon size={18} />
          </motion.button>
          
          <div className="glass rounded-full px-4 py-2 flex items-center gap-2">
            <Battery size={18} className="text-white" />
            <span className="text-white font-semibold text-sm">{batteryPercent}%</span>
          </div>
        </motion.div>
      </div>

      {/* Main Content - Tek Kutucuk */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass-ios rounded-3xl p-4 flex-1 flex flex-col min-h-0"
      >
        {/* Profiller - Neon Hexagon Tasarım */}
        <div className="flex-1 flex flex-col justify-center min-h-0">
          {profiles.length === 0 ? (
            <div className="text-center text-white/60 py-4">
              <Users size={40} className="mx-auto mb-2 opacity-50" />
              <p className="text-base mb-1">Henüz profil yok</p>
              <button
                onClick={() => navigate('/profiles')}
                className="mt-2 text-sm text-white underline"
              >
                Profil Ekle
              </button>
            </div>
          ) : (
            <div className="overflow-x-auto pb-2">
              <div className="flex gap-6 justify-start min-w-max px-2">
                {profiles.map((profile, index) => (
                  <motion.div
                    key={profile.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    whileHover={{ scale: 1.08, y: -5 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => {
                      setSelectedProfile(profile);
                      playSound('beep');
                    }}
                    className="relative flex flex-col items-center cursor-pointer"
                  >
                    {/* Neon Hexagon Çerçeve */}
                    <div className="relative">
                      {/* Hexagon SVG */}
                      <svg width="120" height="140" viewBox="0 0 120 140" className="absolute inset-0">
                        <defs>
                          <linearGradient id={`gradient-${profile.id}`} x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor={selectedProfile?.id === profile.id ? '#a855f7' : '#ffffff'} stopOpacity="0.3" />
                            <stop offset="100%" stopColor={selectedProfile?.id === profile.id ? '#ec4899' : '#ffffff'} stopOpacity="0.1" />
                          </linearGradient>
                          <filter id={`glow-${profile.id}`}>
                            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                            <feMerge>
                              <feMergeNode in="coloredBlur"/>
                              <feMergeNode in="SourceGraphic"/>
                            </feMerge>
                          </filter>
                        </defs>
                        {/* Hexagon path */}
                        <path
                          d="M60 10 L100 35 L100 85 L60 110 L20 85 L20 35 Z"
                          fill={`url(#gradient-${profile.id})`}
                          stroke={selectedProfile?.id === profile.id ? '#a855f7' : 'rgba(255,255,255,0.3)'}
                          strokeWidth={selectedProfile?.id === profile.id ? '3' : '2'}
                          filter={selectedProfile?.id === profile.id ? `url(#glow-${profile.id})` : 'none'}
                          className="transition-all duration-300"
                        />
                      </svg>
                      
                      {/* Avatar İçerik */}
                      <div className="relative w-[120px] h-[140px] flex flex-col items-center justify-center">
                        <div
                          className={`w-20 h-20 rounded-full flex items-center justify-center text-3xl font-bold transition-all ${
                            selectedProfile?.id === profile.id
                              ? 'bg-gradient-to-br from-purple-500 to-pink-500 text-white shadow-2xl'
                              : 'bg-white/20 text-white backdrop-blur-sm'
                          }`}
                        >
                          {profile.name.charAt(0).toUpperCase()}
                        </div>
                        
                        {/* Seçili işareti */}
                        {selectedProfile?.id === profile.id && (
                          <motion.div
                            initial={{ scale: 0, rotate: -180 }}
                            animate={{ scale: 1, rotate: 0 }}
                            className="absolute -bottom-2"
                          >
                            <div className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-full p-1.5">
                              <Zap size={16} className="text-white" fill="white" />
                            </div>
                          </motion.div>
                        )}
                      </div>
                    </div>
                    
                    {/* İsim */}
                    <p
                      className={`mt-2 text-sm font-bold transition-all ${
                        selectedProfile?.id === profile.id
                          ? 'text-white drop-shadow-lg'
                          : 'text-white/70'
                      }`}
                    >
                      {profile.name}
                    </p>
                    
                    {/* Profil Bilgisi */}
                    <p className="text-xs text-white/50 mt-0.5">
                      {profile.height}cm • {profile.weight}kg
                    </p>
                  </motion.div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Tara ve Analiz Et Butonu */}
        <motion.button
          whileHover={{ scale: selectedProfile ? 1.02 : 1 }}
          whileTap={{ scale: selectedProfile ? 0.98 : 1 }}
          onClick={handleScan}
          disabled={!selectedProfile}
          className={`w-full py-4 rounded-2xl text-lg font-bold transition-all mt-3 ${
            selectedProfile
              ? 'bg-white text-purple-600 shadow-2xl'
              : 'bg-white/20 text-white/50 cursor-not-allowed'
          }`}
        >
          <div className="flex items-center justify-center gap-2">
            <Camera size={24} />
            <span>Tara ve Analiz Et</span>
          </div>
        </motion.button>
        
        {!selectedProfile && (
          <p className="text-white/60 text-xs mt-2 text-center">Lütfen bir profil seçin</p>
        )}
      </motion.div>
    </div>
    </WallpaperBackground>
  );
}
