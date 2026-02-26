import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { playSound } from '../services/api';

export default function SplashScreen() {
  useEffect(() => {
    playOpeningSound();
  }, []);

  const playOpeningSound = async () => {
    console.log('🔊 Opening sound playing...');
    try {
      // HTML5 Audio API kullanarak açılış sesi çal
      const audio = new Audio('/opening-sound.mp3');
      audio.volume = 1;
      audio.preload = 'auto';
      
      // Browser autoplay policy için promise-based approach
      const playPromise = audio.play();
      
      if (playPromise !== undefined) {
        await playPromise;
        console.log('🔊 Opening sound played successfully');
      }
    } catch (error) {
      console.error('Opening sound play error (autoplay blocked):', error);
      
      // Autoplay engellendiyse, kullanıcı etkileşimi bekle
      const handleUserInteraction = async () => {
        try {
          const audio = new Audio('/opening-sound.mp3');
          audio.volume = 1;
          await audio.play();
          console.log('🔊 Opening sound played after user interaction');
          
          // Event listener'ı kaldır
          document.removeEventListener('click', handleUserInteraction);
          document.removeEventListener('touchstart', handleUserInteraction);
          document.removeEventListener('keydown', handleUserInteraction);
        } catch (retryError) {
          console.error('Retry sound play error:', retryError);
        }
      };
      
      // İlk kullanıcı etkileşiminde sesi çal
      document.addEventListener('click', handleUserInteraction, { once: true });
      document.addEventListener('touchstart', handleUserInteraction, { once: true });
      document.addEventListener('keydown', handleUserInteraction, { once: true });
      
      // Fallback: Backend API ile ses çalmayı dene
      try {
        await playSound('startup');
      } catch (backendError) {
        console.error('Backend sound play error:', backendError);
      }
    }
  };

  return (
    <div className="h-screen w-screen bg-gradient-to-br from-blue-500 via-green-500 to-yellow-400 flex items-center justify-center">
      {/* Sadece Logo - Büyüyerek Gelen */}
      <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ 
          duration: 0.8,
          ease: [0.34, 1.56, 0.64, 1], // Spring-like easing
        }}
        className="inline-block"
      >
        <img 
          src="/icon.png" 
          alt="Nutriquant Logo" 
          className="w-104 h-104 object-contain drop-shadow-2xl"
        />
      </motion.div>
    </div>
  );
}
