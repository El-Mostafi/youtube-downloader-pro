@echo off
REM YouTube Downloader Pro - One-Click Setup and Launch
title YouTube Downloader Pro - Setup

echo.
echo ========================================
echo   YouTube Downloader Pro
echo   Quick Setup and Launch
echo ========================================
echo.

REM Run the PowerShell setup script
powershell.exe -ExecutionPolicy Bypass -File "%~dp0setup_and_run.ps1"

pause
