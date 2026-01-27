import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Save, RotateCcw, Flame, Beef, Wheat, Droplet } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import { saveMeasurement, playSound } from '../services/api';
import WallpaperBackground from '../components/WallpaperBackground';

export default function Results() {
  const navigate = useNavigate();
  const { lastResult, selectedProfile } = useAppStore();

  if (!lastResult) {
    navigate('/');
    return null;
  }

  // Model prediction results with nutrition
  const { food_name, confidence, percentage, weight, nutrition, predictions, profile } = lastResult;

  const handleSave = async () => {
    try {
      await saveMeasurement({
        user_id: selectedProfile?.id || 1,
        food_name: food_name,
        weight: weight,
        nutrition: nutrition,
        bmi_data: { bmi: 0, comment: '-' }
      });
      await playSound('success');
      navigate('/');
    } catch (error) {
      console.error('Kayıt hatası:', error);
    }
  };

  const handleRetry = async () => {
    await playSound('beep');
    navigate('/scanning');
  };

  const nutritionItems = [
    { icon: Flame, label: 'Kalori', value: nutrition?.calorie || 0, unit: 'kcal', color: 'from-orange-400 to-red-500' },
    { icon: Beef, label: 'Protein', value: nutrition?.protein || 0, unit: 'g', color: 'from-red-400 to-pink-500' },
    { icon: Wheat, label: 'Karbonhidrat', value: nutrition?.carbohydrate || 0, unit: 'g', color: 'from-yellow-400 to-orange-500' },
    { icon: Droplet, label: 'Şeker', value: nutrition?.sugar || 0, unit: 'g', color: 'from-blue-400 to-cyan-500' },
  ];

  return (
    <WallpaperBackground>
    <div className="h-full w-full p-4 flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center mb-3 flex-shrink-0">
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

      {/* Scrollable Content */}
      <div className="flex-1 overflow-y-auto pb-4">
        {/* Food Name & Confidence */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-2xl p-4 mb-3 text-center"
        >
          <motion.h2
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 200 }}
            className="text-3xl font-bold text-white mb-1"
          >
            {food_name}
          </motion.h2>
          <div className="flex items-center justify-center gap-3 text-white/80">
            <span className="text-lg">{weight?.toFixed(0) || 0}g</span>
            <span className="text-lg">•</span>
            <span className="text-lg">%{percentage?.toFixed(1) || 0} güven</span>
          </div>
        </motion.div>

        {/* Nutrition Grid */}
        <div className="grid grid-cols-2 gap-3 mb-3">
          {nutritionItems.map((item, index) => (
            <motion.div
              key={item.label}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              className="glass rounded-2xl p-4"
            >
              <div className={`inline-flex p-2 rounded-xl bg-gradient-to-br ${item.color} mb-2`}>
                <item.icon size={24} className="text-white" />
              </div>
              <p className="text-white/70 text-xs mb-0.5">{item.label}</p>
              <p className="text-white text-2xl font-bold">
                {item.value.toFixed(1)} <span className="text-base font-normal">{item.unit}</span>
              </p>
            </motion.div>
          ))}
        </div>

        {/* Top 5 Predictions */}
        {predictions && predictions.length > 1 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="glass rounded-2xl p-4 mb-3"
          >
            <h3 className="text-white text-lg font-bold mb-3">Diğer Tahminler</h3>
            <div className="space-y-2">
              {predictions.slice(1, 5).map((pred, index) => (
                <div key={index} className="flex justify-between items-center">
                  <span className="text-white/80 text-sm">{index + 2}. {pred.food_name}</span>
                  <span className="text-white font-semibold text-sm">%{pred.percentage.toFixed(1)}</span>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="grid grid-cols-2 gap-3 flex-shrink-0">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleRetry}
          className="glass rounded-2xl py-4 text-white text-lg font-semibold flex items-center justify-center gap-2"
        >
          <RotateCcw size={20} />
          Tekrar Tara
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleSave}
          className="bg-white text-green-600 rounded-2xl py-4 text-lg font-bold flex items-center justify-center gap-2 shadow-2xl"
        >
          <Save size={20} />
          Kaydet
        </motion.button>
      </div>
    </div>
    </WallpaperBackground>
  );
}
