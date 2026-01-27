import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Plus, Edit2, Trash2, User, Save, X } from 'lucide-react';
import { getProfiles, createProfile, updateProfile, deleteProfile, playSound } from '../services/api';
import WallpaperBackground from '../components/WallpaperBackground';
import TouchKeyboard from '../components/TouchKeyboard';

export default function Profiles() {
  const navigate = useNavigate();
  const [profiles, setProfiles] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingProfile, setEditingProfile] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    gender: 'Erkek',
    height: '',
    weight: ''
  });
  const [activeInput, setActiveInput] = useState(null);
  const [showKeyboard, setShowKeyboard] = useState(false);

  useEffect(() => {
    loadProfiles();
  }, []);

  const loadProfiles = async () => {
    try {
      const data = await getProfiles();
      setProfiles(data);
    } catch (error) {
      console.error('Profil yükleme hatası:', error);
    }
  };

  const handleAddProfile = () => {
    setEditingProfile(null);
    setFormData({ name: '', gender: 'Erkek', height: '', weight: '' });
    setShowForm(true);
    setShowKeyboard(false);
    setActiveInput(null);
    playSound('beep');
  };

  const handleEditProfile = (profile) => {
    setEditingProfile(profile);
    setFormData({
      name: profile.name,
      gender: profile.gender,
      height: profile.height,
      weight: profile.weight
    });
    setShowForm(true);
    setShowKeyboard(false);
    setActiveInput(null);
    playSound('beep');
  };

  const handleDeleteProfile = async (profileId) => {
    if (confirm('Bu profili silmek istediğinize emin misiniz?')) {
      try {
        await deleteProfile(profileId);
        await loadProfiles();
        await playSound('success');
      } catch (error) {
        console.error('Silme hatası:', error);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name || !formData.height || !formData.weight) {
      alert('Lütfen tüm alanları doldurun');
      return;
    }

    try {
      const profileData = {
        name: formData.name,
        gender: formData.gender,
        height: parseInt(formData.height),
        weight: parseInt(formData.weight)
      };

      if (editingProfile) {
        await updateProfile(editingProfile.id, profileData);
      } else {
        await createProfile(profileData);
      }

      await loadProfiles();
      setShowForm(false);
      await playSound('success');
    } catch (error) {
      console.error('Kayıt hatası:', error);
      alert('Bir hata oluştu');
    }
  };

  const handleCloseForm = () => {
    setShowForm(false);
    setEditingProfile(null);
    setFormData({ name: '', gender: 'Erkek', height: '', weight: '' });
    setShowKeyboard(false);
    setActiveInput(null);
  };

  const handleInputFocus = (inputName) => {
    setActiveInput(inputName);
    setShowKeyboard(true);
  };

  const handleKeyPress = (key) => {
    if (activeInput) {
      setFormData(prev => ({
        ...prev,
        [activeInput]: prev[activeInput] + key
      }));
    }
  };

  const handleBackspace = () => {
    if (activeInput) {
      setFormData(prev => ({
        ...prev,
        [activeInput]: prev[activeInput].slice(0, -1)
      }));
    }
  };

  const handleKeyboardClose = () => {
    setShowKeyboard(false);
    setActiveInput(null);
  };

  return (
    <WallpaperBackground gradient="from-indigo-600 via-purple-600 to-pink-500">
    <div className="h-full w-full p-8 flex flex-col">
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

        <img 
          src="/icon.png" 
          alt="Nutriquant Logo" 
          className="w-18 h-12 object-contain"
        />

        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={handleAddProfile}
          className="glass rounded-full p-3 text-white"
        >
          <Plus size={28} />
        </motion.button>
      </div>

      {/* Profile List */}
      <div className="flex-1 overflow-y-auto space-y-4">
        <AnimatePresence>
          {profiles.map((profile, index) => (
            <motion.div
              key={profile.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ delay: index * 0.05 }}
              className="glass rounded-2xl p-6"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 rounded-full bg-white/20 flex items-center justify-center">
                    <User size={32} className="text-white" />
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold text-white">{profile.name}</h3>
                    <p className="text-white/70">
                      {profile.height} cm • {profile.weight} kg • {profile.gender}
                    </p>
                  </div>
                </div>

                <div className="flex gap-2">
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => handleEditProfile(profile)}
                    className="bg-white/20 hover:bg-white/30 rounded-full p-3 text-white"
                  >
                    <Edit2 size={20} />
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => handleDeleteProfile(profile.id)}
                    className="bg-red-500/30 hover:bg-red-500/50 rounded-full p-3 text-white"
                  >
                    <Trash2 size={20} />
                  </motion.button>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {profiles.length === 0 && (
          <div className="text-center text-white/60 py-20">
            <User size={64} className="mx-auto mb-4 opacity-50" />
            <p className="text-2xl">Henüz profil eklenmemiş</p>
            <p className="text-lg mt-2">Sağ üstteki + butonuna tıklayın</p>
          </div>
        )}
      </div>

      {/* Profile Form Modal */}
      <AnimatePresence>
        {showForm && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
            onClick={() => setShowForm(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ 
                scale: 1, 
                opacity: 1
              }}
              exit={{ scale: 0.9, opacity: 0 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              onClick={(e) => e.stopPropagation()}
              className="glass rounded-3xl p-8 w-[500px] max-w-[90vw]"
            >
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-white">
                  {editingProfile ? 'Profil Düzenle' : 'Yeni Profil'}
                </h2>
                <button
                  onClick={() => setShowForm(false)}
                  className="text-white/60 hover:text-white"
                >
                  <X size={24} />
                </button>
              </div>

              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Name */}
                <div>
                  <label className="block text-white/80 mb-2">İsim</label>
                  <input
                    type="text"
                    value={formData.name}
                    onFocus={() => handleInputFocus('name')}
                    readOnly
                    className={`w-full bg-white/10 border rounded-xl px-4 py-3 text-white text-lg focus:outline-none cursor-pointer transition-all ${
                      activeInput === 'name' ? 'border-white/60 bg-white/20' : 'border-white/20'
                    }`}
                    placeholder="Örn: Ahmet"
                  />
                </div>

                {/* Gender */}
                <div>
                  <label className="block text-white/80 mb-2">Cinsiyet</label>
                  <div className="flex gap-4">
                    {['Erkek', 'Kadın'].map((gender) => (
                      <button
                        key={gender}
                        type="button"
                        onClick={() => setFormData({ ...formData, gender })}
                        className={`flex-1 py-3 rounded-xl text-lg font-semibold transition-all ${
                          formData.gender === gender
                            ? 'bg-white text-purple-600'
                            : 'bg-white/10 text-white'
                        }`}
                      >
                        {gender}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Height & Weight */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-white/80 mb-2">Boy (cm)</label>
                    <input
                      type="text"
                      value={formData.height}
                      onFocus={() => handleInputFocus('height')}
                      readOnly
                      className={`w-full bg-white/10 border rounded-xl px-4 py-3 text-white text-lg focus:outline-none cursor-pointer transition-all ${
                        activeInput === 'height' ? 'border-white/60 bg-white/20' : 'border-white/20'
                      }`}
                      placeholder="175"
                    />
                  </div>
                  <div>
                    <label className="block text-white/80 mb-2">Kilo (kg)</label>
                    <input
                      type="text"
                      value={formData.weight}
                      onFocus={() => handleInputFocus('weight')}
                      readOnly
                      className={`w-full bg-white/10 border rounded-xl px-4 py-3 text-white text-lg focus:outline-none cursor-pointer transition-all ${
                        activeInput === 'weight' ? 'border-white/60 bg-white/20' : 'border-white/20'
                      }`}
                      placeholder="70"
                    />
                  </div>
                </div>

                {/* Submit Button */}
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  type="submit"
                  className="w-full bg-white text-purple-600 rounded-xl py-4 text-xl font-bold flex items-center justify-center gap-2 shadow-xl"
                >
                  <Save size={24} />
                  {editingProfile ? 'Güncelle' : 'Kaydet'}
                </motion.button>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Touch Keyboard */}
      <AnimatePresence>
        {showKeyboard && (
          <TouchKeyboard
            onKeyPress={handleKeyPress}
            onBackspace={handleBackspace}
            onClose={handleKeyboardClose}
            type={activeInput === 'name' ? 'text' : 'numeric'}
            currentValue={formData[activeInput] || ''}
            label={
              activeInput === 'name' ? 'İsim' :
              activeInput === 'height' ? 'Boy (cm)' :
              activeInput === 'weight' ? 'Kilo (kg)' : ''
            }
          />
        )}
      </AnimatePresence>
    </div>
    </WallpaperBackground>
  );
}
