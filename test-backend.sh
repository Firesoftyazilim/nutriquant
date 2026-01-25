#!/bin/bash

# Backend API Test Scripti

echo "🧪 Backend API Testi"
echo "===================="

API_URL="http://localhost:8000"

# Health check
echo ""
echo "1️⃣  Health Check..."
curl -s $API_URL/api/health | python3 -m json.tool

# Weight
echo ""
echo "2️⃣  Ağırlık Okuma..."
curl -s $API_URL/api/scale/weight | python3 -m json.tool

# Battery
echo ""
echo "3️⃣  Batarya Durumu..."
curl -s $API_URL/api/battery | python3 -m json.tool

# Profiles
echo ""
echo "4️⃣  Profiller..."
curl -s $API_URL/api/profiles | python3 -m json.tool

echo ""
echo "✅ Test tamamlandı!"
echo ""
echo "📚 API Dokümantasyonu: http://localhost:8000/docs"
