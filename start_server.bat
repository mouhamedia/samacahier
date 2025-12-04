@echo off
REM Script pour demarrer le serveur Django de maniere stable

cd /d "%~dp0"

echo.
echo ========================================
echo Demarrage du serveur SamaCahier
echo ========================================
echo.

python manage.py runserver --noreload 8000

pause
