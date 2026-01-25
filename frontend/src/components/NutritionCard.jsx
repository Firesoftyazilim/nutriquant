import { motion } from 'framer-motion';

export default function NutritionCard({ icon: Icon, label, value, unit, color, delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay }}
      className="glass rounded-2xl p-6"
    >
      <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${color} mb-3`}>
        <Icon size={32} className="text-white" />
      </div>
      <p className="text-white/70 text-sm mb-1">{label}</p>
      <p className="text-white text-3xl font-bold">
        {value.toFixed(1)} <span className="text-xl font-normal">{unit}</span>
      </p>
    </motion.div>
  );
}
