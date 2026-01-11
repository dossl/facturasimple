import re
import sys
from pathlib import Path
from datetime import datetime

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer


def normalize_ws(s: str) -> str:
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    # Collapse excessive spaces but keep newlines.
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def page_text(pdf_path: Path):
    for i, page_layout in enumerate(extract_pages(str(pdf_path)), start=1):
        chunks = []
        for el in page_layout:
            if isinstance(el, LTTextContainer):
                chunks.append(el.get_text())
        yield i, normalize_ws("".join(chunks))


def split_paragraphs(page: str):
    # Paragraph = blocks separated by one or more blank lines.
    parts = [p.strip() for p in re.split(r"\n\s*\n", page) if p.strip()]
    return parts


def main():
    if len(sys.argv) < 3:
        print("Usage: pdf_to_pages.py <input.pdf> <output.txt>")
        raise SystemExit(2)

    pdf_path = Path(sys.argv[1]).expanduser().resolve()
    out_path = Path(sys.argv[2]).expanduser().resolve()

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"SOURCE_PDF: {pdf_path}\n")
        f.write(f"EXTRACTED_AT: {datetime.now().isoformat()}\n")
        f.write("PARAGRAPH_RULE: paragraphs are blocks separated by blank lines in extracted text; numbering restarts each page.\n")
        f.write("\n")

        for page_no, text in page_text(pdf_path):
            f.write(f"=== PAGE {page_no} ===\n")
            if not text:
                f.write("(no text extracted)\n\n")
                continue
            paras = split_paragraphs(text)
            for idx, p in enumerate(paras, start=1):
                # Keep internal single newlines but avoid huge wrapping issues.
                f.write(f"[P{idx}] {p}\n\n")


if __name__ == "__main__":
    main()
