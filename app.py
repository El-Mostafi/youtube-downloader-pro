import customtkinter as ctk
from tkinter import filedialog, messagebox
import yt_dlp
import threading
import os
from pathlib import Path


class YouTubeDownloaderApp:
    def __init__(self):
        # Initialize the main window
        self.root = ctk.CTk()
        self.root.title("YouTube Video Downloader")
        self.root.geometry("850x750")
        
        # Set theme and color
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.download_path = str(Path.home() / "Downloads")
        self.available_formats = []
        self.is_fetching = False
        self.is_playlist = False
        self.playlist_videos = []
        self.current_video_info = None
        self.download_type = "video"  # "video" or "audio"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="YouTube Video Downloader",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 15))
        
        # Top Section (URL + Type + Fetch) - Fixed height
        top_section = ctk.CTkFrame(main_frame)
        top_section.pack(fill="x", pady=(0, 10))
        
        url_label = ctk.CTkLabel(
            top_section,
            text="Video or Playlist URL:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        url_label.pack(anchor="w", padx=10, pady=(10, 3))
        
        self.url_entry = ctk.CTkEntry(
            top_section,
            placeholder_text="Paste YouTube video or playlist URL here...",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.url_entry.pack(fill="x", padx=10, pady=(0, 5))
        
        # Playlist info label
        self.playlist_info_label = ctk.CTkLabel(
            top_section,
            text="",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.playlist_info_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        # Download Type Selection
        type_label = ctk.CTkLabel(
            top_section,
            text="Download Type:",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        type_label.pack(anchor="w", padx=10, pady=(3, 3))
        
        self.type_selector = ctk.CTkSegmentedButton(
            top_section,
            values=["Video", "Audio Only"],
            command=self.on_type_change,
            height=30,
            font=ctk.CTkFont(size=11)
        )
        self.type_selector.set("Video")
        self.type_selector.pack(fill="x", padx=10, pady=(0, 10))
        
        # Fetch Formats Button
        self.fetch_button = ctk.CTkButton(
            top_section,
            text="Fetch Available Qualities",
            command=self.fetch_formats,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.fetch_button.pack(fill="x", padx=10, pady=(0, 10))
        
        # Middle Section (Quality) - Scrollable with fixed height
        quality_frame = ctk.CTkFrame(main_frame)
        quality_frame.pack(fill="x", pady=(0, 10))
        
        quality_label = ctk.CTkLabel(
            quality_frame,
            text="Available Qualities:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        quality_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Scrollable frame for quality options - FIXED HEIGHT
        self.quality_scroll = ctk.CTkScrollableFrame(
            quality_frame,
            height=140
        )
        self.quality_scroll.pack(fill="x", padx=10, pady=(0, 10))
        
        self.quality_var = ctk.StringVar(value="")
        
        # Download Path Section - Compact
        path_frame = ctk.CTkFrame(main_frame)
        path_frame.pack(fill="x", pady=(0, 10))
        
        path_label = ctk.CTkLabel(
            path_frame,
            text="Download Location:",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        path_label.pack(anchor="w", padx=10, pady=(8, 3))
        
        path_input_frame = ctk.CTkFrame(path_frame)
        path_input_frame.pack(fill="x", padx=10, pady=(0, 8))
        
        self.path_entry = ctk.CTkEntry(
            path_input_frame,
            placeholder_text="Download path...",
            height=30,
            font=ctk.CTkFont(size=11)
        )
        self.path_entry.insert(0, self.download_path)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        browse_button = ctk.CTkButton(
            path_input_frame,
            text="Browse",
            command=self.browse_folder,
            width=90,
            height=30,
            font=ctk.CTkFont(size=11)
        )
        browse_button.pack(side="right")
        
        # Bottom Section (Progress + Download Button) - Always visible
        bottom_section = ctk.CTkFrame(main_frame)
        bottom_section.pack(fill="x", side="bottom", pady=(0, 0))
        
        # Progress Section
        self.progress_label = ctk.CTkLabel(
            bottom_section,
            text="",
            font=ctk.CTkFont(size=11)
        )
        self.progress_label.pack(pady=(5, 5))
        
        self.progress_bar = ctk.CTkProgressBar(bottom_section)
        self.progress_bar.pack(fill="x", padx=10, pady=(0, 10))
        self.progress_bar.set(0)
        
        # Download Button
        self.download_button = ctk.CTkButton(
            bottom_section,
            text="⬇ Download Video",
            command=self.start_download,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled",
            corner_radius=10,
            fg_color=("#1f6aa5", "#144870"),
            hover_color=("#144870", "#1f6aa5"),
            border_width=2,
            border_color=("#3b8ed0", "#1f6aa5")
        )
        self.download_button.pack(fill="x", padx=10, pady=(0, 10))
        
        # Initialize playlist-related variables
        self.playlist_quality_var = ctk.StringVar(value="best")
        self.video_checkboxes = []
        self.select_all_var = ctk.BooleanVar(value=True)
        
    def on_type_change(self, value):
        """Handle download type selection change"""
        if value == "Video":
            self.download_type = "video"
        else:
            self.download_type = "audio"
        
        # Clear current formats if any
        if self.available_formats:
            self.available_formats = []
            for widget in self.quality_scroll.winfo_children():
                widget.destroy()
            self.download_button.configure(state="disabled")
            self.progress_label.configure(text="Please fetch formats again for the selected type")
    
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.download_path = folder
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)
    
    def fetch_formats(self):
        if self.is_fetching:
            return
            
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        self.is_fetching = True
        self.is_playlist = False
        self.playlist_videos = []
        self.fetch_button.configure(state="disabled", text="Fetching...")
        self.progress_label.configure(text="Fetching information...")
        self.playlist_info_label.configure(text="")
        
        # Clear previous quality options
        for widget in self.quality_scroll.winfo_children():
            widget.destroy()
        
        thread = threading.Thread(target=self._fetch_formats_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _fetch_formats_thread(self, url):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
                'format': 'all',
                'listformats': False,
                'extract_flat': 'in_playlist'
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Check if it's a playlist
                if 'entries' in info and info.get('_type') == 'playlist':
                    self.is_playlist = True
                    playlist_title = info.get('title', 'Unknown Playlist')
                    playlist_count = len(list(info.get('entries', [])))
                    
                    # Store playlist videos
                    self.playlist_videos = []
                    for entry in info['entries']:
                        if entry:
                            self.playlist_videos.append({
                                'url': entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}",
                                'title': entry.get('title', 'Unknown'),
                                'duration': entry.get('duration', 0),
                                'id': entry.get('id', '')
                            })
                    
                    # Update UI to show playlist
                    self.root.after(0, self._show_playlist, playlist_title, playlist_count)
                    return
                
                # Single video - get formats
                self.is_playlist = False
                self.current_video_info = info
                video_title = info.get('title', 'Unknown')
                
                # Organize formats - collect ALL unique formats
                formats_list = []
                seen_formats = set()
                
                if self.download_type == "audio":
                    # Audio-only formats
                    for fmt in info['formats']:
                        acodec = fmt.get('acodec', 'none')
                        vcodec = fmt.get('vcodec', 'none')
                        
                        # Only include audio-only formats
                        if acodec != 'none' and vcodec == 'none':
                            abr = fmt.get('abr', 0)  # Audio bitrate
                            ext = fmt.get('ext', 'mp3')
                            filesize = fmt.get('filesize', 0)
                            format_id = fmt.get('format_id', '')
                            asr = fmt.get('asr', 0)  # Audio sample rate
                            
                            # Create unique key
                            format_key = (abr, ext, acodec)
                            
                            if format_key not in seen_formats and abr > 0:
                                seen_formats.add(format_key)
                                
                                formats_list.append({
                                    'quality': f"{int(abr)}kbps",
                                    'format_id': format_id,
                                    'ext': ext,
                                    'filesize': filesize,
                                    'abr': abr,
                                    'acodec': acodec,
                                    'asr': asr,
                                    'is_audio': True
                                })
                    
                    # Sort by bitrate (desc)
                    self.available_formats = sorted(
                        formats_list,
                        key=lambda x: x['abr'],
                        reverse=True
                    )
                else:
                    # Video formats
                    for fmt in info['formats']:
                        vcodec = fmt.get('vcodec', 'none')
                        acodec = fmt.get('acodec', 'none')
                        
                        # Only include formats with video
                        if vcodec != 'none':
                            height = fmt.get('height', 0)
                            if height and height >= 144:  # Minimum 144p
                                ext = fmt.get('ext', 'mp4')
                                fps = fmt.get('fps', 30)
                                filesize = fmt.get('filesize', 0)
                                has_audio = acodec != 'none'
                                format_id = fmt.get('format_id', '')
                                
                                # Create unique key to avoid exact duplicates
                                format_key = (height, ext, fps, has_audio)
                                
                                if format_key not in seen_formats:
                                    seen_formats.add(format_key)
                                    quality_label = f"{height}p"
                                    
                                    formats_list.append({
                                        'quality': quality_label,
                                        'format_id': format_id,
                                        'ext': ext,
                                        'fps': fps,
                                        'filesize': filesize,
                                        'height': height,
                                        'has_audio': has_audio,
                                        'vcodec': vcodec,
                                        'acodec': acodec,
                                        'is_audio': False
                                    })
                    
                    # Sort by: resolution (desc), then has_audio (yes first), then filesize (desc)
                    self.available_formats = sorted(
                        formats_list,
                        key=lambda x: (x['height'], x['has_audio'], x['filesize']),
                        reverse=True
                    )
                
                # Update UI in main thread
                self.root.after(0, self._update_quality_options, video_title)
                
        except Exception as e:
            self.root.after(0, self._show_error, f"Error fetching formats: {str(e)}")
    
    def _update_quality_options(self, video_title):
        # Clear previous options
        for widget in self.quality_scroll.winfo_children():
            widget.destroy()
        
        if not self.available_formats:
            label = ctk.CTkLabel(
                self.quality_scroll,
                text="No formats available",
                font=ctk.CTkFont(size=12)
            )
            label.pack(pady=10)
        else:
            # Show title with appropriate icon
            icon = "🎵" if self.download_type == "audio" else "📹"
            title_label = ctk.CTkLabel(
                self.quality_scroll,
                text=f"{icon} {video_title}",
                font=ctk.CTkFont(size=13, weight="bold"),
                wraplength=700
            )
            title_label.pack(anchor="w", pady=(5, 15))
            
            # Add quality options with index for unique selection
            for idx, fmt_info in enumerate(self.available_formats):
                filesize_mb = fmt_info['filesize'] / (1024 * 1024) if fmt_info['filesize'] else 0
                size_text = f" (~{filesize_mb:.1f} MB)" if filesize_mb > 0 else ""
                
                if fmt_info.get('is_audio', False):
                    # Audio format display
                    quality_text = fmt_info['quality']
                    codec_info = fmt_info.get('acodec', '').upper()
                    if 'opus' in codec_info.lower():
                        codec_info = "Opus"
                    elif 'mp4a' in codec_info.lower():
                        codec_info = "AAC"
                    
                    asr_text = f" {int(fmt_info.get('asr', 0)/1000)}kHz" if fmt_info.get('asr', 0) else ""
                    radio_text = f"🎵 {quality_text} - {fmt_info['ext'].upper()} ({codec_info}){asr_text}{size_text}"
                else:
                    # Video format display
                    audio_indicator = " 🔊" if fmt_info.get('has_audio', False) else ""
                    quality_text = fmt_info['quality']
                    codec_info = ""
                    if 'vp9' in fmt_info.get('vcodec', ''):
                        codec_info = " VP9"
                    elif 'av01' in fmt_info.get('vcodec', ''):
                        codec_info = " AV1"
                    elif 'avc' in fmt_info.get('vcodec', ''):
                        codec_info = " H.264"
                    
                    radio_text = f"{quality_text} - {fmt_info['ext'].upper()}{codec_info} - {fmt_info['fps']}fps{size_text}{audio_indicator}"
                
                radio = ctk.CTkRadioButton(
                    self.quality_scroll,
                    text=radio_text,
                    variable=self.quality_var,
                    value=str(idx),  # Use index as unique identifier
                    font=ctk.CTkFont(size=12)
                )
                radio.pack(anchor="w", pady=5, padx=10)
            
            # Select first option by default
            self.quality_var.set("0")
            button_text = "⬇ Download Audio" if self.download_type == "audio" else "⬇ Download Video"
            self.download_button.configure(state="normal", text=button_text)
        
        self.fetch_button.configure(state="normal", text="Fetch Available Qualities")
        self.progress_label.configure(text="Ready to download")
        self.is_fetching = False
    
    def _show_playlist(self, playlist_title, playlist_count):
        # Clear previous options
        for widget in self.quality_scroll.winfo_children():
            widget.destroy()
        
        # Show playlist info
        self.playlist_info_label.configure(
            text=f"📋 Playlist detected: {playlist_count} videos",
            text_color="#3b8ed0"
        )
        
        # Show playlist title
        title_label = ctk.CTkLabel(
            self.quality_scroll,
            text=f"📋 {playlist_title}",
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=700
        )
        title_label.pack(anchor="w", pady=(5, 10))
        
        info_label = ctk.CTkLabel(
            self.quality_scroll,
            text=f"Found {playlist_count} videos in this playlist",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        info_label.pack(anchor="w", pady=(0, 15))
        
        # Add quality selection for playlist
        quality_label = ctk.CTkLabel(
            self.quality_scroll,
            text="Select quality for all videos:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        quality_label.pack(anchor="w", pady=(5, 10))
        
        # Quality presets for playlist
        self.playlist_quality_var = ctk.StringVar(value="best")
        
        quality_options = [
            ("Best Quality (Highest available)", "best"),
            ("1080p (if available)", "1080p"),
            ("720p (HD)", "720p"),
            ("480p (SD)", "480p"),
            ("360p (Low)", "360p"),
        ]
        
        for label, value in quality_options:
            radio = ctk.CTkRadioButton(
                self.quality_scroll,
                text=label,
                variable=self.playlist_quality_var,
                value=value,
                font=ctk.CTkFont(size=12)
            )
            radio.pack(anchor="w", pady=3, padx=10)
        
        # Separator
        separator = ctk.CTkFrame(self.quality_scroll, height=2, fg_color="gray30")
        separator.pack(fill="x", pady=15)
        
        # Videos list with checkboxes
        videos_label = ctk.CTkLabel(
            self.quality_scroll,
            text="Select videos to download:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        videos_label.pack(anchor="w", pady=(5, 10))
        
        # Select all checkbox
        self.select_all_var = ctk.BooleanVar(value=True)
        select_all_cb = ctk.CTkCheckBox(
            self.quality_scroll,
            text="Select All",
            variable=self.select_all_var,
            command=self._toggle_all_videos,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        select_all_cb.pack(anchor="w", pady=(0, 10), padx=10)
        
        # Individual video checkboxes
        self.video_checkboxes = []
        for idx, video in enumerate(self.playlist_videos):
            duration_min = video['duration'] // 60
            duration_sec = video['duration'] % 60
            duration_text = f" ({duration_min}:{duration_sec:02d})" if video['duration'] > 0 else ""
            
            # Truncate long titles
            title = video['title']
            if len(title) > 80:
                title = title[:77] + "..."
            
            var = ctk.BooleanVar(value=True)
            cb = ctk.CTkCheckBox(
                self.quality_scroll,
                text=f"{idx+1}. {title}{duration_text}",
                variable=var,
                font=ctk.CTkFont(size=11)
            )
            cb.pack(anchor="w", pady=2, padx=20)
            self.video_checkboxes.append((var, video))
        
        # Update button text
        item_type = "Audio Files" if self.download_type == "audio" else "Videos"
        button_text = f"⬇ Download Selected {item_type}"
        self.download_button.configure(state="normal", text=button_text)
        self.fetch_button.configure(state="normal", text="Fetch Available Qualities")
        self.progress_label.configure(text=f"Ready to download {playlist_count} {item_type.lower()}")
        self.is_fetching = False
    
    def _toggle_all_videos(self):
        select_all = self.select_all_var.get()
        for var, _ in self.video_checkboxes:
            var.set(select_all)
    
    def _show_error(self, message):
        messagebox.showerror("Error", message)
        self.fetch_button.configure(state="normal", text="Fetch Available Qualities")
        self.progress_label.configure(text="")
        self.playlist_info_label.configure(text="")
        self.is_fetching = False
    
    def start_download(self):
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        if self.is_playlist:
            # Playlist download
            selected_videos = [video for var, video in self.video_checkboxes if var.get()]
            
            if not selected_videos:
                messagebox.showerror("Error", "Please select at least one video to download")
                return
            
            quality_preset = self.playlist_quality_var.get()
            
            # Confirm download
            response = messagebox.askyesno(
                "Confirm Download",
                f"Download {len(selected_videos)} video(s) at {quality_preset} quality?\n\n"
                f"Location: {self.download_path}"
            )
            
            if not response:
                return
            
            # Reset progress bar
            self.progress_bar.set(0)
            self.progress_label.configure(text=f"Starting playlist download...")
            
            # Disable buttons
            self.download_button.configure(state="disabled")
            self.fetch_button.configure(state="disabled")
            
            thread = threading.Thread(
                target=self._download_playlist_thread,
                args=(selected_videos, quality_preset)
            )
            thread.daemon = True
            thread.start()
        else:
            # Single video download
            selected_quality = self.quality_var.get()
            
            if not selected_quality:
                messagebox.showerror("Error", "Please select a quality")
                return
            
            # Reset progress bar and show initial status
            self.progress_bar.set(0)
            self.progress_label.configure(text="Initializing download...")
            
            # Disable buttons during download
            self.download_button.configure(state="disabled")
            self.fetch_button.configure(state="disabled")
            
            thread = threading.Thread(
                target=self._download_thread,
                args=(url, selected_quality)
            )
            thread.daemon = True
            thread.start()
    
    def _download_thread(self, url, selected_quality):
        try:
            # Find the format info using index
            try:
                format_idx = int(selected_quality)
                if format_idx < 0 or format_idx >= len(self.available_formats):
                    self.root.after(0, self._download_error, "Selected format not found")
                    return
                format_info = self.available_formats[format_idx]
            except (ValueError, IndexError):
                self.root.after(0, self._download_error, "Invalid format selection")
                return
            
            # Prepare download options based on type
            if format_info.get('is_audio', False):
                # Audio download
                format_string = f"{format_info['format_id']}/bestaudio"
                
                ydl_opts = {
                    'format': format_string,
                    'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self._progress_hook],
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'prefer_ffmpeg': True
                }
            else:
                # Video download
                selected_height = format_info['height']
                
                # Use best quality format for selected resolution
                # If format has audio, use it directly; otherwise merge video+audio
                if format_info.get('has_audio', False):
                    # Format already has audio, use it directly
                    format_string = f"{format_info['format_id']}/best[height<={selected_height}]"
                else:
                    # Merge best video and audio for selected resolution
                    format_string = f"bestvideo[height<={selected_height}]+bestaudio/best[height<={selected_height}]"
                
                ydl_opts = {
                    'format': format_string,
                    'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self._progress_hook],
                    'merge_output_format': 'mp4',
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }],
                    'postprocessor_args': [
                        '-c:v', 'copy',           # Copy video codec (no re-encode)
                        '-c:a', 'aac',            # Convert audio to AAC
                        '-b:a', '192k',           # Audio bitrate
                        '-movflags', '+faststart' # Enable streaming
                    ],
                    'prefer_ffmpeg': True
                }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # Update UI on completion
                self.root.after(0, self._download_complete, filename)
                
        except Exception as e:
            self.root.after(0, self._download_error, str(e))
    
    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                # Extract progress information
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded_bytes = d.get('downloaded_bytes', 0)
                
                if total_bytes > 0:
                    progress = downloaded_bytes / total_bytes
                    percent = progress * 100
                else:
                    # Fallback to string parsing
                    percent_str = d.get('_percent_str', '0%').strip().replace('%', '')
                    try:
                        percent = float(percent_str)
                        progress = percent / 100
                    except:
                        progress = 0
                        percent = 0
                
                # Get speed and ETA
                speed = d.get('_speed_str', 'N/A').strip()
                eta = d.get('_eta_str', 'N/A').strip()
                
                # Format downloaded size
                downloaded_mb = downloaded_bytes / (1024 * 1024)
                total_mb = total_bytes / (1024 * 1024) if total_bytes > 0 else 0
                
                if total_mb > 0:
                    size_text = f"{downloaded_mb:.1f}MB / {total_mb:.1f}MB"
                else:
                    size_text = f"{downloaded_mb:.1f}MB"
                
                status_text = f"Downloading... {percent:.1f}% | {size_text} | Speed: {speed} | ETA: {eta}"
                
                self.root.after(0, self._update_progress, progress, status_text)
            except Exception as e:
                # Fallback to basic progress
                try:
                    percent_str = d.get('_percent_str', '0%').strip().replace('%', '')
                    progress = float(percent_str) / 100
                    self.root.after(0, self._update_progress, progress, f"Downloading... {percent_str}%")
                except:
                    pass
        elif d['status'] == 'finished':
            self.root.after(0, self._update_progress, 0.95, "Finalizing download...")
        elif d['status'] == 'error':
            self.root.after(0, self._update_progress, 0, "Download error!")
    
    def _update_progress(self, value, text):
        self.progress_bar.set(value)
        self.progress_label.configure(text=text)
    
    def _playlist_audio_progress_hook(self, d, idx, total_videos, video_title):
        """Progress hook for playlist audio downloads"""
        if d['status'] == 'downloading':
            try:
                # Calculate overall progress
                video_progress = 0
                if 'total_bytes' in d or 'total_bytes_estimate' in d:
                    total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                    downloaded_bytes = d.get('downloaded_bytes', 0)
                    if total_bytes > 0:
                        video_progress = downloaded_bytes / total_bytes
                
                # Overall playlist progress
                overall_progress = ((idx - 1) + video_progress) / total_videos
                
                # Get speed and ETA
                speed = d.get('_speed_str', 'N/A').strip()
                eta = d.get('_eta_str', 'N/A').strip()
                
                # Calculate percentage
                percent = video_progress * 100
                
                status_text = f"🎵 Audio {idx}/{total_videos}: {video_title} - {percent:.0f}% | Speed: {speed} | ETA: {eta}"
                
                self.root.after(0, self._update_progress, overall_progress, status_text)
            except:
                pass
        elif d['status'] == 'finished':
            progress = idx / total_videos
            self.root.after(0, self._update_progress, progress, f"✅ Completed {idx}/{total_videos}: {video_title}")
    
    def _download_playlist_thread(self, selected_videos, quality_preset):
        try:
            total_videos = len(selected_videos)
            downloaded_files = []
            failed_videos = []
            
            for idx, video in enumerate(selected_videos, 1):
                try:
                    # Update progress - starting download
                    progress = (idx - 1) / total_videos
                    video_title = video['title'][:60]
                    item_type = "🎵" if self.download_type == "audio" else "📥"
                    self.root.after(
                        0,
                        self._update_progress,
                        progress,
                        f"{item_type} Item {idx}/{total_videos}: {video_title}..."
                    )
                    
                    # Check if downloading audio or video
                    if self.download_type == "audio":
                        # Audio download for playlist
                        format_string = "bestaudio/best"
                        ydl_opts = {
                            'format': format_string,
                            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                            'quiet': True,
                            'no_warnings': True,
                            'progress_hooks': [lambda d: self._playlist_audio_progress_hook(d, idx, total_videos, video_title)],
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            'prefer_ffmpeg': True
                        }
                    else:
                        # Video download for playlist
                        # Map quality preset to format
                        if quality_preset == "best":
                            format_string = "bestvideo+bestaudio/best"
                        elif quality_preset in ["1080p", "720p", "480p", "360p"]:
                            height = quality_preset.replace('p', '')
                            format_string = f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"
                        else:
                            format_string = "best"
                        
                        # Create a progress hook for this video
                        def playlist_progress_hook(d):
                            if d['status'] == 'downloading':
                                try:
                                    # Calculate overall progress
                                    video_progress = 0
                                    if 'total_bytes' in d or 'total_bytes_estimate' in d:
                                        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                                        downloaded_bytes = d.get('downloaded_bytes', 0)
                                        if total_bytes > 0:
                                            video_progress = downloaded_bytes / total_bytes
                                    
                                    # Overall playlist progress
                                    overall_progress = ((idx - 1) + video_progress) / total_videos
                                    
                                    # Get speed and ETA
                                    speed = d.get('_speed_str', 'N/A').strip()
                                    eta = d.get('_eta_str', 'N/A').strip()
                                    
                                    # Calculate percentage
                                    percent = video_progress * 100
                                    
                                    status_text = f"📥 Video {idx}/{total_videos}: {video_title} - {percent:.0f}% | Speed: {speed} | ETA: {eta}"
                                    
                                    self.root.after(0, self._update_progress, overall_progress, status_text)
                                except:
                                    pass
                            elif d['status'] == 'finished':
                                progress = idx / total_videos
                                self.root.after(0, self._update_progress, progress, f"✅ Completed {idx}/{total_videos}: {video_title}")
                        
                        ydl_opts = {
                            'format': format_string,
                            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                            'quiet': True,
                            'no_warnings': True,
                            'progress_hooks': [playlist_progress_hook],
                            'merge_output_format': 'mp4',
                            'postprocessors': [{
                                'key': 'FFmpegVideoConvertor',
                                'preferedformat': 'mp4',
                            }],
                            'postprocessor_args': [
                                '-c:v', 'copy',           # Copy video codec (no re-encode)
                                '-c:a', 'aac',            # Convert audio to AAC
                                '-b:a', '192k',           # Audio bitrate
                                '-movflags', '+faststart' # Enable streaming
                            ],
                            'prefer_ffmpeg': True
                        }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video['url'], download=True)
                        filename = ydl.prepare_filename(info)
                        downloaded_files.append(filename)
                    
                except Exception as e:
                    failed_videos.append((video['title'], str(e)))
            
            # Show completion message
            self.root.after(0, self._playlist_download_complete, downloaded_files, failed_videos, total_videos)
            
        except Exception as e:
            self.root.after(0, self._download_error, f"Playlist download error: {str(e)}")
    
    def _playlist_download_complete(self, downloaded_files, failed_videos, total_videos):
        self.progress_bar.set(1.0)
        
        success_count = len(downloaded_files)
        failed_count = len(failed_videos)
        item_type = "audio files" if self.download_type == "audio" else "videos"
        
        message = f"Playlist Download Complete!\n\n"
        message += f"✅ Successfully downloaded: {success_count}/{total_videos} {item_type}\n"
        
        if failed_count > 0:
            message += f"❌ Failed: {failed_count} {item_type}\n\n"
            message += f"Failed {item_type}:\n"
            for title, error in failed_videos[:5]:  # Show first 5 failures
                message += f"  • {title[:50]}\n"
            if failed_count > 5:
                message += f"  ... and {failed_count - 5} more\n"
        
        message += f"\nLocation:\n{self.download_path}"
        
        if failed_count > 0:
            messagebox.showwarning("Download Complete with Errors", message)
        else:
            messagebox.showinfo("Success", message)
        
        # Re-enable buttons
        self.download_button.configure(state="normal")
        self.fetch_button.configure(state="normal")
        self.progress_bar.set(0)
        self.progress_label.configure(text="")
    
    def _download_complete(self, filepath):
        self.progress_bar.set(1.0)
        self.progress_label.configure(text="Download complete!")
        item_type = "Audio" if self.download_type == "audio" else "Video"
        
        messagebox.showinfo(
            "Success",
            f"{item_type} downloaded successfully!\n\nLocation:\n{filepath}"
        )
        
        # Re-enable buttons
        self.download_button.configure(state="normal")
        if self.is_playlist:
            self.download_button.configure(text="Download Selected Videos")
        else:
            self.download_button.configure(text="Download Video")
        self.fetch_button.configure(state="normal")
        self.progress_bar.set(0)
        self.progress_label.configure(text="")
    
    def _download_error(self, error_message):
        messagebox.showerror("Download Error", f"Failed to download video:\n{error_message}")
        
        # Re-enable buttons
        self.download_button.configure(state="normal")
        self.fetch_button.configure(state="normal")
        self.progress_bar.set(0)
        self.progress_label.configure(text="")
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.run()
