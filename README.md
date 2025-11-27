# YouTube Downloader Pro 🎥

[![GitHub release](https://img.shields.io/github/v/release/El-Mostafi/youtube-downloader-pro)](https://github.com/El-Mostafi/youtube-downloader-pro/releases)
[![Downloads](https://img.shields.io/github/downloads/El-Mostafi/youtube-downloader-pro/total)](https://github.com/El-Mostafi/youtube-downloader-pro/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A modern, professional desktop application for downloading YouTube videos and audio with quality selection. Built with Python using CustomTkinter for a sleek, dark-themed UI and yt-dlp for reliable downloading.

## 📥 Download

Get YouTube Downloader Pro from multiple sources:

### GitHub Releases (Primary)

**Latest Release:** [Download v1.0.0](https://github.com/El-Mostafi/youtube-downloader-pro/releases/latest)

Choose your preferred format:

- **Source Code** - Lightweight, auto-setup (~14KB)
- **Portable Executable** - No Python needed, ready to use (~34MB)

### SourceForge (Alternative)

[![Download YouTube Downloader Pro](https://img.shields.io/sourceforge/dt/youtube-downloader-pro.svg)](https://sourceforge.net/projects/youtube-downloader-pro/files/latest/download)

**Direct Download:** [SourceForge Downloads](https://sourceforge.net/projects/youtube-downloader-pro/)

Benefits:

- 🌍 Global CDN for faster downloads
- 📊 Download statistics and rankings
- 🔄 Mirror downloads for reliability

## ⚡ Quick Start (For New Users)

**Just cloned this repository? Get started in ONE click:**

### Windows:

1. Double-click `QUICK_START.bat`
2. Wait for automatic setup (installs dependencies, checks FFmpeg)
3. App launches automatically!

### Alternative (PowerShell):

```powershell
.\setup_and_run.ps1
```

That's it! The script handles everything:

- ✅ Checks Python installation
- ✅ Installs required packages
- ✅ Installs FFmpeg if needed
- ✅ Creates desktop shortcut
- ✅ Launches the app

## Features

- 🎨 **Modern UI**: Dark-themed, professional interface using CustomTkinter
- 🎬 **Video Download**: Fetch and choose from all available video qualities (144p-4K)
- 🎵 **Audio Download**: Extract audio as MP3 with quality selection
- 📋 **Playlist Support**: Download entire playlists or select specific videos/audio
- 📊 **Progress Tracking**: Real-time download progress with speed and ETA
- 📁 **Custom Download Location**: Choose where to save your files
- 📝 **Detailed Information**: Display video title, format, codec, and file size
- ⚡ **Fast & Reliable**: Uses yt-dlp, the most reliable YouTube downloader
- 🔊 **Universal Audio**: Automatic AAC/MP3 conversion for all devices
- 🎥 **High Quality**: FFmpeg support for best quality video+audio merging
- ✅ **Batch Downloads**: Download multiple videos/audio with quality presets

## Screenshots

The application features:

- Clean URL input field with playlist detection
- Video/Audio type selector
- One-click format fetching
- Radio button quality selection with file size and codec info
- Custom download path selection
- Real-time progress bar with download statistics
- Desktop shortcut for easy access

## Prerequisites

- **Python 3.8+** (Python 3.12 recommended)
- **Windows 10/11** (primary support), macOS/Linux compatible
- **Internet connection**

## 📦 Installation Options

### Option 1: One-Click Setup (Recommended)

```powershell
# Just run this - it does everything!
.\QUICK_START.bat
```

### Option 2: Manual Setup

1. **Clone the repository**

   ```powershell
   git clone https://github.com/El-Mostafi/youtube-downloader-pro.git
   cd youtube-downloader-pro
   ```

2. **Install Python packages**

   ```powershell
   pip install -r requirements.txt
   ```

3. **Install FFmpeg** (Required for video+audio merging and MP3 conversion)

   ```powershell
   winget install --id=Gyan.FFmpeg -e
   ```

4. **Run the app**
   ```powershell
   python app.py
   ```

## 🚀 Usage

### For First-Time Users:

1. Run `QUICK_START.bat` - everything is automated!
2. A desktop shortcut will be created
3. Next time, just double-click the desktop icon

### Manual Launch:

```powershell
python app.py
```

2. **Download a single video**:

   - Paste a YouTube video URL in the input field
   - Click "Fetch Available Qualities" to retrieve available formats
   - Select your preferred quality from the list
   - (Optional) Change the download location using the "Browse" button
   - Click "Download Video" to start the download
   - Wait for the download to complete - you'll see real-time progress
   - A success message will show the file location when done

3. **Download a playlist** ([See detailed guide](PLAYLIST_FEATURE.md)):
   - Paste a YouTube playlist URL
   - Click "Fetch Available Qualities"
   - The app detects the playlist and shows all videos
   - Choose a quality preset (Best, 1080p, 720p, 480p, 360p)
   - Select which videos to download (or keep "Select All" checked)
   - Click "Download Selected Videos"
   - Confirm the download
   - Watch progress as each video downloads
   - Get a summary report when complete

## Dependencies

- **customtkinter**: Modern UI framework for Python
- **yt-dlp**: YouTube video downloader (maintained fork of youtube-dl)

## Features Explained

### Quality Selection

The app automatically fetches all available video qualities including:

- Resolution (144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 2160p/4K, etc.)
- File format (MP4, WEBM, etc.)
- Frame rate (30fps, 60fps, etc.)
- Estimated file size
- Audio indicator (🔊) showing formats with built-in audio

### Download Process

- Multiple format options available: MP4 (H.264), WEBM (VP9), with or without audio
- Formats with 🔊 include audio and are ready to play immediately
- Video-only formats are automatically merged with audio using ffmpeg
- **Audio compatibility**: All audio is automatically converted to AAC codec for universal playback
- **Video optimization**: Video codecs are copied (no re-encoding for fast processing)
- **Detailed progress tracking** showing:
  - Real-time percentage and progress bar
  - Downloaded size / Total size (e.g., 75MB / 167MB)
  - Current download speed (e.g., 1.2MB/s)
  - Estimated time remaining (ETA)
- Downloaded files use the original video title as the filename

## Troubleshooting

### Module Not Found Error

If you get a "No module named 'customtkinter'" or similar error:

```powershell
C:/Python312/python.exe -m pip install --upgrade pip
C:/Python312/python.exe -m pip install -r requirements.txt
```

### Video Download Fails

- Ensure you have a stable internet connection
- Check that the URL is a valid YouTube video link
- Some videos may be age-restricted or geographically limited
- Try updating yt-dlp: `C:/Python312/python.exe -m pip install --upgrade yt-dlp`

### Application Won't Start

- Verify Python 3.12 is installed: `C:/Python312/python.exe --version`
- Check that all dependencies are installed properly
- Try running with: `C:/Python312/python.exe -u app.py` for verbose output

## Technical Details

- **Threading**: Downloads run in separate threads to keep the UI responsive
- **Error Handling**: Comprehensive error catching and user-friendly messages
- **Progress Hooks**: Real-time progress updates from yt-dlp
- **Format Selection**: Automatically selects best quality video + audio combination

## License

This project is for educational purposes. Please respect YouTube's Terms of Service and copyright laws when downloading content.

## Notes

- Always ensure you have the right to download and use the content
- Download speeds depend on your internet connection
- Larger files (4K, high bitrate) will take longer to download
- The application requires an active internet connection to function

## Support

For issues or questions:

1. Check the Troubleshooting section above
2. Ensure all dependencies are up to date
3. Verify your Python version is compatible

---

**Enjoy downloading videos with a professional, modern interface!**
