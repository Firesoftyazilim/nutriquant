import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Scale, Camera, Users, Settings as SettingsIcon, Battery, Zap } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import { getProfiles, getBattery, connectWeightStream, getWeight, playSound } from '../services/api';

export default function Dashboard() {
  const navigate = useNavigate();
  const { selectedProfile, setSelectedProfile, currentWeight, setCurrentWeight, batteryPercent, setBatteryPercent } = useAppStore();
  
  const [profiles, setProfiles] = useState([]);
  const [ws, setWs] = useState(null);

  // Profilleri yükle
  useEffect(() => {
    console.log('🔄 Dashboard mounting - loading data...');
    loadProfiles().catch(err => console.error('Profile load failed:', err));
    loadBattery().catch(err => console.error('Battery load failed:', err));
  }, []);

  // WebSocket ile gerçek zamanlı ağırlık
  useEffect(() => {
    console.log('🔌 Connecting to weight WebSocket...');
    let websocket = null;
    
    try {
      websocket = connectWeightStream((weight) => {
        setCurrentWeight(weight);
      });
      setWs(websocket);
      console.log('✅ WebSocket connected');
    } catch (error) {
      console.error('❌ WebSocket connection failed:', error);
    }

    // Fallback: Her saniye ağırlık güncelle (WebSocket bağlantısı kesilirse)
    const pollInterval = setInterval(async () => {
      try {
        const weight = await getWeight();
        setCurrentWeight(weight);
      } catch (error) {
        console.error('Ağırlık polling hatası:', error);
      }
    }, 1000);

    return () => {
      if (websocket) {
        try {
          websocket.close();
        } catch (e) {
          console.error('WebSocket close error:', e);
        }
      }
      clearInterval(pollInterval);
    };
  }, [setCurrentWeight]);

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

  return (
    <div className="h-screen w-screen bg-gradient-to-br from-blue-600 via-purple-600 to-pink-500 p-4 overflow-hidden flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-2"
        >
          <Scale size={28} className="text-white" />
          <h1 className="text-2xl font-bold text-white">Nutriquant</h1>
        </motion.div>

        {/* Battery */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass rounded-full px-4 py-2 flex items-center gap-2"
        >
          <Battery size={18} className="text-white" />
          <span className="text-white font-semibold text-sm">{batteryPercent}%</span>
        </motion.div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-2 gap-4 flex-1 min-h-0">
        {/* Left: Weight Display */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass rounded-2xl p-4 flex flex-col items-center justify-center"
        >
          <Scale size={40} className="text-white/60 mb-2" />
          <motion.div
            animate={{ scale: currentWeight > 0 ? 1.05 : 1 }}
            transition={{ duration: 0.3 }}
            className="text-center"
          >
            <h2 className="text-6xl font-bold text-white mb-1">
              {currentWeight.toFixed(0)}
            </h2>
            <p className="text-xl text-white/80">gram</p>
          </motion.div>

          {/* Scan Button */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleScan}
            disabled={!selectedProfile || currentWeight < 10}
            className={`mt-4 w-full py-4 rounded-xl text-lg font-bold transition-all ${
              selectedProfile && currentWeight >= 10
                ? 'bg-white text-purple-600 shadow-2xl'
                : 'bg-white/20 text-white/50 cursor-not-allowed'
            }`}
          >
            <div className="flex items-center justify-center gap-2">
              <Camera size={24} />
              <span>Tara ve Analiz Et</span>
            </div>
          </motion.button>
        </motion.div>

        {/* Right: Profiles */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass rounded-2xl p-4 flex flex-col"
        >
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Users size={24} />
              Profiller
            </h2>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => navigate('/profiles')}
              className="bg-white/20 hover:bg-white/30 text-white rounded-full p-2"
            >
              <SettingsIcon size={18} />
            </motion.button>
          </div>

          {/* Profile List */}
          <div className="flex-1 overflow-y-auto space-y-2">
            {profiles.length === 0 ? (
              <div className="text-center text-white/60 py-6">
                <Users size={32} className="mx-auto mb-2 opacity-50" />
                <p className="text-base">Henüz profil yok</p>
                <button
                  onClick={() => navigate('/profiles')}
                  className="mt-2 text-sm text-white underline"
                >
                  Profil Ekle
                </button>
              </div>
            ) : (
              profiles.map((profile) => (
                <motion.div
                  key={profile.id}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => {
                    setSelectedProfile(profile);
                    playSound('beep');
                  }}
                  className={`p-3 rounded-lg cursor-pointer transition-all ${
                    selectedProfile?.id === profile.id
                      ? 'bg-white text-purple-600 shadow-xl'
                      : 'bg-white/10 text-white hover:bg-white/20'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-base font-bold">{profile.name}</h3>
                      <p className="text-xs opacity-80">
                        {profile.height} cm • {profile.weight} kg • {profile.gender}
                      </p>
                    </div>
                    {selectedProfile?.id === profile.id && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="w-5 h-5 bg-purple-600 rounded-full flex items-center justify-center"
                      >
                        <Zap size={12} className="text-white" fill="white" />
                      </motion.div>
                    )}
                  </div>
                </motion.div>
              ))
            )}
          </div>
        </motion.div>
      </div>

      {/* Bottom Navigation */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="flex justify-center gap-3 mt-3"
      >
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => navigate('/profiles')}
          className="glass rounded-full p-3 text-white"
        >
          <Users size={20} />
        </motion.button>
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => navigate('/settings')}
          className="glass rounded-full p-3 text-white"
        >
          <SettingsIcon size={20} />
        </motion.button>
      </motion.div>
    </div>
  );
}
