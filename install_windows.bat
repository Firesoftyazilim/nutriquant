@echo off
echo ============================================
echo Nutriquant - Windows Simulasyon Kurulumu
echo ============================================
echo.

echo Gerekli Python paketleri kuruluyor...
echo.

python -m pip install --upgrade pip
python -m pip install numpy pillow

echo.
echo ============================================
echo Kurulum tamamlandi!
echo.
echo Calistirmak icin:
echo   python main_console.py
echo ============================================
pause
