import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Image as ImageIcon, UtensilsCrossed } from 'lucide-react';
import { getSettings } from '../services/api';
import WallpaperBackground from '../components/WallpaperBackground';

export default function Settings() {
  const navigate = useNavigate();
  const [settings, setSettings] = useState({
    wallpaper: null,
    soundEnabled: true,
    brightness: 100
  });

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const data = await getSettings();
      setSettings(data);
    } catch (error) {
      console.error('Ayar yükleme hatası:', error);
    }
  };

  const settingsItems = [
    {
      icon: ImageIcon,
      title: 'Arka Plan',
      description: 'Arka plan resmini değiştir',
      action: () => navigate('/wallpaper'),
      color: 'from-purple-400 to-pink-500'
    }
  ];

  return (
    <WallpaperBackground>
    <div className="h-full w-full p-6 flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center mb-4 flex-shrink-0">
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => navigate('/')}
          className="glass rounded-full p-2 text-white"
        >
          <ArrowLeft size={24} />
        </motion.button>

        <img 
          src="/icon.png" 
          alt="Nutriquant Logo" 
          className="w-18 h-12 object-contain"
        />

        <div className="w-10" />
      </div>

      {/* Settings Grid */}
      <div className="flex-1 flex items-center justify-center">
        <div className="grid grid-cols-2 gap-4 max-w-2xl w-full">
          {/* Arka Plan */}
          <motion.button
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/wallpaper')}
            className="glass rounded-3xl p-6 text-center"
          >
            <div className="inline-flex p-3 rounded-2xl bg-gradient-to-br from-purple-400 to-pink-500 mb-3">
              <ImageIcon size={40} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-white mb-1">Arka Plan</h3>
            <p className="text-white/70 text-sm">Arka plan değiştir</p>
          </motion.button>

          {/* Yemek Listesi */}
          <motion.button
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/food-list')}
            className="glass rounded-3xl p-6 text-center"
          >
            <div className="inline-flex p-3 rounded-2xl bg-gradient-to-br from-green-400 to-emerald-500 mb-3">
              <UtensilsCrossed size={40} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-white mb-1">Yemek Listesi</h3>
            <p className="text-white/70 text-sm">Tanınabilir yemekler</p>
          </motion.button>
        </div>
      </div>

      {/* App Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="glass rounded-xl p-3 text-center flex-shrink-0 mt-2"
      >
        <p className="text-white/70 text-sm font-semibold">Nutriquant v1.0.0</p>
        <p className="text-white/50 text-xs mt-1">Created by Firesoft</p>
      </motion.div>
    </div>
    </WallpaperBackground>
  );
}
