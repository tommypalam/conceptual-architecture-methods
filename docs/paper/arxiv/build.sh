#!/bin/sh
# Build the preprint from docs/paper/paper_draft.md (run from docs/paper).
set -e
for out in arxiv/preprint.tex arxiv/preprint.pdf; do
  pandoc paper_draft.md -s -o "$out" --resource-path=. \
    --pdf-engine=xelatex \
    --include-in-header=arxiv/preamble.tex \
    --citeproc --bibliography=arxiv/references.bib \
    -V documentclass=article -V classoption=11pt -V geometry:a4paper \
    -V geometry:top=2.5cm -V geometry:bottom=2.5cm \
    -V geometry:left=2.7cm -V geometry:right=2.7cm \
    -V colorlinks=true -V linkcolor=black -V urlcolor=blue -V citecolor=black
done
