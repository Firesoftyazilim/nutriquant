import { motion } from 'framer-motion';
import { User, Zap } from 'lucide-react';

export default function ProfileCard({ profile, isSelected, onSelect, delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay }}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onSelect}
      className={`p-4 rounded-xl cursor-pointer transition-all ${
        isSelected
          ? 'bg-white text-purple-600 shadow-xl'
          : 'bg-white/10 text-white hover:bg-white/20'
      }`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
            isSelected ? 'bg-purple-100' : 'bg-white/20'
          }`}>
            <User size={24} className={isSelected ? 'text-purple-600' : 'text-white'} />
          </div>
          <div>
            <h3 className="text-xl font-bold">{profile.name}</h3>
            <p className={`text-sm ${isSelected ? 'opacity-70' : 'opacity-80'}`}>
              {profile.height} cm • {profile.weight} kg • {profile.gender}
            </p>
          </div>
        </div>
        
        {isSelected && (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="w-6 h-6 bg-purple-600 rounded-full flex items-center justify-center"
          >
            <Zap size={16} className="text-white" fill="white" />
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}
