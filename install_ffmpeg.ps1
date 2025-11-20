# FFmpeg Installation Script for Windows
# This script will help you install FFmpeg which improves video download quality

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   FFmpeg Installation Helper" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "FFmpeg is recommended for:" -ForegroundColor Yellow
Write-Host "  - Better video quality" -ForegroundColor White
Write-Host "  - Fixing video/audio sync issues" -ForegroundColor White
Write-Host "  - Merging video and audio streams" -ForegroundColor White
Write-Host ""

# Check if ffmpeg is already installed
$ffmpegExists = Get-Command ffmpeg -ErrorAction SilentlyContinue

if ($ffmpegExists) {
    Write-Host "✓ FFmpeg is already installed!" -ForegroundColor Green
    Write-Host "  Location: $($ffmpegExists.Source)" -ForegroundColor Gray
    Write-Host "  Version: " -ForegroundColor Gray -NoNewline
    & ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Host ""
    Write-Host "You're all set! The app will use ffmpeg automatically." -ForegroundColor Green
    exit 0
}

Write-Host "FFmpeg is not installed." -ForegroundColor Yellow
Write-Host ""
Write-Host "Installation Options:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Install via Winget (Recommended - Easy & Automatic)" -ForegroundColor White
Write-Host "2. Install via Chocolatey" -ForegroundColor White
Write-Host "3. Manual Download Instructions" -ForegroundColor White
Write-Host "4. Skip (App will work but with limited quality options)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Installing FFmpeg via Winget..." -ForegroundColor Cyan
        
        # Check if winget is available
        $wingetExists = Get-Command winget -ErrorAction SilentlyContinue
        
        if ($wingetExists) {
            Write-Host "Running: winget install --id=Gyan.FFmpeg -e" -ForegroundColor Gray
            winget install --id=Gyan.FFmpeg -e
            
            Write-Host ""
            Write-Host "✓ Installation complete!" -ForegroundColor Green
            Write-Host "⚠ Please restart your terminal/app for changes to take effect." -ForegroundColor Yellow
        } else {
            Write-Host "✗ Winget is not available on your system." -ForegroundColor Red
            Write-Host "Please use option 2 or 3." -ForegroundColor Yellow
        }
    }
    
    "2" {
        Write-Host ""
        Write-Host "Installing FFmpeg via Chocolatey..." -ForegroundColor Cyan
        
        # Check if chocolatey is available
        $chocoExists = Get-Command choco -ErrorAction SilentlyContinue
        
        if ($chocoExists) {
            Write-Host "Running: choco install ffmpeg" -ForegroundColor Gray
            choco install ffmpeg -y
            
            Write-Host ""
            Write-Host "✓ Installation complete!" -ForegroundColor Green
            Write-Host "⚠ Please restart your terminal/app for changes to take effect." -ForegroundColor Yellow
        } else {
            Write-Host "✗ Chocolatey is not installed." -ForegroundColor Red
            Write-Host "Install Chocolatey from: https://chocolatey.org/install" -ForegroundColor Yellow
        }
    }
    
    "3" {
        Write-Host ""
        Write-Host "Manual Installation Instructions:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "1. Download FFmpeg from: https://github.com/BtbN/FFmpeg-Builds/releases" -ForegroundColor White
        Write-Host "   - Download: ffmpeg-master-latest-win64-gpl.zip" -ForegroundColor Gray
        Write-Host ""
        Write-Host "2. Extract the ZIP file to a folder (e.g., C:\ffmpeg)" -ForegroundColor White
        Write-Host ""
        Write-Host "3. Add FFmpeg to PATH:" -ForegroundColor White
        Write-Host "   - Open System Properties > Environment Variables" -ForegroundColor Gray
        Write-Host "   - Edit the 'Path' variable" -ForegroundColor Gray
        Write-Host "   - Add: C:\ffmpeg\bin" -ForegroundColor Gray
        Write-Host ""
        Write-Host "4. Restart your terminal and app" -ForegroundColor White
        Write-Host ""
        Write-Host "Opening download page in browser..." -ForegroundColor Cyan
        Start-Process "https://github.com/BtbN/FFmpeg-Builds/releases"
    }
    
    "4" {
        Write-Host ""
        Write-Host "Skipping FFmpeg installation." -ForegroundColor Yellow
        Write-Host "The app will work but some videos may have quality limitations." -ForegroundColor Gray
    }
    
    default {
        Write-Host ""
        Write-Host "Invalid choice. Exiting." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
