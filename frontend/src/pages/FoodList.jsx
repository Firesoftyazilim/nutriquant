import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Search, UtensilsCrossed, Flame, Beef, Wheat } from 'lucide-react';
import { getFoods } from '../services/api';
import WallpaperBackground from '../components/WallpaperBackground';

export default function FoodList() {
  const navigate = useNavigate();
  const [foods, setFoods] = useState([]);
  const [filteredFoods, setFilteredFoods] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFoods();
  }, []);

  useEffect(() => {
    if (searchTerm.trim() === '') {
      setFilteredFoods(foods);
    } else {
      const filtered = foods.filter(food =>
        food.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredFoods(filtered);
    }
  }, [searchTerm, foods]);

  const loadFoods = async () => {
    try {
      setLoading(true);
      const data = await getFoods();
      setFoods(data.foods);
      setFilteredFoods(data.foods);
    } catch (error) {
      console.error('Yemek listesi yükleme hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <WallpaperBackground>
      <div className="h-full w-full p-6 flex flex-col">
        {/* Header */}
        <div className="flex justify-between items-center mb-4 flex-shrink-0">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => navigate('/settings')}
            className="glass rounded-full p-2 text-white"
          >
            <ArrowLeft size={24} />
          </motion.button>

          <div className="text-center">
            <h1 className="text-2xl font-bold text-white">Yemek Listesi</h1>
            <p className="text-white/60 text-sm">{filteredFoods.length} yemek</p>
          </div>

          <div className="w-10" />
        </div>

        {/* Search */}
        <div className="mb-4 flex-shrink-0">
          <div className="glass rounded-2xl p-3 flex items-center gap-3">
            <Search size={20} className="text-white/60" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Yemek ara..."
              className="flex-1 bg-transparent text-white placeholder-white/40 focus:outline-none"
            />
          </div>
        </div>

        {/* Food List */}
        <div className="flex-1 overflow-y-auto">
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-white/60 text-center">
                <UtensilsCrossed size={48} className="mx-auto mb-2 animate-pulse" />
                <p>Yükleniyor...</p>
              </div>
            </div>
          ) : filteredFoods.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-white/60 text-center">
                <UtensilsCrossed size={48} className="mx-auto mb-2 opacity-50" />
                <p>Yemek bulunamadı</p>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-3 pb-4">
              {filteredFoods.map((food, index) => (
                <motion.div
                  key={food.key}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.02 }}
                  className="glass rounded-2xl p-4"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="text-white font-bold text-lg mb-2">{food.name}</h3>
                      <div className="grid grid-cols-3 gap-2">
                        <div className="flex items-center gap-1">
                          <Flame size={14} className="text-orange-400" />
                          <span className="text-white/80 text-sm">{food.calorie} kcal</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Beef size={14} className="text-red-400" />
                          <span className="text-white/80 text-sm">{food.protein}g</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Wheat size={14} className="text-yellow-400" />
                          <span className="text-white/80 text-sm">{food.carbohydrate}g</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="mt-2 pt-2 border-t border-white/10">
                    <p className="text-white/40 text-xs">100g başına besin değerleri</p>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </div>
    </WallpaperBackground>
  );
}
