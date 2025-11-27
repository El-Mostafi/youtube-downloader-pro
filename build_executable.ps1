# Build Standalone Executable
# This script creates a Windows executable using PyInstaller

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Building Executable" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if PyInstaller is installed
Write-Host "[1/4] Checking PyInstaller..." -ForegroundColor Yellow
$checkResult = & python -m pip show pyinstaller 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Installing PyInstaller..." -ForegroundColor Yellow
    python -m pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ERROR Could not install PyInstaller" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "  OK PyInstaller installed" -ForegroundColor Green
} else {
    Write-Host "  OK PyInstaller found" -ForegroundColor Green
}

# Clean previous builds
Write-Host ""
Write-Host "[2/4] Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "*.spec") { Remove-Item -Force "*.spec" }
Write-Host "  OK Cleaned" -ForegroundColor Green

# Build executable
Write-Host ""
Write-Host "[3/4] Building executable..." -ForegroundColor Yellow
Write-Host "  This may take 2-3 minutes..." -ForegroundColor Gray

$buildArgs = @(
    "--onefile",
    "--windowed",
    "--name=YouTubeDownloaderPro",
    "--add-data=requirements.txt;.",
    "app.py"
)

python -m PyInstaller @buildArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK Build successful!" -ForegroundColor Green
} else {
    Write-Host "  ERROR Build failed" -ForegroundColor Red
    exit 1
}

# Create distribution package
Write-Host ""
Write-Host "[4/4] Creating distribution package..." -ForegroundColor Yellow

$version = "1.0.0"
$distFolder = "youtube-downloader-pro-v$version"

# Create distribution folder
if (Test-Path $distFolder) { Remove-Item -Recurse -Force $distFolder }
New-Item -ItemType Directory -Path $distFolder | Out-Null

# Copy files
Copy-Item "dist\YouTubeDownloaderPro.exe" $distFolder
Copy-Item "README.md" $distFolder
Copy-Item "*.md" $distFolder -Exclude "README.md"

# Create README for executable
@"
# YouTube Downloader Pro - Portable Edition

## Quick Start

1. Double-click `YouTubeDownloaderPro.exe`
2. That's it! The app will launch immediately.

## System Requirements

- Windows 10/11 (64-bit)
- Internet connection
- FFmpeg (optional, for best quality)

## Installing FFmpeg (Optional but Recommended)

Open PowerShell as Administrator and run:
``````
winget install --id=Gyan.FFmpeg -e
``````

## Features

- Download YouTube videos in multiple qualities
- Extract audio as MP3
- Download entire playlists
- Real-time progress tracking
- Modern dark UI

## Notes

- First launch may take 10-15 seconds (unpacking)
- Antivirus may show a warning (false positive - the app is safe)
- File size: ~80-100MB (includes Python runtime)

## Source Code

https://github.com/El-Mostafi/youtube-downloader-pro

---

Enjoy downloading! 🎥
"@ | Out-File -FilePath "$distFolder\README_PORTABLE.txt" -Encoding UTF8

# Create ZIP
Write-Host "  Creating ZIP archive..." -ForegroundColor Cyan
$zipName = "$distFolder-portable.zip"
if (Test-Path $zipName) { Remove-Item -Force $zipName }
Compress-Archive -Path $distFolder -DestinationPath $zipName

Write-Host "  OK Distribution package created" -ForegroundColor Green

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Build Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Files created:" -ForegroundColor Cyan
Write-Host "  - dist\YouTubeDownloaderPro.exe" -ForegroundColor White
Write-Host "  - $zipName" -ForegroundColor White
Write-Host ""
Write-Host "File size:" -ForegroundColor Cyan
$exeSize = (Get-Item "dist\YouTubeDownloaderPro.exe").Length / 1MB
Write-Host "  - Executable: $([math]::Round($exeSize, 2)) MB" -ForegroundColor White
Write-Host ""
Write-Host "Upload to GitHub Releases:" -ForegroundColor Yellow
Write-Host "  1. Go to: https://github.com/El-Mostafi/youtube-downloader-pro/releases" -ForegroundColor Gray
Write-Host "  2. Click 'Draft a new release'" -ForegroundColor Gray
Write-Host "  3. Upload $zipName" -ForegroundColor Gray
Write-Host ""
