import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

import fitz  # PyMuPDF


def normalize_ws(s: str) -> str:
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def split_paragraphs(page: str):
    parts = [p.strip() for p in re.split(r"\n\s*\n", page) if p.strip()]
    return parts


def ocr_image(png_path: Path) -> str:
    # tesseract writes to stdout with '-' output
    cmd = [
        "/opt/homebrew/bin/tesseract",
        str(png_path),
        "stdout",
        "-l",
        "eng",
        "--psm",
        "6",
    ]
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8", errors="replace")


def main():
    if len(sys.argv) < 3:
        print("Usage: pdf_ocr_to_pages.py <input.pdf> <output.txt>")
        raise SystemExit(2)

    pdf_path = Path(sys.argv[1]).expanduser().resolve()
    out_path = Path(sys.argv[2]).expanduser().resolve()
    tmp_dir = out_path.parent / (out_path.stem + "_pages")
    tmp_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))

    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"SOURCE_PDF: {pdf_path}\n")
        f.write(f"EXTRACTED_AT: {datetime.now().isoformat()}\n")
        f.write("EXTRACTION_METHOD: OCR (tesseract eng) over rendered page images (PyMuPDF).\n")
        f.write("PARAGRAPH_RULE: paragraphs are blocks separated by blank lines in OCR text; numbering restarts each page.\n")
        f.write("\n")

        for i in range(doc.page_count):
            page_no = i + 1
            page = doc.load_page(i)
            # Render at ~200 DPI for OCR quality.
            mat = fitz.Matrix(2, 2)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            png_path = tmp_dir / f"page_{page_no:03d}.png"
            pix.save(str(png_path))

            ocr_text = normalize_ws(ocr_image(png_path))
            f.write(f"=== PAGE {page_no} ===\n")
            if not ocr_text:
                f.write("(no text extracted)\n\n")
                continue
            paras = split_paragraphs(ocr_text)
            for idx, p in enumerate(paras, start=1):
                f.write(f"[P{idx}] {p}\n\n")


if __name__ == "__main__":
    main()
