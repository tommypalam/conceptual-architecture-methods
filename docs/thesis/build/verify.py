"""Read-only checks on the Bocconi submission PDF, not research reanalysis.

Run with a Python environment containing pypdf and pdfplumber:
    python docs/thesis/build/verify.py
"""
from __future__ import annotations

import hashlib
import json
import statistics
from pathlib import Path

import pdfplumber
from pypdf import PdfReader

# This file lives in docs/thesis/build, three levels below the repository root.
ROOT = Path(__file__).resolve().parents[3]
PDF = ROOT / "docs/thesis/LF3262767.pdf"


def verify():
    reader = PdfReader(PDF)
    texts = [p.extract_text() or "" for p in reader.pages]
    assert len(texts) > 4
    assert all(not t.strip() for t in texts[:4]), "Opening pages are not blank"
    assert texts[4].startswith("Contents"), "Contents must start after four blanks"
    assert PDF.stat().st_size < 10_000_000, "Exceeds 10 MB"
    combined = "\n".join(texts)
    for forbidden in ("Tommaso", "Palamenga", "3262767", "Supervisor", "Academic Year"):
        assert forbidden not in combined, f"Personal/title-page text: {forbidden}"
    assert not reader.metadata.get("/Author"), "Author metadata must be empty"
    for number, (page, text) in enumerate(zip(reader.pages, texts), 1):
        assert abs(float(page.mediabox.width) - 595.28) < 1
        assert abs(float(page.mediabox.height) - 841.89) < 1
        if number > 4:
            assert text.rstrip().splitlines()[-1] == str(number - 4), (
                f"Incorrect footer on physical page {number}"
            )
    assert "Abstract\n" not in combined
    # Markers are matched with ALL whitespace removed from both sides. Text
    # extraction drops inter-word spaces in tightly kerned compact-type table
    # cells, and whether it does depends on the pypdf version: "no finite SE"
    # extracts as "nofinite SE" under pypdf 6.19. Every character of the marker
    # must still be present and in order; only spacing is forgiven.
    dense = "".join(combined.split())
    for marker in ("sample_draw", "+0.375", "+0.064", "0.061", "0.095",
                   "Appendix C", "no finite SE", "unit-bootstrap"):
        assert "".join(marker.split()) in dense, f"Missing required content: {marker}"

    intro = next(i for i, t in enumerate(texts) if t.startswith("1. Introduction\n"))
    references = next(i for i, t in enumerate(texts) if t.startswith("References\n"))
    appendix = next(i for i, t in enumerate(texts) if t.startswith("Appendix A"))
    body_pages = references - intro
    appendix_pages = len(texts) - appendix
    assert body_pages + appendix_pages <= 30, "Body and appendices exceed 30 pages"

    abstract = (ROOT / "docs/thesis/abstract.txt").read_text(encoding="utf-8").strip()
    assert len(abstract) <= 4000, "Portal abstract exceeds 4,000 characters"
    # docs/abstract.md stays at its old path because frozen reports link to it.
    # It must carry the portal abstract verbatim, so the two copies cannot drift.
    squeeze = lambda s: " ".join(s.split())
    published = (ROOT / "docs/abstract.md").read_text(encoding="utf-8")
    assert squeeze(abstract) in squeeze(published), (
        "docs/abstract.md no longer contains the portal abstract verbatim")

    body_line_counts = []
    spacings = []
    margin_violations = []
    fonts = set()
    with pdfplumber.open(PDF) as pdf:
        for index, page in enumerate(pdf.pages):
            chars = [c for c in page.chars if c["text"].strip()]
            fonts.update(c["fontname"].split("+")[-1] for c in chars)
            for c in chars:
                if c["x0"] < 70.86 - 1 or c["x1"] > 524.42 + 1:
                    margin_violations.append([index + 1, c["text"], round(c["x0"], 2), round(c["x1"], 2)])
            # PDF points differ from TeX points by 72/72.27.
            body = [c for c in chars if abs(c["size"] - 11.955) < 0.12
                    and "Arial" in c["fontname"] and c["top"] < 775]
            tops = sorted({round(c["top"], 1) for c in body})
            rows = []
            for top in tops:
                if not rows or top - rows[-1] > 2:
                    rows.append(top)
            if intro <= index < references:
                body_line_counts.append(len(rows))
                spacings.extend(b - a for a, b in zip(rows, rows[1:]) if 20 < b - a < 27)
    assert not margin_violations, f"Text exceeds side margins: {margin_violations[:12]}"
    assert "ArialMT" in fonts, f"Arial not found: {fonts}"
    assert max(body_line_counts) <= 30, body_line_counts
    assert spacings and 23 < statistics.median(spacings) < 25

    embedded = set()
    for page in reader.pages:
        resources = page.get("/Resources").get_object()
        for ref in resources.get("/Font", {}).get_object().values() if hasattr(resources.get("/Font", {}), "get_object") else []:
            font = ref.get_object()
            descendants = font.get("/DescendantFonts", [font])
            for child in descendants:
                child = child.get_object()
                descriptor = child.get("/FontDescriptor")
                if descriptor:
                    desc = descriptor.get_object()
                    assert any(k in desc for k in ("/FontFile", "/FontFile2", "/FontFile3")), child
                    embedded.add(str(desc.get("/FontName")))
    return {
        "file": PDF.name, "sha256": hashlib.sha256(PDF.read_bytes()).hexdigest(),
        "bytes": PDF.stat().st_size, "physical_pages": len(texts),
        "blank_opening_pages": 4, "contents_pages": intro - 4,
        "body_pages": body_pages, "reference_pages": appendix - references,
        "appendix_pages": appendix_pages,
        "body_and_appendix_pages": body_pages + appendix_pages,
        "abstract_characters": len(abstract), "body_font": "Arial, 12 TeX points",
        "median_body_baseline_gap_pdf_points": round(statistics.median(spacings), 3),
        "max_body_text_rows_on_a_page": max(body_line_counts),
        "side_margins_cm": 2.5, "margin_violations": 0,
        "embedded_page_fonts": sorted(embedded),
        "personal_information_absent": True, "abstract_md_consistent": True,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, ensure_ascii=False))
