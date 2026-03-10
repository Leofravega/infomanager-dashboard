#!/usr/bin/env powershell

Write-Host "`n========================================`n" -ForegroundColor Cyan
Write-Host "   BARBY INFOMANAGER - Dashboard KPI" -ForegroundColor Cyan
Write-Host "`n========================================`n" -ForegroundColor Cyan

# Verificar Python
try {
    $pythonVersion = python --version 2>$null
    Write-Host "[✓] Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Descarga Python desde https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Crear carpeta uploads
if (-not (Test-Path "uploads")) {
    New-Item -ItemType Directory -Name "uploads" | Out-Null
    Write-Host "[✓] Carpeta uploads creada" -ForegroundColor Green
}

# Verificar dependencias
Write-Host "`n[*] Verificando dependencias..." -ForegroundColor Yellow

$dashInstalled = python -c "import dash" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[*] Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt | Out-Null
    Write-Host "[✓] Dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "[✓] Dependencias ya instaladas" -ForegroundColor Green
}

# Obtener IP local
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "*Ethernet*","*WiFi*" | Where-Object {$_.IPAddress -notmatch "127.0.0.1"} | Select-Object -First 1 -ExpandProperty IPAddress)

Write-Host "`n[*] Iniciando Barby InfoManager..." -ForegroundColor Yellow
Write-Host "`n========================================`n" -ForegroundColor Cyan

Write-Host "   🚀 Dashboard iniciado" -ForegroundColor Green
Write-Host "   📍 Local:  http://localhost:8050" -ForegroundColor Cyan
if ($ipAddress) {
    Write-Host "   📍 Red:    http://$($ipAddress):8050" -ForegroundColor Cyan
}
Write-Host "   🔐 Admin:  contraseña: admin123" -ForegroundColor Yellow
Write-Host "`n========================================`n" -ForegroundColor Cyan

# Iniciar la app
python src/app.py

Write-Host "`n[!] Dashboard finalizado" -ForegroundColor Yellow
