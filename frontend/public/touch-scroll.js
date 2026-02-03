/**
 * Touch Scroll Handler - Raspberry Pi için dokunmatik kaydırma
 * Tüm scrollable elementlerde dokunmatik kaydırma desteği ekler
 */

(function() {
  'use strict';

  console.log('🖐️ Touch Scroll Handler başlatıldı');

  let startY = 0;
  let startX = 0;
  let startScrollTop = 0;
  let startScrollLeft = 0;
  let isScrolling = false;
  let scrollElement = null;

  // Scrollable element bul
  function findScrollableParent(element) {
    if (!element) return null;
    
    const overflowY = window.getComputedStyle(element).overflowY;
    const isScrollable = overflowY !== 'visible' && overflowY !== 'hidden';
    
    if (isScrollable && element.scrollHeight > element.clientHeight) {
      return element;
    }
    
    return findScrollableParent(element.parentElement);
  }

  // Pointer down - Dokunma başladı
  document.addEventListener('pointerdown', (e) => {
    // Touch veya mouse kontrolü
    if (e.pointerType !== 'touch' && e.pointerType !== 'mouse') return;
    
    // Scrollable element bul
    scrollElement = findScrollableParent(e.target);
    
    if (!scrollElement) {
      // Eğer scrollable parent yoksa document.scrollingElement kullan
      scrollElement = document.scrollingElement || document.documentElement;
    }
    
    startY = e.clientY;
    startX = e.clientX;
    startScrollTop = scrollElement.scrollTop;
    startScrollLeft = scrollElement.scrollLeft;
    isScrolling = true;
    
    // Smooth scroll'u geçici olarak kapat (performans için)
    scrollElement.style.scrollBehavior = 'auto';
  }, { passive: true });

  // Pointer move - Dokunma hareket ediyor
  document.addEventListener('pointermove', (e) => {
    if (!isScrolling) return;
    if (e.buttons !== 1 && e.pointerType === 'mouse') return;
    
    e.preventDefault();
    
    const deltaY = startY - e.clientY;
    const deltaX = startX - e.clientX;
    
    // Dikey kaydırma
    if (scrollElement) {
      scrollElement.scrollTop = startScrollTop + deltaY;
      scrollElement.scrollLeft = startScrollLeft + deltaX;
    }
  }, { passive: false });

  // Pointer up - Dokunma bitti
  document.addEventListener('pointerup', () => {
    if (isScrolling && scrollElement) {
      // Smooth scroll'u geri aç
      scrollElement.style.scrollBehavior = '';
    }
    isScrolling = false;
    scrollElement = null;
  }, { passive: true });

  // Pointer cancel - Dokunma iptal edildi
  document.addEventListener('pointercancel', () => {
    if (isScrolling && scrollElement) {
      scrollElement.style.scrollBehavior = '';
    }
    isScrolling = false;
    scrollElement = null;
  }, { passive: true });

  // Momentum scrolling için (isteğe bağlı)
  let lastY = 0;
  let lastTime = 0;
  let velocity = 0;
  let momentumAnimation = null;

  document.addEventListener('pointermove', (e) => {
    if (!isScrolling) return;
    
    const now = Date.now();
    const deltaTime = now - lastTime;
    
    if (deltaTime > 0) {
      velocity = (lastY - e.clientY) / deltaTime;
    }
    
    lastY = e.clientY;
    lastTime = now;
  }, { passive: true });

  document.addEventListener('pointerup', () => {
    if (!isScrolling || !scrollElement) return;
    
    // Momentum scrolling
    if (Math.abs(velocity) > 0.5) {
      if (momentumAnimation) {
        cancelAnimationFrame(momentumAnimation);
      }
      
      const startVelocity = velocity;
      const friction = 0.95;
      let currentVelocity = startVelocity;
      
      function animate() {
        if (Math.abs(currentVelocity) < 0.1 || !scrollElement) {
          momentumAnimation = null;
          return;
        }
        
        scrollElement.scrollTop += currentVelocity * 16; // 16ms frame
        currentVelocity *= friction;
        
        momentumAnimation = requestAnimationFrame(animate);
      }
      
      animate();
    }
    
    velocity = 0;
  }, { passive: true });

  console.log('✅ Touch Scroll Handler hazır');
})();
