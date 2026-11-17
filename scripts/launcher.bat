@echo off
title USB AI System
SET USB_ROOT=%~dp0..
SET PYTHON=%USB_ROOT%\runtime\python\python.exe
SET APP=%USB_ROOT%\app\main.py

echo.
echo  ==========================================
echo   USB AI System v1.0.0
echo   Portable AI Assistant - Offline Ready
echo  ==========================================
echo.

:: Cek apakah runtime Python portable ada
IF NOT EXIST "%PYTHON%" (
    echo [!] Runtime portable tidak ditemukan.
    echo [!] Jalankan scripts\setup.bat terlebih dahulu.
    echo.
    pause
    exit /b 1
)

:: Jalankan aplikasi dengan argumen yang diteruskan
"%PYTHON%" "%APP%" %*

echo.
pause
