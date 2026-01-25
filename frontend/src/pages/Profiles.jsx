import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Plus, Edit2, Trash2, User, Save, X } from 'lucide-react';
import { getProfiles, createProfile, updateProfile, deleteProfile, playSound } from '../services/api';

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
    playSound('beep');
  };

  const handleEditProfile = (profile) => {
    setEditingProfile(profile);
    setFormData({
      name: profile.name,
      gender: profile.gender,
      height: profile.height.toString(),
      weight: profile.weight.toString()
    });
    setShowForm(true);
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

  return (
    <div className="h-screen w-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 p-8 flex flex-col">
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

        <h1 className="text-3xl font-bold text-white">Profil Yönetimi</h1>

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
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
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
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white text-lg focus:outline-none focus:border-white/40"
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
                      type="number"
                      value={formData.height}
                      onChange={(e) => setFormData({ ...formData, height: e.target.value })}
                      className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white text-lg focus:outline-none focus:border-white/40"
                      placeholder="175"
                    />
                  </div>
                  <div>
                    <label className="block text-white/80 mb-2">Kilo (kg)</label>
                    <input
                      type="number"
                      value={formData.weight}
                      onChange={(e) => setFormData({ ...formData, weight: e.target.value })}
                      className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white text-lg focus:outline-none focus:border-white/40"
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
    </div>
  );
}
