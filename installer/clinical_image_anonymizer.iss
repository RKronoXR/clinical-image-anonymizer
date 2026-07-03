[Setup]
AppName=Clinical Image Anonymizer
AppVersion=1.0.0
AppPublisher=ACTA AI Lab
DefaultDirName={autopf}\Clinical Image Anonymizer
DefaultGroupName=Clinical Image Anonymizer
OutputDir=..\dist\installer
OutputBaseFilename=ClinicalImageAnonymizerSetup_v1.0.0
SetupIconFile=..\assets\icons\clinical_image_anonymizer.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "..\dist\Clinical Image Anonymizer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Icons]
Name: "{group}\Clinical Image Anonymizer"; Filename: "{app}\Clinical Image Anonymizer.exe"
Name: "{autodesktop}\Clinical Image Anonymizer"; Filename: "{app}\Clinical Image Anonymizer.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Clinical Image Anonymizer.exe"; Description: "Launch Clinical Image Anonymizer"; Flags: nowait postinstall skipifsilent