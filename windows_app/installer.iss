[Setup]
AppId=RotaryDeckCompanion
AppName=RotaryDeck Companion
AppVersion=0.3.0
AppVerName=RotaryDeck Companion 0.3.0 Preview
AppPublisher=Shubham Mehta
AppPublisherURL=https://github.com/Justme017/RotaryDeck
AppSupportURL=https://github.com/Justme017/RotaryDeck/issues
DefaultDirName={localappdata}\Programs\RotaryDeck
DefaultGroupName=RotaryDeck
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=dist
OutputBaseFilename=RotaryDeckSetup-Windows-x64-preview
SetupIconFile=assets\rotarydeck.ico
UninstallDisplayIcon={app}\RotaryDeckCompanion.exe
AppMutex=Local\RotaryDeckCompanion
CloseApplications=yes
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
LicenseFile=..\LICENSE
[Tasks]
Name: startup; Description: "Start RotaryDeck with Windows in the system tray"; GroupDescription: "Startup:"; Flags: checkedonce
[Files]
Source: "dist\RotaryDeckCompanion.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\THIRD_PARTY_NOTICES.md"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{group}\RotaryDeck"; Filename: "{app}\RotaryDeckCompanion.exe"
[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "RotaryDeck Companion"; ValueData: """{app}\RotaryDeckCompanion.exe"" --background"; Tasks: startup; Flags: uninsdeletevalue
[Run]
Filename: "{app}\RotaryDeckCompanion.exe"; Parameters: "--background"; Description: "Launch RotaryDeck in the system tray"; Flags: nowait postinstall skipifsilent
