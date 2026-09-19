# Builds docs/thesis.pdf from docs/thesis.md with pandoc and xelatex.
#
# Requirements on this machine: pandoc (bundled with RStudio's quarto) and a
# TeX Live distribution providing xelatex, tex-gyre and dejavu (TinyTeX, installed
# with `quarto install tinytex`). Run from the repository root:
#
#     powershell -File docs/thesis_build/build.ps1
#
# The build is deterministic apart from the PDF creation date. It makes no API
# calls and touches nothing outside docs/thesis.pdf.

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$env:PATH = "$env:APPDATA\TinyTeX\bin\windows;C:\Program Files\RStudio\resources\app\bin\quarto\bin\tools;$env:PATH"

Push-Location $root
try {
    pandoc docs/thesis.md -o docs/thesis.pdf `
        --pdf-engine=xelatex `
        --include-in-header=docs/thesis_build/preamble.tex `
        --resource-path=docs `
        -V mainfont="TeX Gyre Pagella" `
        -V monofont="DejaVuSansMono" `
        -V monofontoptions="Extension=.ttf,BoldFont=DejaVuSansMono-Bold,ItalicFont=DejaVuSansMono-Oblique,Scale=MatchLowercase" `
        -V geometry:a4paper `
        -V geometry:top=2.6cm -V geometry:bottom=2.6cm -V geometry:left=2.8cm -V geometry:right=2.8cm `
        -V fontsize=11pt `
        -V linkcolor=black -V urlcolor=black -V citecolor=black `
        -V toc-depth=2 `
        -V title="Concepts as Architecture"
    if (Test-Path "docs/thesis.pdf") { "built docs/thesis.pdf" } else { throw "pandoc produced no PDF" }
}
finally {
    Pop-Location
}
