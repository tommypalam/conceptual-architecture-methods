# Build the arXiv preprint PDF from docs/paper/paper_draft.md.
# Run: powershell -File docs/paper/arxiv/build.ps1
# Output: docs/paper/arxiv/preprint.pdf  (and preprint.tex for arXiv upload)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$env:PATH = "$env:APPDATA\TinyTeX\bin\windows;C:\Program Files\RStudio\resources\app\bin\quarto\bin\tools;$env:PATH"
Push-Location $root
try {
    # arXiv wants TeX source, so emit the .tex alongside the PDF.
    & pandoc docs/paper/paper_draft.md -s `
        -o docs/paper/arxiv/preprint.tex `
        --include-in-header=docs/paper/arxiv/preamble.tex `
        --citeproc --bibliography=docs/paper/arxiv/references.bib `
        -V documentclass=article -V classoption=11pt `
        -V geometry:a4paper `
        -V geometry:top=2.5cm -V geometry:bottom=2.5cm `
        -V geometry:left=2.7cm -V geometry:right=2.7cm `
        -V colorlinks=true -V linkcolor=black -V urlcolor=blue
    if ($LASTEXITCODE -ne 0) { throw 'pandoc (tex) failed' }

    & pandoc docs/paper/paper_draft.md -s `
        -o docs/paper/arxiv/preprint.pdf `
        --pdf-engine=xelatex `
        --include-in-header=docs/paper/arxiv/preamble.tex `
        --citeproc --bibliography=docs/paper/arxiv/references.bib `
        -V documentclass=article -V classoption=11pt `
        -V geometry:a4paper `
        -V geometry:top=2.5cm -V geometry:bottom=2.5cm `
        -V geometry:left=2.7cm -V geometry:right=2.7cm `
        -V colorlinks=true -V linkcolor=black -V urlcolor=blue
    if ($LASTEXITCODE -ne 0) { throw 'pandoc (pdf) failed' }
    Write-Host 'built docs/paper/arxiv/preprint.pdf and preprint.tex'
}
finally { Pop-Location }
