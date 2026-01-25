# Nutriquant Frontend

Modern Electron + React + TailwindCSS UI

## Özellikler

- ✨ **Glassmorphism Tasarım**: Modern, şeffaf cam efekti
- 🎨 **Framer Motion**: Smooth animasyonlar
- 📱 **Tam Ekran Kiosk Mode**: Raspberry Pi dokunmatik ekran için optimize
- ⚡ **Gerçek Zamanlı**: WebSocket ile anlık ağırlık gösterimi
- 🎯 **React Router**: Sayfa geçişleri
- 🔄 **Zustand**: Global state management

## Geliştirme

```bash
# Kütüphaneleri yükle
npm install

# Geliştirme modu (DevTools açık)
npm run electron:dev

# Production build
npm run build
npm run electron
```

## Teknolojiler

- **Electron**: Desktop app framework
- **React 18**: UI library
- **Vite**: Build tool
- **TailwindCSS**: Utility-first CSS
- **Framer Motion**: Animasyon library
- **Lucide React**: Modern icon set
- **Zustand**: State management
- **Axios**: HTTP client

## Sayfa Yapısı

- `/` - Dashboard (Ana ekran)
- `/scanning` - Tarama ve analiz ekranı
- `/results` - Sonuç gösterimi
- `/profiles` - Profil yönetimi
- `/settings` - Ayarlar

## Kiosk Mode

Production modda uygulama tam ekran açılır ve kullanıcı çıkış yapamaz.

Geliştirme modunda:
- **F11**: Tam ekran toggle
- **ESC**: Kiosk mode'dan çık
