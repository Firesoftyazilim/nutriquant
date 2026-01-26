import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Save, RotateCcw, Flame, Beef, Wheat, Droplet } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import { saveMeasurement, playSound } from '../services/api';

export default function Results() {
  const navigate = useNavigate();
  const { lastResult, selectedProfile } = useAppStore();

  if (!lastResult) {
    navigate('/');
    return null;
  }

  // Model prediction results
  const { food_name, confidence, percentage, weight, predictions, image, profile } = lastResult;

  const handleSave = async () => {
    try {
      await saveMeasurement({
        user_id: selectedProfile?.id || 1,
        food_name: food_name,
        weight: weight,
        nutrition: { name: food_name, weight: weight },
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

  return (
    <div className="h-screen w-screen bg-gradient-to-br from-green-600 via-emerald-600 to-teal-500 p-8 flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => navigate('/')}
          className="glass rounded-full p-3 text-white"
        >
          <ArrowLeft size={28} />
        </motion.button>

        <h1 className="text-3xl font-bold text-white">Analiz Sonucu</h1>

        <div className="w-12" />
      </div>

      {/* Captured Image */}
      {image && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass rounded-3xl overflow-hidden mb-6"
        >
          <img 
            src={image} 
            alt="Captured food" 
            className="w-full h-64 object-cover"
          />
        </motion.div>
      )}

      {/* Food Name & Confidence */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-3xl p-6 mb-6 text-center"
      >
        <motion.h2
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 200 }}
          className="text-5xl font-bold text-white mb-2"
        >
          {food_name}
        </motion.h2>
        <div className="flex items-center justify-center gap-4 text-white/80">
          <span className="text-xl">{weight.toFixed(0)}g</span>
          <span className="text-xl">•</span>
          <span className="text-xl">%{percentage.toFixed(1)} güven</span>
        </div>
      </motion.div>

      {/* Top 5 Predictions */}
      {predictions && predictions.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass rounded-3xl p-6 mb-6"
        >
          <h3 className="text-white text-xl font-bold mb-4">Diğer Tahminler</h3>
          <div className="space-y-3">
            {predictions.slice(0, 5).map((pred, index) => (
              <div key={index} className="flex justify-between items-center">
                <span className="text-white/80">{index + 1}. {pred.food_name}</span>
                <span className="text-white font-semibold">%{pred.percentage.toFixed(1)}</span>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Action Buttons */}
      <div className="grid grid-cols-2 gap-4">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleRetry}
          className="glass rounded-2xl py-6 text-white text-xl font-semibold flex items-center justify-center gap-2"
        >
          <RotateCcw size={24} />
          Tekrar Tara
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleSave}
          className="bg-white text-green-600 rounded-2xl py-6 text-xl font-bold flex items-center justify-center gap-2 shadow-2xl"
        >
          <Save size={24} />
          Kaydet
        </motion.button>
      </div>
    </div>
  );
}
