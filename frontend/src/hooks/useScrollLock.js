import { useEffect } from 'react';

/**
 * Scroll lock hook - Belirli bir element dışında scroll'u engeller
 * Touch scroll için optimize edilmiş
 */
export function useScrollLock(enabled = true) {
  useEffect(() => {
    if (!enabled) return;

    const originalStyle = window.getComputedStyle(document.body).overflow;
    
    // Body scroll'u kilitle
    document.body.style.overflow = 'hidden';
    document.body.style.position = 'fixed';
    document.body.style.width = '100%';
    document.body.style.height = '100%';

    return () => {
      // Cleanup - Eski duruma döndür
      document.body.style.overflow = originalStyle;
      document.body.style.position = '';
      document.body.style.width = '';
      document.body.style.height = '';
    };
  }, [enabled]);
}

/**
 * Touch scroll momentum hook - iOS-style momentum scrolling
 */
export function useTouchScroll(ref) {
  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    let startY = 0;
    let startScrollTop = 0;
    let isDragging = false;
    let velocity = 0;
    let lastY = 0;
    let lastTime = Date.now();
    let momentumId = null;

    const handleTouchStart = (e) => {
      isDragging = true;
      startY = e.touches[0].clientY;
      lastY = startY;
      startScrollTop = element.scrollTop;
      velocity = 0;
      lastTime = Date.now();
      
      // Momentum animasyonunu durdur
      if (momentumId) {
        cancelAnimationFrame(momentumId);
        momentumId = null;
      }
    };

    const handleTouchMove = (e) => {
      if (!isDragging) return;

      const currentY = e.touches[0].clientY;
      const deltaY = startY - currentY;
      const currentTime = Date.now();
      const deltaTime = currentTime - lastTime;

      // Velocity hesapla (momentum için)
      if (deltaTime > 0) {
        velocity = (currentY - lastY) / deltaTime;
      }

      element.scrollTop = startScrollTop + deltaY;

      lastY = currentY;
      lastTime = currentTime;
    };

    const handleTouchEnd = () => {
      isDragging = false;

      // Momentum scrolling uygula
      if (Math.abs(velocity) > 0.5) {
        const deceleration = 0.95;
        let currentVelocity = velocity * 30; // Velocity'yi scale et

        const momentum = () => {
          currentVelocity *= deceleration;
          element.scrollTop -= currentVelocity;

          // Velocity çok düşükse dur
          if (Math.abs(currentVelocity) > 0.5) {
            momentumId = requestAnimationFrame(momentum);
          }
        };

        momentum();
      }
    };

    // Touch event listeners
    element.addEventListener('touchstart', handleTouchStart, { passive: true });
    element.addEventListener('touchmove', handleTouchMove, { passive: true });
    element.addEventListener('touchend', handleTouchEnd, { passive: true });

    return () => {
      element.removeEventListener('touchstart', handleTouchStart);
      element.removeEventListener('touchmove', handleTouchMove);
      element.removeEventListener('touchend', handleTouchEnd);
      
      if (momentumId) {
        cancelAnimationFrame(momentumId);
      }
    };
  }, [ref]);
}
