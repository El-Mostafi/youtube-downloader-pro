# Advanced Desktop Shortcut Creator with Custom Icon
$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [System.Environment]::GetFolderPath('Desktop')
$ShortcutPath = Join-Path $Desktop "YouTube Downloader Pro.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

# Set shortcut properties
$AppPath = $PSScriptRoot
$Shortcut.TargetPath = "C:\Python312\pythonw.exe"
$Shortcut.Arguments = "`"$AppPath\app.py`""
$Shortcut.WorkingDirectory = $AppPath
$Shortcut.Description = "YouTube Video & Audio Downloader - Download videos and audio from YouTube with quality selection"
$Shortcut.WindowStyle = 1  # Normal window

# Try to use a custom icon if available, otherwise use Python icon
$IconPath = Join-Path $AppPath "icon.ico"
if (Test-Path $IconPath) {
    $Shortcut.IconLocation = $IconPath
} else {
    # Use Python icon as fallback
    $Shortcut.IconLocation = "C:\Python312\pythonw.exe,0"
}

# Save the shortcut
$Shortcut.Save()

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "✓ Desktop Shortcut Created!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Shortcut Name: YouTube Downloader Pro" -ForegroundColor Cyan
Write-Host "Location: $Desktop" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now double-click the shortcut on your desktop to launch the app!" -ForegroundColor Yellow
Write-Host ""

# Optionally pin to taskbar (requires manual confirmation)
Write-Host "Tip: Right-click the desktop shortcut and select Pin to taskbar for even faster access!" -ForegroundColor Magenta
