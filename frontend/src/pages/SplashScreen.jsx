import { motion } from 'framer-motion';

export default function SplashScreen() {
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
