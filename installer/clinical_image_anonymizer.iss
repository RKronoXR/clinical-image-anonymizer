#define AppName "Clinical Image Anonymizer"
#define AppVersion "1.0.0"
#define AppPublisher "ACTA AI Lab"
#define AppExeName "Clinical Image Anonymizer.exe"
#define CliExeName "clinical-image-anonymizer.exe"

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL=https://github.com/RKronoXR/clinical-image-anonymizer
AppSupportURL=https://github.com/RKronoXR/clinical-image-anonymizer/issues
AppUpdatesURL=https://github.com/RKronoXR/clinical-image-anonymizer/releases
DefaultDirName={autopf}\Clinical Image Anonymizer
DefaultGroupName=Clinical Image Anonymizer
OutputDir=..\dist\installer
OutputBaseFilename=ClinicalImageAnonymizerSetup_v1.0.0
SetupIconFile=..\assets\icons\clinical_image_anonymizer.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ChangesEnvironment=yes
UninstallDisplayIcon={app}\{#AppExeName}
VersionInfoCompany=ACTA AI Lab
VersionInfoDescription=Clinical Image Anonymizer Windows Installer
VersionInfoProductName=Clinical Image Anonymizer
VersionInfoProductVersion={#AppVersion}
VersionInfoVersion={#AppVersion}

[Files]
Source: "..\dist\Clinical Image Anonymizer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\dist\clinical-image-anonymizer.exe"; DestDir: "{app}"; Flags: ignoreversion

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"
Name: "addtopath"; Description: "Add Clinical Image Anonymizer CLI to the user PATH"; GroupDescription: "Command-line interface:"; Flags: checkedonce

[Icons]
Name: "{group}\Clinical Image Anonymizer"; Filename: "{app}\{#AppExeName}"
Name: "{group}\Clinical Image Anonymizer CLI Help"; Filename: "{cmd}"; Parameters: "/K ""{app}\{#CliExeName}"" --help"
Name: "{autodesktop}\Clinical Image Anonymizer"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Check: NeedsAddPath(ExpandConstant('{app}')); Tasks: addtopath; Flags: preservestringtype

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch Clinical Image Anonymizer"; Flags: nowait postinstall skipifsilent

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', OrigPath) then
  begin
    Result := True;
    exit;
  end;

  Result := Pos(';' + Uppercase(Param) + ';', ';' + Uppercase(OrigPath) + ';') = 0;
end;
