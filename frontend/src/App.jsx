import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { useEffect } from 'react';
import Dashboard from './pages/Dashboard';
import Scanning from './pages/Scanning';
import Results from './pages/Results';
import Profiles from './pages/Profiles';
import Settings from './pages/Settings';
import WallpaperSelector from './pages/WallpaperSelector';
import History from './pages/History';
import SplashScreen from './pages/SplashScreen';
import { useAppStore } from './store/appStore';
import { checkHealth } from './services/api';

function App() {
  const { isLoading, setLoading } = useAppStore();

  useEffect(() => {
    // Backend bağlantısını kontrol et (arka planda)
    const checkBackend = async () => {
      try {
        console.log('🔍 Backend bağlantısı kontrol ediliyor...');
        await checkHealth();
        console.log('✅ Backend bağlantısı başarılı');
      } catch (error) {
        console.warn('⚠️ Backend bağlantı kurulamadı:', error.message);
        console.warn('Uygulama çalışmaya devam edecek ancak bazı özellikler çalışmayabilir.');
      }
    };

    // Başlangıç yüklemesi
    console.log('⏳ Splash screen 2 saniye gösteriliyor...');
    setTimeout(() => {
      console.log('✅ Splash screen tamamlandı, Dashboard yükleniyor...');
      setLoading(false);
    }, 2000);

    // Backend kontrolünü arka planda yap
    checkBackend();
  }, [setLoading]);

  if (isLoading) {
    console.log('📺 Rendering: SplashScreen');
    return <SplashScreen />;
  }

  console.log('📺 Rendering: Router (Main App)');
  console.log('   isLoading:', isLoading);
  
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/scanning" element={<Scanning />} />
        <Route path="/results" element={<Results />} />
        <Route path="/profiles" element={<Profiles />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/wallpaper" element={<WallpaperSelector />} />
        <Route path="/history/:profileId" element={<History />} />
      </Routes>
    </Router>
  );
}

export default App;
