import { motion } from 'framer-motion';
import { AlertTriangle, RefreshCw, Search } from 'lucide-react';

export default function LowConfidenceModal({ 
  isOpen, 
  onClose, 
  data, 
  onRetryAnalysis, 
  onManualSelect 
}) {
  if (!isOpen || !data) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="bg-white rounded-2xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto"
      >
        {/* Header */}
        <div className="flex items-center justify-center mb-4">
          <div className="bg-orange-100 p-3 rounded-full">
            <AlertTriangle className="text-orange-600" size={24} />
          </div>
        </div>

        <h2 className="text-xl font-bold text-center mb-2 text-gray-800">
          Düşük Doğruluk Tespit Edildi
        </h2>

        <p className="text-gray-600 text-center mb-4">
          Tahmin doğruluğu %{data.percentage?.toFixed(1)} olarak tespit edildi. 
          Bu değer %65'in altında olduğu için manuel seçim yapmanız önerilir.
        </p>

        {/* Tahmin Sonuçları */}
        <div className="bg-gray-50 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-gray-800 mb-3">Tahmin Sonuçları:</h3>
          <div className="space-y-2">
            {data.predictions?.slice(0, 3).map((pred, index) => (
              <div 
                key={index}
                className="flex justify-between items-center p-2 bg-white rounded border"
              >
                <span className="font-medium text-gray-700">
                  {pred.display_name || pred.food_name}
                </span>
                <span className="text-sm text-gray-500">
                  %{pred.percentage?.toFixed(1)}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Ağırlık Bilgisi */}
        <div className="bg-blue-50 rounded-lg p-3 mb-6">
          <p className="text-sm text-blue-800">
            <strong>Ölçülen Ağırlık:</strong> {data.weight}g
          </p>
        </div>

        {/* Aksiyon Butonları */}
        <div className="space-y-3">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onManualSelect}
            className="w-full bg-blue-600 text-white py-3 px-4 rounded-xl font-semibold flex items-center justify-center gap-2"
          >
            <Search size={20} />
            Manuel Besin Seç
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onRetryAnalysis}
            className="w-full bg-orange-600 text-white py-3 px-4 rounded-xl font-semibold flex items-center justify-center gap-2"
          >
            <RefreshCw size={20} />
            Tekrar Analiz Et
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onClose}
            className="w-full bg-gray-300 text-gray-700 py-3 px-4 rounded-xl font-semibold"
          >
            İptal
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
}
