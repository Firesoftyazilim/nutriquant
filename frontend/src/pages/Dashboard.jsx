import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Scale, Camera, Users, Settings as SettingsIcon, Battery, Zap } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import { getProfiles, getBattery, connectWeightStream, playSound } from '../services/api';

export default function Dashboard() {
  const navigate = useNavigate();
  const { selectedProfile, setSelectedProfile, currentWeight, setCurrentWeight, batteryPercent, setBatteryPercent } = useAppStore();
  
  const [profiles, setProfiles] = useState([]);
  const [ws, setWs] = useState(null);

  // Profilleri yükle
  useEffect(() => {
    loadProfiles();
    loadBattery();
  }, []);

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
    <div className="h-screen w-screen bg-gradient-to-br from-blue-600 via-purple-600 to-pink-500 p-8 overflow-hidden">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-3"
        >
          <Scale size={40} className="text-white" />
          <h1 className="text-4xl font-bold text-white">Nutriquant</h1>
        </motion.div>

        {/* Battery */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass rounded-full px-6 py-3 flex items-center gap-2"
        >
          <Battery size={24} className="text-white" />
          <span className="text-white font-semibold">{batteryPercent}%</span>
        </motion.div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-2 gap-6 h-[calc(100vh-200px)]">
        {/* Left: Weight Display */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass rounded-3xl p-8 flex flex-col items-center justify-center"
        >
          <Scale size={60} className="text-white/60 mb-4" />
          <motion.div
            animate={{ scale: currentWeight > 0 ? 1.05 : 1 }}
            transition={{ duration: 0.3 }}
            className="text-center"
          >
            <h2 className="text-8xl font-bold text-white mb-2">
              {currentWeight.toFixed(0)}
            </h2>
            <p className="text-3xl text-white/80">gram</p>
          </motion.div>

          {/* Scan Button */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleScan}
            disabled={!selectedProfile || currentWeight < 10}
            className={`mt-8 w-full py-6 rounded-2xl text-2xl font-bold transition-all ${
              selectedProfile && currentWeight >= 10
                ? 'bg-white text-purple-600 shadow-2xl'
                : 'bg-white/20 text-white/50 cursor-not-allowed'
            }`}
          >
            <div className="flex items-center justify-center gap-3">
              <Camera size={32} />
              <span>Tara ve Analiz Et</span>
            </div>
          </motion.button>
        </motion.div>

        {/* Right: Profiles */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass rounded-3xl p-8 flex flex-col"
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-3xl font-bold text-white flex items-center gap-2">
              <Users size={32} />
              Profiller
            </h2>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => navigate('/profiles')}
              className="bg-white/20 hover:bg-white/30 text-white rounded-full p-3"
            >
              <SettingsIcon size={24} />
            </motion.button>
          </div>

          {/* Profile List */}
          <div className="flex-1 overflow-y-auto space-y-3">
            {profiles.length === 0 ? (
              <div className="text-center text-white/60 py-12">
                <Users size={48} className="mx-auto mb-4 opacity-50" />
                <p className="text-xl">Henüz profil yok</p>
                <button
                  onClick={() => navigate('/profiles')}
                  className="mt-4 text-white underline"
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
                  className={`p-4 rounded-xl cursor-pointer transition-all ${
                    selectedProfile?.id === profile.id
                      ? 'bg-white text-purple-600 shadow-xl'
                      : 'bg-white/10 text-white hover:bg-white/20'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-xl font-bold">{profile.name}</h3>
                      <p className="text-sm opacity-80">
                        {profile.height} cm • {profile.weight} kg • {profile.gender}
                      </p>
                    </div>
                    {selectedProfile?.id === profile.id && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="w-6 h-6 bg-purple-600 rounded-full flex items-center justify-center"
                      >
                        <Zap size={16} className="text-white" fill="white" />
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
        className="fixed bottom-8 left-1/2 transform -translate-x-1/2 flex gap-4"
      >
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => navigate('/profiles')}
          className="glass rounded-full p-4 text-white"
        >
          <Users size={28} />
        </motion.button>
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => navigate('/settings')}
          className="glass rounded-full p-4 text-white"
        >
          <SettingsIcon size={28} />
        </motion.button>
      </motion.div>
    </div>
  );
}
