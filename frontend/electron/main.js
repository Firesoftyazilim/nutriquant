/**
 * Nutriquant Electron Main Process
 * Tam ekran kiosk mode uygulaması
 */

const { app, BrowserWindow } = require('electron');
const path = require('path');

// Raspberry Pi GPU hataları için flag'ler
app.commandLine.appendSwitch('disable-gpu');
app.commandLine.appendSwitch('disable-software-rasterizer');
app.commandLine.appendSwitch('disable-gpu-compositing');
app.commandLine.appendSwitch('disable-gpu-sandbox');
app.commandLine.appendSwitch('ignore-gpu-blocklist');
app.commandLine.appendSwitch('enable-features', 'VaapiVideoDecoder');
app.commandLine.appendSwitch('use-gl', 'egl');

// Geliştirme modu kontrolü
const isDev = process.env.NODE_ENV === 'development';

console.log('🔍 Environment check:');
console.log('   NODE_ENV:', process.env.NODE_ENV);
console.log('   isPackaged:', app.isPackaged);
console.log('   isDev:', isDev);

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 480,
    fullscreen: !isDev,         // Tam ekran (sadece production'da)
    kiosk: !isDev,              // Kiosk mode (sadece production'da)
    frame: false,               // Pencere çerçevesi yok
    autoHideMenuBar: true,      // Menu bar gizli
    backgroundColor: '#1a1a2e', // Arka plan rengi
    resizable: isDev,           // Sadece dev modda resize edilebilir
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: true,
      webSecurity: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  // URL yükle
  if (isDev) {
    // Geliştirme: Vite dev server
    console.log('🔧 Development mode: Loading from Vite dev server');
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools(); // DevTools aç
  } else {
    // Production: Build edilmiş dosyalar
    const indexPath = path.join(__dirname, '../dist/index.html');
    console.log('🚀 Production mode: Loading from', indexPath);
    mainWindow.loadFile(indexPath).catch(err => {
      console.error('❌ Failed to load index.html:', err);
    });
  }

  // Web içeriği yüklendiğinde
  mainWindow.webContents.on('did-finish-load', () => {
    console.log('✅ Page loaded successfully');
  });

  // Yükleme hatası
  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
    console.error('❌ Page failed to load:', errorCode, errorDescription);
  });

  // Console mesajlarını yakala (detaylı)
  mainWindow.webContents.on('console-message', (event, level, message, line, sourceId) => {
    const levels = ['', 'INFO', 'WARNING', 'ERROR'];
    console.log(`[Renderer ${levels[level] || 'LOG'}] ${message} (${sourceId}:${line})`);
  });

  // Renderer process hataları
  mainWindow.webContents.on('render-process-gone', (event, details) => {
    console.error('❌ Renderer process crashed:', details);
  });

  // Unresponsive uyarısı
  mainWindow.on('unresponsive', () => {
    console.warn('⚠️ Window became unresponsive');
  });

  // Pencere kapatıldığında
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Tam ekran kısayolları (geliştirme için)
  if (isDev) {
    mainWindow.webContents.on('before-input-event', (event, input) => {
      // F11: Tam ekran toggle
      if (input.key === 'F11' && input.type === 'keyDown') {
        mainWindow.setFullScreen(!mainWindow.isFullScreen());
      }
      // ESC: Kiosk mode'dan çık (sadece dev)
      if (input.key === 'Escape' && input.type === 'keyDown') {
        mainWindow.setKiosk(false);
        mainWindow.setFullScreen(false);
      }
    });
  }
}

// Uygulama hazır olduğunda
app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Tüm pencereler kapatıldığında
app.on('window-all-closed', () => {
  // macOS dışında uygulamayı kapat
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Uygulama kapanırken
app.on('will-quit', () => {
  console.log('Nutriquant kapatılıyor...');
});
