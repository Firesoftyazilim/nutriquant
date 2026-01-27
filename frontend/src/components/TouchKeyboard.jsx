import { motion } from 'framer-motion';
import { Delete } from 'lucide-react';

export default function TouchKeyboard({ onKeyPress, onBackspace, onClose, type = 'text', currentValue = '', label = '' }) {
  // Türkçe klavye düzeni
  const textKeys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Ğ', 'Ü'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ş', 'İ'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Ö', 'Ç']
  ];

  // Sayısal klavye
  const numericKeys = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['0']
  ];

  const keys = type === 'numeric' ? numericKeys : textKeys;

  return (
    <motion.div
      initial={{ y: 300, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      exit={{ y: 300, opacity: 0 }}
      className="fixed bottom-0 left-0 right-0 bg-gradient-to-t from-slate-800 to-slate-700 p-4 shadow-2xl z-50"
    >
      <div className="max-w-2xl mx-auto">
        {/* Preview Area - Yazdığımız Metin */}
        <div className="mb-4 bg-slate-900/50 rounded-2xl p-4 min-h-[80px] flex flex-col justify-center">
          {label && (
            <p className="text-white/60 text-sm mb-2">{label}</p>
          )}
          <div className="text-white text-2xl font-semibold min-h-[40px] flex items-center">
            {currentValue || <span className="text-white/30">...</span>}
            <span className="animate-pulse ml-1">|</span>
          </div>
        </div>
        {/* Klavye Tuşları */}
        <div className="space-y-2 mb-2">
          {keys.map((row, rowIndex) => (
            <div key={rowIndex} className="flex justify-center gap-2">
              {row.map((key) => (
                <motion.button
                  key={key}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => onKeyPress(key)}
                  className="glass text-white font-bold text-xl py-4 px-6 rounded-xl min-w-[60px] hover:bg-white/20 transition-all"
                >
                  {key}
                </motion.button>
              ))}
            </div>
          ))}
        </div>

        {/* Alt Tuşlar */}
        <div className="flex justify-center gap-2">
          {type === 'text' && (
            <motion.button
              whileTap={{ scale: 0.95 }}
              onClick={() => onKeyPress(' ')}
              className="glass text-white font-bold text-lg py-4 px-12 rounded-xl hover:bg-white/20 transition-all"
            >
              Boşluk
            </motion.button>
          )}
          
          <motion.button
            whileTap={{ scale: 0.95 }}
            onClick={onBackspace}
            className="glass text-white font-bold text-lg py-4 px-8 rounded-xl hover:bg-white/20 transition-all flex items-center gap-2"
          >
            <Delete size={20} />
            Sil
          </motion.button>
          
          <motion.button
            whileTap={{ scale: 0.95 }}
            onClick={onClose}
            className="bg-green-500 text-white font-bold text-lg py-4 px-8 rounded-xl hover:bg-green-600 transition-all"
          >
            Tamam
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
}
