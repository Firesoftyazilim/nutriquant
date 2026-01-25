import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useEffect } from 'react';
import Dashboard from './pages/Dashboard';
import Scanning from './pages/Scanning';
import Results from './pages/Results';
import Profiles from './pages/Profiles';
import Settings from './pages/Settings';
import SplashScreen from './pages/SplashScreen';
import { useAppStore } from './store/appStore';

function App() {
  const { isLoading, setLoading } = useAppStore();

  useEffect(() => {
    // Başlangıç yüklemesi
    const timer = setTimeout(() => {
      setLoading(false);
    }, 2000);

    return () => clearTimeout(timer);
  }, [setLoading]);

  if (isLoading) {
    return <SplashScreen />;
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
