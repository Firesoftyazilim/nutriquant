#!/bin/bash

# ============================================
# Node.js ve npm Kurulum Scripti
# Raspberry Pi / Ubuntu / Debian
# ============================================

echo "============================================"
echo "📦 Node.js Kurulumu"
echo "============================================"

# Sistem güncellemesi
echo "⚙️  Sistem güncelleniyor..."
sudo apt update

# Node.js 18.x kurulumu (LTS)
echo "📥 Node.js 18.x repository ekleniyor..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

echo "📦 Node.js ve npm kuruluyor..."
sudo apt install -y nodejs

# Kurulum kontrolü
echo ""
echo "============================================"
echo "✅ Kurulum Tamamlandı!"
echo "============================================"
echo "Node.js versiyonu: $(node --version)"
echo "npm versiyonu: $(npm --version)"
echo ""
echo "🚀 Şimdi şunu çalıştırabilirsiniz:"
echo "   ./start.sh"
echo "============================================"
