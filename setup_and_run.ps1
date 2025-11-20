# YouTube Downloader Pro - Automated Setup and Launch
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  YouTube Downloader Pro - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if a command exists
function Test-Command {
    param($Command)
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            return $true
        }
    } catch {
        return $false
    }
}

# Step 1: Check Python installation
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
if (Test-Command "python") {
    $pythonVersion = python --version 2>&1
    Write-Host "  OK Python found: $pythonVersion" -ForegroundColor Green
    $pythonCmd = "python"
} elseif (Test-Path "C:\Python312\python.exe") {
    Write-Host "  OK Python found at C:\Python312\python.exe" -ForegroundColor Green
    $pythonCmd = "C:\Python312\python.exe"
} else {
    Write-Host "  ERROR Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.8 or higher from:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host ""
    pause
    exit 1
}

# Step 2: Install packages
Write-Host ""
Write-Host "[2/5] Checking Python packages..." -ForegroundColor Yellow
if (-not (Test-Path "requirements.txt")) {
    Write-Host "  Creating requirements.txt..." -ForegroundColor Yellow
    @"
customtkinter==5.2.1
yt-dlp>=2025.11.12
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8
}

Write-Host "  Installing packages..." -ForegroundColor Cyan
& $pythonCmd -m pip install --upgrade pip --quiet
& $pythonCmd -m pip install -r requirements.txt --upgrade --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK All packages installed" -ForegroundColor Green
} else {
    Write-Host "  ERROR Failed to install packages" -ForegroundColor Red
    pause
    exit 1
}

# Step 3: Check FFmpeg
Write-Host ""
Write-Host "[3/5] Checking FFmpeg..." -ForegroundColor Yellow
if (Test-Command "ffmpeg") {
    Write-Host "  OK FFmpeg is installed" -ForegroundColor Green
} else {
    Write-Host "  WARNING FFmpeg not found" -ForegroundColor Yellow
    Write-Host "  The app will work but with limited features" -ForegroundColor Gray
}

# Step 4: Check app files
Write-Host ""
Write-Host "[4/5] Checking application files..." -ForegroundColor Yellow
if (Test-Path "app.py") {
    Write-Host "  OK Application files found" -ForegroundColor Green
} else {
    Write-Host "  ERROR app.py not found!" -ForegroundColor Red
    pause
    exit 1
}

# Step 5: Create shortcut
Write-Host ""
Write-Host "[5/5] Desktop shortcut..." -ForegroundColor Yellow
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop "YouTube Downloader.lnk"

if (-not (Test-Path $ShortcutPath)) {
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = "C:\Python312\pythonw.exe"
    $Shortcut.Arguments = "app.py"
    $Shortcut.WorkingDirectory = $PSScriptRoot
    $Shortcut.Description = "YouTube Downloader"
    $Shortcut.Save()
    Write-Host "  OK Desktop shortcut created" -ForegroundColor Green
} else {
    Write-Host "  OK Desktop shortcut exists" -ForegroundColor Green
}

# Done
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Launching app..." -ForegroundColor Cyan
Write-Host ""

Start-Sleep -Seconds 1

# Launch
& $pythonCmd app.py
