@echo off
:: Hızlı Github Yükleme Scripti (Windows)
:: Kullanım: push.bat "commit mesajınız"

if "%~1"=="" (
    echo Hata: Lutfen bir commit mesaji girin.
    echo Ornek: push.bat "yeni ozellik eklendi"
    exit /b 1
)

echo ===================================
echo Github'a yukleniyor...
echo Mesaj: %~1
echo ===================================

:: Git komutları
git add .
git commit -m "%~1"
git push origin main

if %ERRORLEVEL% equ 0 (
    echo ===================================
    echo BASARILI! Degisiklikler yuklendi.
    echo ===================================
) else (
    echo ===================================
    echo HATA! Yukleme basarisiz oldu.
    echo ===================================
)
