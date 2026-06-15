"""Render all website pages to a single PDF via headless Chromium.

Takes full-page screenshots at 1440px desktop viewport and assembles
them into a clean PDF. Each website page starts on a new PDF page.

Requires: playwright, Pillow, reportlab
Requires: Astro dev server running on localhost:4321
Run: python3 brand/render_website_pdf.py
"""

from __future__ import annotations

import math
import tempfile
from pathlib import Path

from PIL import Image as PILImage
from playwright.sync_api import sync_playwright
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdfcanvas

PROJECT = Path(__file__).parent.parent
OUTPUT = PROJECT / "brand" / "website_review_rendered_2026-06-07.pdf"

PAGES = [
    ("/", "01 — Home", "01_home"),
    ("/about", "02 — About", "02_about"),
    ("/services", "03 — Services", "03_services"),
    ("/services/travel-alpine", "04 — Travel & Alpine", "04_travel_alpine"),
    ("/services/behavioral-harmony", "05 — Behavioral & Harmony", "05_behavioral_harmony"),
    ("/services/elite-relief", "06 — Elite Relief", "06_elite_relief"),
    ("/agencies", "07 — For Agencies", "07_agencies"),
    ("/contact", "08 — Contact", "08_contact"),
    ("/privacy", "09 — Privacy Policy", "09_privacy"),
    ("/imprint", "10 — Imprint", "10_imprint"),
]

BASE_URL = "http://localhost:4321"

# PDF page: A4 landscape (842 x 595 pt). We use the full width for the
# screenshot and leave a small margin for header/footer.
PAGE_W = 842  # A4 landscape width in points
PAGE_H = 595  # A4 landscape height in points
MARGIN_TOP = 18 * mm
MARGIN_BOTTOM = 12 * mm
MARGIN_LR = 8 * mm
USABLE_W = PAGE_W - 2 * MARGIN_LR
USABLE_H = PAGE_H - MARGIN_TOP - MARGIN_BOTTOM

NAVY = HexColor("#0E1A3A")
GOLD = HexColor("#B8893A")
MUTED = HexColor("#5A5F73")


def draw_header_footer(c, page_label: str, page_num: int):
    """Draw header and footer on each PDF page."""
    c.saveState()
    # Header line
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.4)
    c.line(MARGIN_LR, PAGE_H - MARGIN_TOP + 4 * mm,
           PAGE_W - MARGIN_LR, PAGE_H - MARGIN_TOP + 4 * mm)
    # Header text
    c.setFont("Helvetica", 7)
    c.setFillColor(MUTED)
    c.drawString(MARGIN_LR, PAGE_H - MARGIN_TOP + 6 * mm,
                 f"Riviera & Ridge · Website-Entwurf · {page_label}")
    c.drawRightString(PAGE_W - MARGIN_LR, PAGE_H - MARGIN_TOP + 6 * mm,
                      "7. Juni 2026 · Zur Durchsicht")
    # Footer
    c.setFont("Helvetica", 7)
    c.setFillColor(MUTED)
    c.drawCentredString(PAGE_W / 2, MARGIN_BOTTOM - 6 * mm, f"Seite {page_num}")
    c.restoreState()


