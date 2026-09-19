# Build the anonymous Bocconi undergraduate upload; no model/API calls.
# Run: powershell -File docs/thesis_build/build.ps1
param([string]$StudentId = '3262767')
$ErrorActionPreference = 'Stop'
if ($StudentId -notmatch '^\d+$') { throw 'StudentId must contain digits only.' }
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$env:PATH = "$env:APPDATA\TinyTeX\bin\windows;C:\Program Files\RStudio\resources\app\bin\quarto\bin\tools;$env:PATH"
$taskBuildDir = Join-Path ([System.IO.Path]::GetTempPath()) ('bocconi-thesis-' + [guid]::NewGuid())
New-Item -ItemType Directory -Path $taskBuildDir | Out-Null
$taskLatex = Join-Path $taskBuildDir 'thesis.tex'
$taskLog = Join-Path $taskBuildDir 'build.log'
$uploadPath = Join-Path $root "docs/LF$StudentId.pdf"
Push-Location $root
try {
    & pandoc docs/thesis.md -s -o $taskLatex `
        --include-in-header=docs/thesis_build/preamble.tex `
        --resource-path=docs `
        -V mainfont=Arial -V sansfont=Arial `
        -V monofont=DejaVuSansMono `
        -V 'monofontoptions=Extension=.ttf,BoldFont=DejaVuSansMono-Bold,ItalicFont=DejaVuSansMono-Oblique,Scale=MatchLowercase' `
        -V geometry:a4paper `
        -V geometry:top=2.5cm -V geometry:bottom=2.5cm `
        -V geometry:left=2.5cm -V geometry:right=2.5cm `
        -V fontsize=12pt -V linkcolor=black -V urlcolor=black -V citecolor=black `
        --toc-depth=1
    if ($LASTEXITCODE -ne 0) { throw 'Pandoc failed.' }
    $taskText = [IO.File]::ReadAllText($taskLatex)
    $taskText = $taskText.Replace('{figures/', '{docs/figures/')
    [IO.File]::WriteAllText($taskLatex, $taskText, [Text.UTF8Encoding]::new($false))
    foreach ($pass in 1..3) {
        & xelatex -interaction=nonstopmode -halt-on-error "-output-directory=$taskBuildDir" $taskLatex *> $taskLog
        if ($LASTEXITCODE -ne 0) {
            Get-Content $taskLog -Tail 50
            throw "XeLaTeX failed; diagnostics: $taskLog"
        }
    }
    $taskPdf = Join-Path $taskBuildDir 'thesis.pdf'
    if (-not (Test-Path -LiteralPath $taskPdf)) { throw 'No PDF was produced.' }
    Copy-Item -LiteralPath $taskPdf -Destination $uploadPath -Force
    Copy-Item -LiteralPath $taskPdf -Destination (Join-Path $root 'docs/thesis.pdf') -Force
    Write-Output "Built $uploadPath and docs/thesis.pdf"
    Write-Output "Build diagnostics: $taskBuildDir"
    Select-String -LiteralPath (Join-Path $taskBuildDir 'thesis.log') -Pattern 'Overfull|Missing character|undefined references'
}
finally { Pop-Location }
