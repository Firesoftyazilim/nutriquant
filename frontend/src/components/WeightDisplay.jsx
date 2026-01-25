import { motion } from 'framer-motion';
import { Scale } from 'lucide-react';

export default function WeightDisplay({ weight, size = 'large' }) {
  const sizes = {
    small: { text: 'text-4xl', icon: 32 },
    medium: { text: 'text-6xl', icon: 48 },
    large: { text: 'text-8xl', icon: 60 }
  };

  const currentSize = sizes[size];

  return (
    <motion.div
      animate={{ scale: weight > 0 ? 1.05 : 1 }}
      transition={{ duration: 0.3 }}
      className="text-center"
    >
      <Scale size={currentSize.icon} className="text-white/60 mx-auto mb-4" />
      <h2 className={`${currentSize.text} font-bold text-white mb-2`}>
        {weight.toFixed(0)}
      </h2>
      <p className="text-2xl text-white/80">gram</p>
    </motion.div>
  );
}