def main():
    tmp_dir = Path(tempfile.mkdtemp(prefix="rr_pdf_"))
    screenshots: list[tuple[Path, str]] = []

    # ── 1. Capture full-page screenshots ──────────────────────────────────
    print("  Capturing screenshots (1440px desktop viewport) ...\n")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.emulate_media(media="screen")

        for route, label, filename in PAGES:
            url = f"{BASE_URL}{route}"
            print(f"    {label:40s} {url}")
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(1000)

            img_path = tmp_dir / f"{filename}.png"
            page.screenshot(path=str(img_path), full_page=True)
            screenshots.append((img_path, label))

        browser.close()

    # ── 2. Assemble PDF ───────────────────────────────────────────────────
    print(f"\n  Assembling PDF ({len(screenshots)} pages) ...")
    c = pdfcanvas.Canvas(str(OUTPUT), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Riviera & Ridge — Website-Texte zur Durchsicht")
    c.setAuthor("Felix (für SG)")

    # Cover page
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(30 * mm, PAGE_H - 40 * mm, 30 * mm, 0.8 * mm, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 28)
    c.drawString(30 * mm, PAGE_H - 55 * mm, "Riviera & Ridge")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30 * mm, PAGE_H - 67 * mm, "Website — Desktop-Ansicht zur Durchsicht")
    c.setFont("Helvetica", 12)
    c.drawString(30 * mm, PAGE_H - 82 * mm, "Alle 10 Seiten · Stand 7. Juni 2026")
    c.setFillColor(HexColor("#A9B8C9"))
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(30 * mm, PAGE_H - 96 * mm,
                 "Desktop-Ansicht (1440px) · Primärsprache Englisch")

    # Intro text
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica", 10.5)
    intro_lines = [
        "Liebe Saskia,",
        "",
        "dieses PDF zeigt alle Website-Seiten so, wie sie auf einem Desktop-",
        "Bildschirm aussehen werden. Jede Seite beginnt auf einer neuen PDF-Seite.",
        "",
        "Was ich von dir brauche:",
        "  1.  Klingt das nach dir? Wo nicht?",
        "  2.  Stimmen die fachlichen Aussagen?",
        "  3.  Welche Sätze möchtest du auf keinen Fall so stehen lassen?",
        "  4.  Sind die Preise korrekt dargestellt?",
        "  5.  Fehlt etwas Wichtiges?",
    ]
    y = PAGE_H - 116 * mm
    for line in intro_lines:
        c.drawString(30 * mm, y, line)
        y -= 5 * mm

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(30 * mm, 28 * mm, "Kein Zeitdruck — lies es in Ruhe durch und markiere, was auffällt.")
    c.setFillColor(HexColor("#A9B8C9"))
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawString(30 * mm, 22 * mm,
                 "Intern · nicht zur Weitergabe an Familien oder Agenturen vor Freigabe.")
    c.showPage()

    # Render each screenshot across as many PDF pages as needed
    total_pages = 1  # cover counts as 1
    for img_path, label in screenshots:
        img = PILImage.open(img_path)
        img_w, img_h = img.size  # pixels

        # Scale image width to usable PDF width
        scale = USABLE_W / img_w
        scaled_h = img_h * scale  # total image height in points

        # How many PDF pages do we need for this screenshot?
        n_pages = max(1, math.ceil(scaled_h / USABLE_H))

        for page_idx in range(n_pages):
            total_pages += 1
            # Crop the relevant strip from the screenshot
            crop_top_px = int(page_idx * USABLE_H / scale)
            crop_bottom_px = min(int((page_idx + 1) * USABLE_H / scale), img_h)
            strip = img.crop((0, crop_top_px, img_w, crop_bottom_px))

            strip_path = tmp_dir / f"strip_{img_path.stem}_{page_idx}.png"
            strip.save(str(strip_path))

            strip_h_pt = (crop_bottom_px - crop_top_px) * scale

            # Draw on PDF page
            draw_header_footer(c, label, total_pages)
            c.drawImage(
                str(strip_path),
                MARGIN_LR,
                PAGE_H - MARGIN_TOP - strip_h_pt,
                width=USABLE_W,
                height=strip_h_pt,
                preserveAspectRatio=False,
            )
            c.showPage()

            strip_path.unlink()

        img.close()

    c.save()

    # Clean up
    for img_path, _ in screenshots:
        img_path.unlink()
    # Remove any remaining temp files
    for f in tmp_dir.iterdir():
        f.unlink()
    tmp_dir.rmdir()

    print(f"\n  PDF erstellt: {OUTPUT}")
    print(f"  {len(screenshots)} Website-Seiten → {total_pages} PDF-Seiten")


if __name__ == "__main__":
    main()
