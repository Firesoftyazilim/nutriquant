import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Plus, Trash2, Scale, Save } from 'lucide-react';
import { getPlates, createPlate, deletePlate } from '../services/api';
import { useAppStore } from '../store/appStore';
import axios from 'axios';

export default function TareModal({ isOpen, onClose, onSelectPlate }) {
  const { setSelectedPlate } = useAppStore();
  const [plates, setPlates] = useState([]);
  const [currentWeight, setCurrentWeight] = useState(0);
  const [showNewPlate, setShowNewPlate] = useState(false);
  const [newPlateName, setNewPlateName] = useState('');
  const inputRef = useRef(null);

  // Tabakları yükle
  useEffect(() => {
    if (isOpen) {
      loadPlates();
    }
  }, [isOpen]);

  // Ağırlık polling (sadece yeni tabak ekleme modunda)
  useEffect(() => {
    if (isOpen && showNewPlate) {
      // İlk ağırlığı hemen al
      fetchWeight();
      
      // Her 1 saniyede bir ağırlık güncelle
      const pollInterval = setInterval(fetchWeight, 1000);

      // Input'a focus yap (klavye açılsın)
      setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.focus();
          inputRef.current.click(); // Mobil cihazlarda klavye açılması için
        }
      }, 100);

      return () => {
        clearInterval(pollInterval);
      };
    }
  }, [isOpen, showNewPlate]);

  const fetchWeight = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/scale/weight');
      setCurrentWeight(response.data.weight);
    } catch (error) {
      console.error('Ağırlık okuma hatası:', error);
    }
  };

  const loadPlates = async () => {
    try {
      const data = await getPlates();
      setPlates(data);
    } catch (error) {
      console.error('Tabak yükleme hatası:', error);
    }
  };

  const handleSaveNewPlate = async () => {
    if (!newPlateName.trim()) {
      alert('Lütfen tabak adı girin');
      return;
    }

    if (currentWeight < 5) {
      alert('Lütfen tabağı tartıya koyun');
      return;
    }

    try {
      await createPlate({
        name: newPlateName,
        weight: currentWeight
      });
      setNewPlateName('');
      setShowNewPlate(false);
      await loadPlates();
    } catch (error) {
      console.error('Tabak kaydetme hatası:', error);
      alert('Tabak kaydedilemedi');
    }
  };

  const handleDeletePlate = async (plateId) => {
    if (!confirm('Bu tabağı silmek istediğinize emin misiniz?')) {
      return;
    }

    try {
      await deletePlate(plateId);
      await loadPlates();
    } catch (error) {
      console.error('Tabak silme hatası:', error);
      alert('Tabak silinemedi');
    }
  };

  const handleSelectPlate = (plate) => {
    setSelectedPlate(plate);
    onSelectPlate(plate);
    onClose();
  };

  const handleSkip = () => {
    setSelectedPlate(null);
    onSelectPlate(null);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
          className="glass-ios rounded-3xl p-6 max-w-md w-full max-h-[80vh] overflow-y-auto"
        >
          {/* Header */}
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-white">Tara Alma</h2>
            <button
              onClick={onClose}
              className="glass rounded-full p-2 text-white hover:bg-white/20"
            >
              <X size={24} />
            </button>
          </div>

          {/* Yeni Tabak Ekleme */}
          {showNewPlate ? (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass rounded-2xl p-4 mb-4"
            >
              {/* Mevcut Ağırlık - Sadece yeni tabak eklerken göster */}
              <div className="glass rounded-2xl p-4 mb-4 text-center">
                <Scale size={32} className="mx-auto mb-2 text-white" />
                <p className="text-white/60 text-sm mb-1">Mevcut Ağırlık</p>
                <p className="text-3xl font-bold text-white">{currentWeight.toFixed(0)}g</p>
              </div>

              <input
                ref={inputRef}
                type="text"
                value={newPlateName}
                onChange={(e) => setNewPlateName(e.target.value)}
                placeholder="Tabak adı (örn: Beyaz Tabak)"
                className="w-full bg-white/10 text-white placeholder-white/40 rounded-xl px-4 py-3 mb-3 focus:outline-none focus:ring-2 focus:ring-white/30"
                autoFocus
                autoComplete="off"
                inputMode="text"
                onFocus={(e) => e.target.select()}
              />
              <div className="flex gap-2">
                <button
                  onClick={handleSaveNewPlate}
                  className="flex-1 bg-green-500 text-white rounded-xl py-2 font-semibold flex items-center justify-center gap-2"
                >
                  <Save size={18} />
                  Kaydet
                </button>
                <button
                  onClick={() => {
                    setShowNewPlate(false);
                    setNewPlateName('');
                  }}
                  className="flex-1 bg-white/20 text-white rounded-xl py-2 font-semibold"
                >
                  İptal
                </button>
              </div>
            </motion.div>
          ) : (
            <button
              onClick={() => setShowNewPlate(true)}
              className="w-full glass rounded-2xl p-4 mb-4 flex items-center justify-center gap-2 text-white hover:bg-white/20 transition-all"
            >
              <Plus size={20} />
              <span className="font-semibold">Yeni Tabak Kaydet</span>
            </button>
          )}

          {/* Kayıtlı Tabaklar */}
          <div className="space-y-2 mb-4">
            <p className="text-white/60 text-sm mb-2">Kayıtlı Tabaklar</p>
            {plates.length === 0 ? (
              <p className="text-white/40 text-center py-4">Henüz kayıtlı tabak yok</p>
            ) : (
              plates.map((plate) => (
                <motion.div
                  key={plate.id}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="glass rounded-xl p-3 flex items-center justify-between"
                >
                  <button
                    onClick={() => handleSelectPlate(plate)}
                    className="flex-1 text-left"
                  >
                    <p className="text-white font-semibold">{plate.name}</p>
                    <p className="text-white/60 text-sm">{plate.weight.toFixed(0)}g</p>
                  </button>
                  <button
                    onClick={() => handleDeletePlate(plate.id)}
                    className="p-2 text-red-400 hover:bg-red-500/20 rounded-lg"
                  >
                    <Trash2 size={18} />
                  </button>
                </motion.div>
              ))
            )}
          </div>

          {/* Tabaksız Devam Et */}
          <button
            onClick={handleSkip}
            className="w-full bg-white/20 text-white rounded-2xl py-3 font-semibold hover:bg-white/30 transition-all"
          >
            Tabaksız Devam Et
          </button>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
