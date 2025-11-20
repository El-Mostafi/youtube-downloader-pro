# YouTube Video Downloader

A modern, professional desktop application for downloading YouTube videos with quality selection. Built with Python using CustomTkinter for a sleek, dark-themed UI and yt-dlp for reliable video downloading.

## Features

- 🎨 **Modern UI**: Dark-themed, professional interface using CustomTkinter
- 🎬 **Quality Selection**: Fetch and choose from all available video qualities
- 📋 **Playlist Support**: Download entire playlists or select specific videos
- 📊 **Progress Tracking**: Real-time download progress with speed and ETA
- 📁 **Custom Download Location**: Choose where to save your videos
- 📝 **Video Information**: Display video title and format details
- ⚡ **Fast & Reliable**: Uses yt-dlp, the most reliable YouTube downloader
- 🔊 **Smart Format Selection**: Works with or without ffmpeg
- 🎥 **High Quality**: FFmpeg support for best quality video+audio merging
- ✅ **Batch Downloads**: Download multiple videos with quality presets

## Screenshots

The application features:
- Clean URL input field
- One-click format fetching
- Radio button quality selection with file size info
- Custom download path selection
- Real-time progress bar with download statistics
- Success notifications with file path

## Prerequisites

- Python 3.12 or higher
- Windows/macOS/Linux

## Installation

1. **Clone or navigate to the project directory**
   ```powershell
   cd d:\Documents\DownloadYTVideosByPy
   ```

2. **Install required packages**
   ```powershell
   C:/Python312/python.exe -m pip install -r requirements.txt
   ```

3. **Install FFmpeg (Recommended for best quality)**
   
   **Option A - Easy Install (Recommended):**
   ```powershell
   .\install_ffmpeg.ps1
   ```
   
   **Option B - Manual Install:**
   ```powershell
   winget install --id=Gyan.FFmpeg -e
   ```
   
   After installation, restart your terminal for changes to take effect.
   
   > **Note:** FFmpeg enables merging high-quality video and audio streams and fixes video playback issues. Without it, only pre-combined formats will be available.

## Usage

1. **Run the application**
   ```powershell
   C:/Python312/python.exe app.py
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
