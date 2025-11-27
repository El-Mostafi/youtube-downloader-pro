# Create GitHub Release Package
# This creates a ZIP file ready for GitHub Releases

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Creating Release Package" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$version = "1.0.0"
$releaseName = "youtube-downloader-pro-v$version"
$releaseFolder = "release_package"

# Create release folder
Write-Host "[1/3] Preparing files..." -ForegroundColor Yellow
if (Test-Path $releaseFolder) { Remove-Item -Recurse -Force $releaseFolder }
New-Item -ItemType Directory -Path $releaseFolder | Out-Null
New-Item -ItemType Directory -Path "$releaseFolder\$releaseName" | Out-Null

# Copy essential files
$files = @(
    "app.py",
    "requirements.txt",
    "QUICK_START.bat",
    "setup_and_run.ps1",
    "create_shortcut.ps1",
    "README.md",
    "AUDIO_FEATURE.md",
    "PLAYLIST_FEATURE.md",
    ".gitignore"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Copy-Item $file "$releaseFolder\$releaseName\"
    }
}

Write-Host "  OK Files copied" -ForegroundColor Green

# Create installation guide
Write-Host ""
Write-Host "[2/3] Creating INSTALL.txt..." -ForegroundColor Yellow
@"
========================================
  YouTube Downloader Pro v$version
========================================

QUICK INSTALLATION (5 seconds):
-------------------------------
1. Extract this ZIP file
2. Double-click "QUICK_START.bat"
3. Done! The app will auto-setup and launch

WHAT IT DOES:
-------------
✓ Checks Python installation
✓ Installs required packages
✓ Creates desktop shortcut
✓ Launches the application

REQUIREMENTS:
-------------
- Windows 10/11
- Python 3.8+ (will prompt to install if missing)
- Internet connection

FEATURES:
---------
✓ Download YouTube videos (144p-4K)
✓ Extract audio as MP3
✓ Download playlists
✓ Multiple quality options
✓ Real-time progress tracking
✓ Modern dark-themed UI

FIRST TIME SETUP:
-----------------
The QUICK_START.bat will:
1. Install Python packages (30 seconds)
2. Check for FFmpeg (optional)
3. Create desktop shortcut
4. Launch the application

SUBSEQUENT USES:
----------------
Just double-click the desktop shortcut!

MANUAL SETUP (if needed):
-------------------------
1. Install Python 3.8+: https://www.python.org/downloads/
2. Open PowerShell in this folder
3. Run: pip install -r requirements.txt
4. Run: python app.py

FFMPEG (OPTIONAL):
------------------
For best quality and audio conversion:
winget install --id=Gyan.FFmpeg -e

TROUBLESHOOTING:
----------------
- If Python not found: Install from python.org
- If packages fail: Run PowerShell as Administrator
- If FFmpeg needed: See README.md

SUPPORT:
--------
GitHub: https://github.com/El-Mostafi/youtube-downloader-pro
Issues: https://github.com/El-Mostafi/youtube-downloader-pro/issues

========================================
Enjoy downloading! 🎥
========================================
"@ | Out-File -FilePath "$releaseFolder\$releaseName\INSTALL.txt" -Encoding UTF8

Write-Host "  OK INSTALL.txt created" -ForegroundColor Green

# Create ZIP
Write-Host ""
Write-Host "[3/3] Creating ZIP archive..." -ForegroundColor Yellow
$zipName = "$releaseName-source.zip"
if (Test-Path $zipName) { Remove-Item -Force $zipName }
Compress-Archive -Path "$releaseFolder\$releaseName\*" -DestinationPath $zipName

Write-Host "  OK ZIP created" -ForegroundColor Green

# Cleanup
Remove-Item -Recurse -Force $releaseFolder

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Release Package Ready!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Created: $zipName" -ForegroundColor Cyan
$zipSize = (Get-Item $zipName).Length / 1KB
Write-Host "Size: $([math]::Round($zipSize, 2)) KB" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Create Git tag:" -ForegroundColor Gray
Write-Host "   git tag -a v$version -m 'Release version $version'" -ForegroundColor White
Write-Host "   git push origin v$version" -ForegroundColor White
Write-Host ""
Write-Host "2. Create GitHub Release:" -ForegroundColor Gray
Write-Host "   - Go to: https://github.com/El-Mostafi/youtube-downloader-pro/releases" -ForegroundColor White
Write-Host "   - Click 'Draft a new release'" -ForegroundColor White
Write-Host "   - Choose tag: v$version" -ForegroundColor White
Write-Host "   - Upload: $zipName" -ForegroundColor White
Write-Host ""
Write-Host "3. Add release notes with features and screenshots" -ForegroundColor Gray
Write-Host ""
