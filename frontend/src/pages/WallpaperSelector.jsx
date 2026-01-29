import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Check } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import { setWallpaper as setWallpaperAPI } from '../services/api';
import WallpaperBackground from '../components/WallpaperBackground';

// Wallpaper listesi
const wallpapers = [
  { id: 'coffe', name: 'Kahve', file: 'coffe800x480.jpg' },
  { id: 'iridescent', name: 'Gökkuşağı', file: 'iridescent_liquid 800x480.jpg' },
  { id: 'clover', name: 'Yonca', file: 'lucky_clover800x480.jpg' },
  { id: 'mountain', name: 'Dağ', file: 'mountain-800x480.jpg' },
  { id: 'winter', name: 'Kış', file: 'scenic_winter 800x480.jpg' },
  { id: 'tunnel', name: 'Tünel', file: 'tree_tunnel800x480.jpg' },
  { id: 'default', name: 'Varsayılan', file: null }, // Gradient arkaplan
];

export default function WallpaperSelector() {
  const navigate = useNavigate();
  const { currentWallpaper, setCurrentWallpaper } = useAppStore();
  const [selectedWallpaper, setSelectedWallpaper] = useState(currentWallpaper || 'default');
  const [saving, setSaving] = useState(false);

  const handleSelectWallpaper = async (wallpaper) => {
    setSelectedWallpaper(wallpaper.id);
    setSaving(true);

    try {
      // Backend'e kaydet
      await setWallpaperAPI(wallpaper.id);
      
      // Global state'e kaydet
      setCurrentWallpaper(wallpaper.id);
      
      // LocalStorage'a kaydet
      localStorage.setItem('nutriquant_wallpaper', wallpaper.id);
      
      // Kısa bir süre sonra geri dön
      setTimeout(() => {
        setSaving(false);
        navigate('/settings');
      }, 500);
    } catch (error) {
      console.error('Wallpaper kaydetme hatası:', error);
      setSaving(false);
      alert('Arkaplan kaydedilemedi. Lütfen tekrar deneyin.');
    }
  };

  return (
    <WallpaperBackground>
    <div className="h-full w-full p-6 flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => navigate('/settings')}
          className="glass rounded-full p-3 text-white"
          disabled={saving}
        >
          <ArrowLeft size={24} />
        </motion.button>

        <img 
          src="/icon.png" 
          alt="Nutriquant Logo" 
          className="w-50 h-10 object-contain"
        />

        <div className="w-12" />
      </div>

      {/* Wallpaper Grid */}
      <div className="flex-1 grid grid-cols-2 gap-4 overflow-y-auto pb-4 pr-2 overscroll-contain scroll-smooth touch-pan-y">
        {wallpapers.map((wallpaper, index) => (
          <motion.button
            key={wallpaper.id}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.05 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => handleSelectWallpaper(wallpaper)}
            disabled={saving}
            className={`relative rounded-2xl overflow-hidden h-32 ${
              selectedWallpaper === wallpaper.id ? 'ring-4 ring-white' : ''
            }`}
          >
            {/* Wallpaper Preview */}
            {wallpaper.file ? (
              <img
                src={`/Wallpapers/${wallpaper.file}`}
                alt={wallpaper.name}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full bg-gradient-to-br from-blue-600 via-purple-600 to-pink-500" />
            )}

            {/* Overlay */}
            <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
              <div className="text-center">
                <p className="text-white font-bold text-lg drop-shadow-lg">
                  {wallpaper.name}
                </p>
                {selectedWallpaper === wallpaper.id && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="mt-2 inline-flex items-center justify-center w-8 h-8 bg-white rounded-full"
                  >
                    <Check size={20} className="text-green-600" />
                  </motion.div>
                )}
              </div>
            </div>
          </motion.button>
        ))}
      </div>

      {/* Info */}
      {saving && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 glass rounded-2xl p-4 text-center"
        >
          <p className="text-white text-sm">Arkaplan kaydediliyor...</p>
        </motion.div>
      )}
    </div>
    </WallpaperBackground>
  );
}
