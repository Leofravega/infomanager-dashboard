@echo off
REM Barby InfoManager - Script de inicio rápido para Windows

echo.
echo ========================================
echo   BARBY INFOMANAGER - Dashboard KPI
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo Descarga Python desde https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [✓] Python encontrado
echo.

REM Crear carpeta uploads si no existe
if not exist "uploads" (
    mkdir uploads
    echo [✓] Carpeta uploads creada
)

echo.
echo [*] Verificando dependencias...
pip show dash >nul 2>&1
if errorlevel 1 (
    echo [*] Instalando dependencias...
    pip install -r requirements.txt
    echo [✓] Dependencias instaladas
) else (
    echo [✓] Dependencias ya instaladas
)

echo.
echo [*] Iniciando Barby InfoManager...
echo.
timeout /t 2

REM Iniciar la app
python src/app.py

echo.
echo [!] Dashboard finalizado
pause
