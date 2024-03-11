#define MyAppName "removebg_infusiblecoder"
#define MyAppVersion "STABLE"
#define MyAppPublisher "syedusama5556"
#define MyAppURL "https://github.com/syedusama5556/removebg_infusiblecoder"
#define MyAppExeName "removebg_infusiblecoder.exe"
#define MyAppId "49AB7484-212F-4B31-A49F-533A480F3FD4"

[Setup]
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputBaseFilename=removebg_infusiblecoder-cli-installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern
OutputDir=dist
ChangesEnvironment=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "{#SourcePath}dist\removebg_infusiblecoder\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourcePath}dist\removebg_infusiblecoder\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Tasks]
Name: modifypath; Description: "Add to PATH variable"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Code]
const
    ModPathName = 'modifypath';
    ModPathType = 'user';

function ModPathDir(): TArrayOfString;
begin
    setArrayLength(Result, 1)
    Result[0] := ExpandConstant('{app}');
end;
#include "_modpath.iss"