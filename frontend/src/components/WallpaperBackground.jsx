import { useAppStore } from '../store/appStore';

// Wallpaper mapping
const wallpaperFiles = {
  coffe: 'coffe800x480.jpg',
  iridescent: 'iridescent_liquid 800x480.jpg',
  clover: 'lucky_clover800x480.jpg',
  mountain: 'mountain-800x480.jpg',
  winter: 'scenic_winter 800x480.jpg',
  tunnel: 'tree_tunnel800x480.jpg',
  default: null, // Gradient
};

export default function WallpaperBackground({ children, gradient = 'from-blue-500 via-green-500 to-yellow-400' }) {
  const { currentWallpaper } = useAppStore();
  const wallpaperFile = wallpaperFiles[currentWallpaper];

  return (
    <div className="relative h-screen w-screen overflow-hidden">
      {/* Background Layer */}
      {wallpaperFile ? (
        <>
          {/* Wallpaper Image */}
          <div
            className="absolute inset-0 bg-cover bg-center bg-no-repeat"
            style={{
              backgroundImage: `url(/Wallpapers/${wallpaperFile})`,
            }}
          />
          {/* Dark Overlay for better readability */}
          <div className="absolute inset-0 bg-black/20" />
        </>
      ) : (
        /* Default Gradient */
        <div className={`absolute inset-0 bg-gradient-to-br ${gradient}`} />
      )}

      {/* Content Layer */}
      <div className="relative z-10 h-full w-full">
        {children}
      </div>
    </div>
  );
}
