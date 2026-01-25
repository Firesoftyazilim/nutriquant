import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Volume2, Sun, Image as ImageIcon, TestTube } from 'lucide-react';
import { getSettings, setWallpaper, playSound, controlLED } from '../services/api';

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

  const handleTestSound = async () => {
    await playSound('beep');
    setTimeout(() => playSound('success'), 500);
  };

  const handleTestLED = async () => {
    const colors = ['red', 'green', 'blue', 'yellow', 'white'];
    for (const color of colors) {
      await controlLED(color);
      await new Promise(resolve => setTimeout(resolve, 300));
    }
    await controlLED('off');
  };

  const settingsItems = [
    {
      icon: Volume2,
      title: 'Ses Testi',
      description: 'Hoparlörü test et',
      action: handleTestSound,
      color: 'from-blue-400 to-cyan-500'
    },
    {
      icon: Sun,
      title: 'LED Testi',
      description: 'LED halkayı test et',
      action: handleTestLED,
      color: 'from-yellow-400 to-orange-500'
    },
    {
      icon: ImageIcon,
      title: 'Arka Plan',
      description: 'Arka plan resmini değiştir',
      action: () => alert('Arka plan seçimi yakında...'),
      color: 'from-purple-400 to-pink-500'
    },
    {
      icon: TestTube,
      title: 'Test Modu',
      description: 'Donanım testleri',
      action: () => alert('Test modu yakında...'),
      color: 'from-green-400 to-emerald-500'
    }
  ];

  return (
    <div className="h-screen w-screen bg-gradient-to-br from-slate-700 via-gray-800 to-zinc-900 p-8 flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => navigate('/')}
          className="glass rounded-full p-3 text-white"
        >
          <ArrowLeft size={28} />
        </motion.button>

        <h1 className="text-3xl font-bold text-white">Ayarlar</h1>

        <div className="w-12" />
      </div>

      {/* Settings Grid */}
      <div className="grid grid-cols-2 gap-6">
        {settingsItems.map((item, index) => (
          <motion.button
            key={item.title}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={item.action}
            className="glass rounded-3xl p-8 text-left"
          >
            <div className={`inline-flex p-4 rounded-2xl bg-gradient-to-br ${item.color} mb-4`}>
              <item.icon size={40} className="text-white" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-2">{item.title}</h3>
            <p className="text-white/70 text-lg">{item.description}</p>
          </motion.button>
        ))}
      </div>

      {/* App Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="mt-auto glass rounded-2xl p-6 text-center"
      >
        <p className="text-white/60 text-sm">Nutriquant v2.0.0</p>
        <p className="text-white/40 text-xs mt-1">Electron + React + Python FastAPI</p>
      </motion.div>
    </div>
  );
}
