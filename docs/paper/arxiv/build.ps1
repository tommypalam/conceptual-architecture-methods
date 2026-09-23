# Build the arXiv preprint PDF from docs/paper/paper_draft.md.
# Run: powershell -File docs/paper/arxiv/build.ps1
# Output: docs/paper/arxiv/preprint.pdf  (and preprint.tex for arXiv upload)
# Figures are read from docs/paper/figures/; regenerate them with
#   python docs/paper/analysis/paper_item_robustness.py experiments docs/paper/analysis/paper_item_robustness.json
#   python docs/paper/analysis/paper_figures.py docs/paper/analysis/paper_item_robustness.json docs/paper/figures
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$env:PATH = "$env:APPDATA\TinyTeX\bin\windows;C:\Program Files\RStudio\resources\app\bin\quarto\bin\tools;$env:PATH"
Push-Location (Join-Path $root 'docs/paper')
try {
    foreach ($out in @('arxiv/preprint.tex', 'arxiv/preprint.pdf')) {
        & pandoc paper_draft.md -s -o $out `
            --resource-path=. `
            --pdf-engine=xelatex `
            --include-in-header=arxiv/preamble.tex `
            --citeproc --bibliography=arxiv/references.bib `
            -V documentclass=article -V classoption=11pt `
            -V geometry:a4paper `
            -V geometry:top=2.5cm -V geometry:bottom=2.5cm `
            -V geometry:left=2.7cm -V geometry:right=2.7cm `
            -V colorlinks=true -V linkcolor=black -V urlcolor=blue -V citecolor=black
        if ($LASTEXITCODE -ne 0) { throw "pandoc failed for $out" }
    }
    Write-Host 'built docs/paper/arxiv/preprint.pdf and preprint.tex'
}
finally { Pop-Location }
