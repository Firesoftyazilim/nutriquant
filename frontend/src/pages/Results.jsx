import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Save, RotateCcw, Flame, Beef, Wheat, Droplet } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import { saveMeasurement, playSound } from '../services/api';

export default function Results() {
  const navigate = useNavigate();
  const { lastResult, selectedProfile } = useAppStore();

  if (!lastResult || !lastResult.nutrition) {
    navigate('/');
    return null;
  }

  const { nutrition, confidence, bmi } = lastResult;

  const handleSave = async () => {
    try {
      await saveMeasurement({
        user_id: selectedProfile?.id || 1,
        food_name: nutrition.name,
        weight: nutrition.weight,
        nutrition: nutrition,
        bmi_data: bmi || { bmi: 0, comment: '-' }
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
    { icon: Flame, label: 'Kalori', value: nutrition.calorie, unit: 'kcal', color: 'from-orange-400 to-red-500' },
    { icon: Beef, label: 'Protein', value: nutrition.protein, unit: 'g', color: 'from-red-400 to-pink-500' },
    { icon: Wheat, label: 'Karbonhidrat', value: nutrition.carb, unit: 'g', color: 'from-yellow-400 to-orange-500' },
    { icon: Droplet, label: 'Yağ', value: nutrition.fat, unit: 'g', color: 'from-blue-400 to-cyan-500' },
  ];

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
          {nutrition.name}
        </motion.h2>
        <div className="flex items-center justify-center gap-4 text-white/80">
          <span className="text-xl">{nutrition.weight}g</span>
          <span className="text-xl">•</span>
          <span className="text-xl">%{(confidence * 100).toFixed(0)} güven</span>
        </div>
      </motion.div>

      {/* Nutrition Grid */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        {nutritionItems.map((item, index) => (
          <motion.div
            key={item.label}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 }}
            className="glass rounded-2xl p-6"
          >
            <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${item.color} mb-3`}>
              <item.icon size={32} className="text-white" />
            </div>
            <p className="text-white/70 text-sm mb-1">{item.label}</p>
            <p className="text-white text-3xl font-bold">
              {item.value.toFixed(1)} <span className="text-xl font-normal">{item.unit}</span>
            </p>
          </motion.div>
        ))}
      </div>

      {/* BMI Info (if available) */}
      {bmi && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="glass rounded-2xl p-4 mb-6"
        >
          <p className="text-white/70 text-sm mb-1">Vücut Kitle İndeksi</p>
          <p className="text-white text-xl">
            <span className="font-bold">{bmi.bmi.toFixed(1)}</span> - {bmi.comment}
          </p>
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
