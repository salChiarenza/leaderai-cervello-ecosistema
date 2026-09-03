$ErrorActionPreference = "Stop"

$hookInput = [Console]::In.ReadToEnd()
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$guardScript = Join-Path $scriptDirectory "guardiano_stanze.sh"

$candidates = @()
$gitCommand = Get-Command git.exe -ErrorAction SilentlyContinue
if ($gitCommand) {
    $gitDirectory = Split-Path -Parent $gitCommand.Source
    $gitRoot = Split-Path -Parent $gitDirectory
    $candidates += (Join-Path $gitRoot "bin\bash.exe")
    $candidates += (Join-Path $gitRoot "usr\bin\bash.exe")
}
if ($env:ProgramFiles) {
    $candidates += (Join-Path $env:ProgramFiles "Git\bin\bash.exe")
}
if (${env:ProgramFiles(x86)}) {
    $candidates += (Join-Path ${env:ProgramFiles(x86)} "Git\bin\bash.exe")
}
if ($env:LOCALAPPDATA) {
    $candidates += (Join-Path $env:LOCALAPPDATA "Programs\Git\bin\bash.exe")
}
$bashCommand = Get-Command bash.exe -ErrorAction SilentlyContinue
if ($bashCommand -and $bashCommand.Source -notmatch "\\Windows\\System32\\" -and $bashCommand.Source -match "\\Git\\") {
    $candidates += $bashCommand.Source
}
$bashPath = $candidates | Where-Object {
    $_ -and (Test-Path -LiteralPath $_) -and $_ -notmatch "\\Windows\\System32\\"
} | Select-Object -Unique -First 1

if (-not $bashPath) {
    $active = $false
    try {
        $active = [bool](($hookInput | ConvertFrom-Json).stop_hook_active)
    } catch {
        $active = $false
    }
    if ($active) {
        [Console]::Out.WriteLine('{"systemMessage":"Il controllo finale richiede Git Bash, che non risulta disponibile su questa postazione."}')
        exit 0
    }
    [Console]::Error.WriteLine("BLOCCO STRUTTURA: Git Bash non disponibile per il controllo finale.")
    exit 2
}

$hookInput | & $bashPath $guardScript @args
if ($LASTEXITCODE -ne 0) {
    exit 2
}
exit 0
