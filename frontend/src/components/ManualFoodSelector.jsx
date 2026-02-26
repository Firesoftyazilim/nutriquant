import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Search, X, Check } from 'lucide-react';
import { getFoodList } from '../services/api';

export default function ManualFoodSelector({ 
  isOpen, 
  onClose, 
  onSelect,
  weight 
}) {
  const [foods, setFoods] = useState([]);
  const [filteredFoods, setFilteredFoods] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedFood, setSelectedFood] = useState(null);
  const searchInputRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      loadFoods();
      // Modal açıldığında input'a focus ver (klavye tetiklemesi için)
      setTimeout(() => {
        if (searchInputRef.current) {
          searchInputRef.current.focus();
          searchInputRef.current.click(); // Mobile cihazlarda klavye tetiklemesi için
          
          // Raspberry Pi touchscreen için ek tetikleme
          const touchEvent = new TouchEvent('touchstart', {
            bubbles: true,
            cancelable: true,
            touches: [{
              identifier: 0,
              target: searchInputRef.current,
              clientX: 0,
              clientY: 0
            }]
          });
          searchInputRef.current.dispatchEvent(touchEvent);
        }
      }, 500); // Timeout'u artır
    }
  }, [isOpen]);

  useEffect(() => {
    if (searchTerm) {
      const filtered = foods.filter(food => 
        food.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredFoods(filtered);
    } else {
      setFilteredFoods(foods);
    }
  }, [searchTerm, foods]);

  const loadFoods = async () => {
    setLoading(true);
    try {
      const response = await getFoodList();
      setFoods(response.foods || []);
      setFilteredFoods(response.foods || []);
    } catch (error) {
      console.error('Besin listesi yüklenemedi:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFoodSelect = (food) => {
    setSelectedFood(food);
  };

  const handleConfirm = () => {
    if (selectedFood) {
      // Ağırlığa göre besin değerlerini hesapla
      const weightRatio = weight / 100.0;
      const calculatedNutrition = {
        name: selectedFood.name,
        weight: weight,
        calorie: Math.round(selectedFood.calorie * weightRatio * 10) / 10,
        protein: Math.round(selectedFood.protein * weightRatio * 10) / 10,
        carbohydrate: Math.round(selectedFood.carbohydrate * weightRatio * 10) / 10,
        sugar: Math.round((selectedFood.sugar || 0) * weightRatio * 10) / 10,
        base_values_per_100g: selectedFood
      };

      onSelect({
        status: 'manual_selected',
        food_name: selectedFood.name,
        nutrition: calculatedNutrition,
        weight: weight,
        manual_selection: true
      });
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="bg-white rounded-2xl w-full max-w-lg max-h-[90vh] flex flex-col"
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-xl font-bold text-gray-800">
            Manuel Besin Seçimi
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full"
          >
            <X size={20} />
          </button>
        </div>

        {/* Ağırlık Bilgisi */}
        <div className="px-6 py-3 bg-blue-50">
          <p className="text-sm text-blue-800">
            <strong>Ölçülen Ağırlık:</strong> {weight}g
          </p>
        </div>

        {/* Arama */}
        <div className="p-6 border-b">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            <input
              ref={searchInputRef}
              type="text"
              placeholder="Besin ara..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onTouchStart={(e) => {
                // Mobile cihazlarda dokunma ile klavye tetiklemesi
                e.target.focus();
              }}
              onFocus={() => {
                // Focus olduğunda klavye açılması için
                console.log('Input focused - klavye açılmalı');
              }}
              onClick={() => {
                // Click ile de klavye tetiklemesi
                if (searchInputRef.current) {
                  searchInputRef.current.focus();
                }
              }}
              autoFocus={isOpen}
              inputMode="text"
              autoComplete="off"
              autoCorrect="off"
              spellCheck="false"
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-base"
              style={{ fontSize: '16px' }} // iOS'ta zoom'u önlemek için
            />
          </div>
        </div>

        {/* Besin Listesi */}
        <div className="flex-1 overflow-y-auto p-6">
          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-2 text-gray-600">Besinler yükleniyor...</p>
            </div>
          ) : (
            <div className="space-y-2">
              {filteredFoods.map((food, index) => (
                <motion.button
                  key={index}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => handleFoodSelect(food)}
                  className={`w-full p-4 text-left rounded-xl border transition-colors ${
                    selectedFood?.name === food.name
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-semibold text-gray-800">
                        {food.name}
                      </h3>
                      <p className="text-sm text-gray-600">
                        {food.calorie} kcal/100g • Protein: {food.protein}g
                      </p>
                    </div>
                    {selectedFood?.name === food.name && (
                      <Check className="text-blue-600" size={20} />
                    )}
                  </div>
                </motion.button>
              ))}
              
              {filteredFoods.length === 0 && !loading && (
                <div className="text-center py-8">
                  <p className="text-gray-600">Besin bulunamadı</p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-6 border-t">
          <div className="flex gap-3">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={onClose}
              className="flex-1 bg-gray-300 text-gray-700 py-3 px-4 rounded-xl font-semibold"
            >
              İptal
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleConfirm}
              disabled={!selectedFood}
              className={`flex-1 py-3 px-4 rounded-xl font-semibold ${
                selectedFood
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
              }`}
            >
              Seç ve Devam Et
            </motion.button>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
