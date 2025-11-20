Write-Host "Testing YouTube Downloader with FFmpeg..." -ForegroundColor Cyan
Write-Host ""

# Refresh PATH to include ffmpeg
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Check ffmpeg
Write-Host "Checking FFmpeg..." -ForegroundColor Yellow
$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
if ($ffmpeg) {
    Write-Host "✓ FFmpeg found: $($ffmpeg.Source)" -ForegroundColor Green
} else {
    Write-Host "✗ FFmpeg not found in PATH" -ForegroundColor Red
    Write-Host "Please restart your terminal and try again." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Starting the YouTube Downloader app..." -ForegroundColor Cyan
Write-Host "The app will now use FFmpeg for best quality!" -ForegroundColor Green
Write-Host ""

# Start the app with updated environment
C:/Python312/python.exe app.py
