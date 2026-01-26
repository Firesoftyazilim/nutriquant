import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Dashboard from './pages/Dashboard';
import Scanning from './pages/Scanning';
import Results from './pages/Results';
import Profiles from './pages/Profiles';
import Settings from './pages/Settings';
import SplashScreen from './pages/SplashScreen';
import { useAppStore } from './store/appStore';
import { checkHealth } from './services/api';

function App() {
  const { isLoading, setLoading } = useAppStore();
  const [backendError, setBackendError] = useState(null);

  useEffect(() => {
    // Backend bağlantısını kontrol et
    const checkBackend = async () => {
      try {
        console.log('🔍 Backend bağlantısı kontrol ediliyor...');
        await checkHealth();
        console.log('✅ Backend bağlantısı başarılı');
        setBackendError(null);
      } catch (error) {
        console.error('❌ Backend bağlantı hatası:', error.message);
        setBackendError(error.message);
      } finally {
        // Başlangıç yüklemesi
        console.log('⏳ Splash screen 2 saniye gösteriliyor...');
        setTimeout(() => {
          console.log('✅ Splash screen tamamlandı, Dashboard yükleniyor...');
          setLoading(false);
        }, 2000);
      }
    };

    checkBackend();
  }, [setLoading]);

  if (isLoading) {
    return <SplashScreen />;
  }

  // Backend bağlantı hatası varsa göster
  if (backendError) {
    return (
      <div className="h-screen w-screen bg-gradient-to-br from-red-600 via-orange-600 to-yellow-500 flex items-center justify-center p-8">
        <div className="glass rounded-3xl p-8 max-w-2xl text-center">
          <h1 className="text-4xl font-bold text-white mb-4">⚠️ Backend Bağlantı Hatası</h1>
          <p className="text-xl text-white/90 mb-6">{backendError}</p>
          <p className="text-lg text-white/80">Backend sunucusunun çalıştığından emin olun.</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-6 bg-white text-orange-600 px-8 py-3 rounded-xl font-bold text-lg hover:bg-white/90 transition"
          >
            Yeniden Dene
          </button>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/scanning" element={<Scanning />} />
        <Route path="/results" element={<Results />} />
        <Route path="/profiles" element={<Profiles />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Router>
  );
}

export default App;
