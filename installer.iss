; YouTube Downloader Pro - Inno Setup Installer Script
; This creates a professional Windows installer

#define MyAppName "YouTube Downloader Pro"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "El-Mostafi"
#define MyAppURL "https://github.com/El-Mostafi/youtube-downloader-pro"
#define MyAppExeName "app.py"

[Setup]
AppId={{8F9B4D5C-1A2E-4B3C-9D8E-7F6A5B4C3D2E}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=installer_output
OutputBaseFilename=YouTubeDownloaderPro_Setup_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "app.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "setup_and_run.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "QUICK_START.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "*.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "pythonw.exe"; Parameters: """{app}\app.py"""; WorkingDir: "{app}"
Name: "{group}\Setup & Run"; Filename: "{app}\QUICK_START.bat"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "pythonw.exe"; Parameters: """{app}\app.py"""; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\QUICK_START.bat"; Description: "Run setup and launch application"; Flags: postinstall shellexec skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  
  // Check if Python is installed
  if not FileExists('C:\Python312\python.exe') and not DirExists('C:\Python311') then
  begin
    if MsgBox('Python is not detected on your system. Would you like to download Python?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      ShellExec('open', 'https://www.python.org/downloads/', '', '', SW_SHOW, ewNoWait, ResultCode);
    end;
  end;
end;
