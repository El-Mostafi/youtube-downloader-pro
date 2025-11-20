# Create Desktop Shortcut for YouTube Downloader
$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [System.Environment]::GetFolderPath('Desktop')
$ShortcutPath = Join-Path $Desktop "YouTube Downloader.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

# Set shortcut properties
$Shortcut.TargetPath = "C:\Python312\pythonw.exe"
$Shortcut.Arguments = "app.py"
$Shortcut.WorkingDirectory = "$PSScriptRoot"
$Shortcut.Description = "YouTube Video & Audio Downloader"
$Shortcut.IconLocation = "C:\Python312\pythonw.exe,0"

# Save the shortcut
$Shortcut.Save()

Write-Host "Desktop shortcut created successfully!" -ForegroundColor Green
Write-Host "Location: $ShortcutPath" -ForegroundColor Cyan
