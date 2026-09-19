$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$viewerUrl = 'http://127.0.0.1:8772/explore'
function Test-Viewer {
    try {
        $response = Invoke-WebRequest -Uri $viewerUrl -UseBasicParsing -TimeoutSec 2
        return ($response.StatusCode -eq 200 -and $response.Content -match 'explore.js')
    } catch { return $false }
}
try {
    if (-not (Test-Viewer)) {
        $logDir = Join-Path $projectRoot 'output'
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        $viewerProcess = Start-Process -FilePath 'py.exe' -ArgumentList '-3.11 -B code/serve_replay.py --port 8772' -WorkingDirectory $projectRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $logDir 'visualiser-launch.log') -RedirectStandardError (Join-Path $logDir 'visualiser-launch-error.log')
        $ready = $false
        for ($attempt = 0; $attempt -lt 90; $attempt++) {
            if (Test-Viewer) { $ready = $true; break }
            if ($viewerProcess.HasExited) { break }
            Start-Sleep -Milliseconds 1000
        }
        if (-not $ready) { throw 'The visualiser could not start. Check output\visualiser-launch-error.log in the project folder.' }
    }
    Start-Process $viewerUrl
} catch {
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.MessageBox]::Show($_.Exception.Message, 'PARIA visualiser') | Out-Null
    exit 1
}
