"""Generate a PDF of ALL current website pages for SG to review.

Extracts visible text content from each Astro page, organised by page.
Uses the project brand palette (Navy, Gold, Purple, Pearl).
Run: python brand/generate_website_review_pdf.py
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    PageBreak,
    NextPageTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Table,
    TableStyle,
)

# ── Paths ──────────────────────────────────────────────────────────────────
PROJECT = Path(__file__).parent.parent
PAGES_DIR = PROJECT / "website" / "src" / "pages"
OUTPUT = PROJECT / "brand" / "website_review_2026-06-07.pdf"

# ── Brand colours ──────────────────────────────────────────────────────────
NAVY = HexColor("#0E1A3A")
GOLD = HexColor("#B8893A")
VIOLET = HexColor("#4A2C6D")
MUTED = HexColor("#5A5F73")
PEARL = HexColor("#FAF6EF")
LIGHT_GOLD = HexColor("#F5EDE0")

# ── Unicode font (for special chars) ──────────────────────────────────────
_UNICODE_FONT_PATHS = [
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]
UNICODE_FONT = "Helvetica"
for _p in _UNICODE_FONT_PATHS:
    try:
        pdfmetrics.registerFont(TTFont("ArialUnicode", _p))
        UNICODE_FONT = "ArialUnicode"
        break
    except Exception:
        continue


# ── Styles ─────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()
    return {
        "page_title": ParagraphStyle(
            "PageTitle", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=22, leading=26, textColor=NAVY, spaceAfter=4,
        ),
        "page_url": ParagraphStyle(
            "PageURL", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=9, leading=12, textColor=MUTED, spaceAfter=16,
        ),
        "eyebrow": ParagraphStyle(
            "Eyebrow", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=8.5, leading=12, textColor=GOLD, spaceAfter=4,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=18, leading=22, textColor=NAVY, spaceBefore=14, spaceAfter=8,
            keepWithNext=1,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=14, leading=18, textColor=VIOLET, spaceBefore=14, spaceAfter=6,
            keepWithNext=1,
        ),
        "h3": ParagraphStyle(
            "H3", parent=base["Heading3"], fontName="Helvetica-Bold",
            fontSize=11.5, leading=15, textColor=NAVY, spaceBefore=10, spaceAfter=4,
            keepWithNext=1,
        ),
        "h4": ParagraphStyle(
            "H4", parent=base["Heading4"], fontName="Helvetica-Bold",
            fontSize=10, leading=14, textColor=VIOLET, spaceBefore=8, spaceAfter=3,
            keepWithNext=1,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"], fontName="Helvetica",
            fontSize=10.5, leading=15, textColor=colors.black, spaceAfter=6,
            alignment=TA_LEFT,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"], fontName="Helvetica",
            fontSize=10.5, leading=15, textColor=colors.black,
            leftIndent=16, bulletIndent=4, spaceAfter=3,
        ),
        "quote": ParagraphStyle(
            "Quote", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=12, leading=17, textColor=NAVY,
            leftIndent=14, rightIndent=10, spaceBefore=8, spaceAfter=8,
        ),
        "form_label": ParagraphStyle(
            "FormLabel", parent=base["Normal"], fontName="Helvetica",
            fontSize=9, leading=12, textColor=MUTED, spaceAfter=2,
        ),
        "section_label": ParagraphStyle(
            "SectionLabel", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=9, leading=12, textColor=GOLD, spaceBefore=10, spaceAfter=4,
            alignment=TA_LEFT,
        ),
        "cta": ParagraphStyle(
            "CTA", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=10, leading=14, textColor=GOLD, spaceAfter=8,
        ),
        "note": ParagraphStyle(
            "Note", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=9.5, leading=13, textColor=MUTED, spaceAfter=6,
        ),
        "price": ParagraphStyle(
            "Price", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=14, leading=18, textColor=NAVY, spaceAfter=4,
        ),
        "tier_label": ParagraphStyle(
            "TierLabel", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=8.5, leading=12, textColor=GOLD, spaceAfter=2,
        ),
        "toc_entry": ParagraphStyle(
            "TOCEntry", parent=base["Normal"], fontName="Helvetica",
            fontSize=11, leading=18, textColor=NAVY, spaceAfter=2,
            leftIndent=4,
        ),
        "draft_note": ParagraphStyle(
            "DraftNote", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=9, leading=13, textColor=MUTED,
            leftIndent=8, spaceBefore=4, spaceAfter=8,
        ),
    }


# ── Page helpers ───────────────────────────────────────────────────────────
def section_rule():
    return HRFlowable(width="100%", thickness=0.6, color=GOLD,
                      spaceBefore=10, spaceAfter=14)


def thin_rule():
    return HRFlowable(width="100%", thickness=0.3, color=HexColor("#DDDDDD"),
                      spaceBefore=4, spaceAfter=8)


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 12 * mm, "Riviera & Ridge · Website-Texte · Entwurf zur Durchsicht")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Seite {doc.page}")
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.4)
    canvas.line(20 * mm, 15 * mm, A4[0] - 20 * mm, 15 * mm)
    canvas.restoreState()


def on_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(25 * mm, A4[1] - 50 * mm, 30 * mm, 0.8 * mm, fill=1, stroke=0)

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 28)
    canvas.drawString(25 * mm, A4[1] - 68 * mm, "Riviera & Ridge")
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawString(25 * mm, A4[1] - 82 * mm, "Website-Texte zur Durchsicht")
    canvas.setFont("Helvetica", 12)
    canvas.drawString(25 * mm, A4[1] - 96 * mm, "Alle Seiten · Stand 7. Juni 2026")

    canvas.setFillColor(HexColor("#A9B8C9"))
    canvas.setFont("Helvetica-Oblique", 11)
    canvas.drawString(25 * mm, A4[1] - 112 * mm,
                      "Primärsprache: Englisch · Layout-Darstellung ohne Design")

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 11)
    intro = [
        "Liebe Saskia,",
        "",
        "dieses PDF enthält den kompletten Text aller aktuellen Website-Seiten",
        "unter dem Namen Riviera & Ridge. Die Texte sind auf Englisch,",
        "Deutsch und Französisch werden erst übersetzt, wenn die EN-Fassung steht.",
        "",
        "Enthaltene Seiten:",
        "   1.  Home (Startseite)",
        "   2.  About (Über mich)",
        "   3.  Services (Übersicht)",
        "   4.  Active Travel & Alpine (Tier I)",
        "   5.  Behavioral & Harmony Coaching (Tier II)",
        "   6.  Elite Relief & Emergency (Tier III)",
        "   7.  For Agencies (B2B-Seite)",
        "   8.  Contact (Kontaktseite)",
        "   9.  Privacy Policy (Datenschutz)",
        "  10.  Imprint (Impressum)",
        "",
        "Was ich von dir brauche:",
        "   1.  Klingt das nach dir? Wo nicht?",
        "   2.  Stimmen die fachlichen Aussagen?",
        "   3.  Welche Sätze möchtest du auf keinen Fall so stehen lassen?",
        "   4.  Sind die Preise korrekt dargestellt?",
        "   5.  Fehlt etwas Wichtiges?",
    ]
    y = A4[1] - 128 * mm
    for line in intro:
        canvas.drawString(25 * mm, y, line)
        y -= 5.2 * mm

    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(25 * mm, 32 * mm, "Kein Zeitdruck — lies es in Ruhe durch und markiere, was auffällt.")
    canvas.setFillColor(HexColor("#A9B8C9"))
    canvas.setFont("Helvetica-Oblique", 9)
    canvas.drawString(25 * mm, 25 * mm,
                      "Intern · nicht zur Weitergabe an Familien oder Agenturen vor Freigabe.")
    canvas.restoreState()


# ── HTML/Astro text extraction ─────────────────────────────────────────────
def strip_frontmatter(text: str) -> str:
    """Remove Astro frontmatter (--- ... ---)."""
    return re.sub(r'^---.*?---\s*', '', text, count=1, flags=re.DOTALL)


def strip_style_script(text: str) -> str:
    """Remove <style> and <script> blocks."""
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    return text


def strip_comments(text: str) -> str:
    """Remove HTML comments."""
    return re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)


def decode_entities(text: str) -> str:
    """Decode HTML entities."""
    text = text.replace("&amp;", "&")
    text = text.replace("&ldquo;", "\u201c")
    text = text.replace("&rdquo;", "\u201d")
    text = text.replace("&middot;", "\u00b7")
    text = text.replace("&nbsp;", " ")
    text = html.unescape(text)
    return text


def clean_text(text: str) -> str:
    """Collapse whitespace in text."""
    return re.sub(r'\s+', ' ', text).strip()


def extract_sections(raw: str) -> list[dict]:
    """Parse Astro HTML into structured sections for PDF rendering.

    Returns a list of dicts with keys: type, text
    Types: eyebrow, h1, h2, h3, h4, p, li, blockquote, cta, form_field,
           select_option, label, dt, dd, price, tier_label, draft_note,
           section_break, address
    """
    content = strip_frontmatter(raw)
    content = strip_comments(content)
    content = strip_style_script(content)

    sections: list[dict] = []

    # Extract <Image> tags — note them as image references
    for m in re.finditer(r'<Image[^>]*alt="([^"]*)"[^>]*/>', content):
        sections.append({"type": "note", "text": f"[Bild: {m.group(1)}]"})

    # Remove Image tags and other Astro components from further processing
    content = re.sub(r'<Image[^>]*/>', '', content)
    content = re.sub(r'<[A-Z][a-zA-Z]*[^>]*/>', '', content)
    content = re.sub(r'<[A-Z][a-zA-Z]*[^>]*>[^<]*</[A-Z][a-zA-Z]*>', '', content)

    # Reparse line by line to maintain order
    sections.clear()

    # Split into meaningful HTML elements
    tag_pattern = re.compile(
        r'<(h[1-4]|p|li|blockquote|dt|dd|address|label|option|textarea|select|'
        r'input|button|table|thead|tbody|tr|th|td|div|span|a|section|article|aside|'
        r'footer|cite|strong|em|small|ul|ol|form|Image|Nav|Footer|Base|dl)(\s[^>]*)?>'
        r'(.*?)</\1>|'
        r'<(Image|input|br)\s[^>]*/?>',
        re.DOTALL | re.IGNORECASE
    )

    # Simpler approach: use regex to find tagged content in order
    lines = content.split('\n')
    in_commented = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Detect eyebrow divs
        if 'class="eyebrow"' in stripped:
            text = re.sub(r'<[^>]+>', '', stripped)
            text = clean_text(decode_entities(text))
            if text:
                sections.append({"type": "eyebrow", "text": text})
            continue

        # Detect draft notes
        if 'class="draft-note"' in stripped or 'draft-note' in stripped:
            text = re.sub(r'<[^>]+>', '', stripped)
            text = clean_text(decode_entities(text))
            if text:
                sections.append({"type": "draft_note", "text": text})
            continue

        # Tier labels
        if 'class="tier-label"' in stripped or 'class="tier-num"' in stripped:
            text = re.sub(r'<[^>]+>', '', stripped)
            text = clean_text(decode_entities(text))
            if text:
                sections.append({"type": "tier_label", "text": text})
            continue

        # Prices
        if 'class="price"' in stripped:
            text = re.sub(r'<[^>]+>', '', stripped)
            text = clean_text(decode_entities(text))
            if text:
                sections.append({"type": "price", "text": text})
            continue

        # Pillar/step numbers
        if 'class="pillar-num"' in stripped or 'class="step-num"' in stripped:
            text = re.sub(r'<[^>]+>', '', stripped)
            text = clean_text(decode_entities(text))
            if text:
                sections.append({"type": "tier_label", "text": text})
            continue

        # Section comments (═══ markers)
        if stripped.startswith('<!-- ═'):
            text = re.sub(r'<!--\s*═+\s*', '', stripped)
            text = re.sub(r'\s*═+\s*-->', '', text)
            text = text.strip()
            if text:
                sections.append({"type": "section_break", "text": text})
            continue

        # Headings
        for tag_level in ['h1', 'h2', 'h3', 'h4']:
            match = re.search(rf'<{tag_level}[^>]*>(.*?)</{tag_level}>', stripped, re.DOTALL)
            if match:
                text = re.sub(r'<[^>]+>', '', match.group(1))
                text = clean_text(decode_entities(text))
                if text:
                    sections.append({"type": tag_level, "text": text})
                break
        else:
            # Blockquotes
            match = re.search(r'<blockquote[^>]*>(.*?)</blockquote>', stripped, re.DOTALL)
            if match:
                text = re.sub(r'<[^>]+>', '', match.group(1))
                text = clean_text(decode_entities(text))
                if text:
                    sections.append({"type": "blockquote", "text": text})
                continue

            # List items
            match = re.search(r'<li[^>]*>(.*?)</li>', stripped, re.DOTALL)
            if match:
                text = re.sub(r'<[^>]+>', '', match.group(1))
                text = clean_text(decode_entities(text))
                if text:
                    sections.append({"type": "li", "text": text})
                continue

            # Definition terms/descriptions
            match = re.search(r'<dt[^>]*>(.*?)</dt>', stripped, re.DOTALL)
            if match:
                text = re.sub(r'<[^>]+>', '', match.group(1))
                text = clean_text(decode_entities(text))
                if text:
                    sections.append({"type": "dt", "text": text})
                continue
            match = re.search(r'<dd[^>]*>(.*?)</dd>', stripped, re.DOTALL)
            if match:
                text = re.sub(r'<[^>]+>', '', match.group(1))
                text = clean_text(decode_entities(text))
                if text:
                    sections.append({"type": "dd", "text": text})
                continue

            # Form labels
            match = re.search(r'<label[^>]*for="[^"]*"[^>]*>(.*?)</label>', stripped, re.DOTALL)
            if match:
                text = re.sub(r'<[^>]+>', '', match.group(1))
                text = clean_text(decode_entities(text))
                if text and 'Do not fill' not in text:
                    sections.append({"type": "form_field", "text": text})
                continue

            # Select options
            match = re.search(r'<option[^>]*value="[^"]*"[^>]*>(.*?)</option>', stripped, re.DOTALL)
            if match:
                text = clean_text(decode_entities(match.group(1)))
                if text:
                    sections.append({"type": "select_option", "text": f"  → {text}"})
                continue

            # Buttons
            match = re.search(r'<button[^>]*>(.*?)</button>', stripped, re.DOTALL)
            if match:
                text = re.sub(r'<[^>]+>', '', match.group(1))
                text = clean_text(decode_entities(text))
                if text:
                    sections.append({"type": "cta", "text": f"[Button: {text}]"})
                continue

            # CTA links
            if 'class="cta-btn"' in stripped or 'class="hero-cta"' in stripped or \
               'class="contact-cta"' in stripped or 'class="sidebar-cta"' in stripped or \
               'class="track-cta"' in stripped or 'class="submit-btn"' in stripped:
                text = re.sub(r'<[^>]+>', '', stripped)
                text = clean_text(decode_entities(text))
                if text:
                    sections.append({"type": "cta", "text": f"→ {text}"})
                continue

            # More links
            if 'class="more"' in stripped or 'class="card-cta"' in stripped or \
               'class="option-cta"' in stripped:
                text = re.sub(r'<[^>]+>', '', stripped)
                text = clean_text(decode_entities(text))
                if text:
                    sections.append({"type": "cta", "text": text})
                continue

            # Table cells
            match = re.search(r'<t[hd][^>]*>(.*?)</t[hd]>', stripped, re.DOTALL)
            if match:
                text = re.sub(r'<[^>]+>', '', match.group(1))
                text = clean_text(decode_entities(text))
                if text:
                    sections.append({"type": "body" if '<td' in stripped else "h4", "text": text})
                continue

            # Address
            match = re.search(r'<address[^>]*>(.*?)</address>', stripped, re.DOTALL)
            if match:
                text = re.sub(r'<br\s*/?>', '\n', match.group(1))
                text = re.sub(r'<[^>]+>', '', text)
                text = decode_entities(text).strip()
                if text:
                    sections.append({"type": "body", "text": text})
                continue

            # Image references
            match = re.search(r'<Image[^>]*alt="([^"]*)"', stripped)
            if match:
                sections.append({"type": "note", "text": f"[Bild: {match.group(1)}]"})
                continue

            # Paragraphs (catch-all for <p> tags, including multi-line)
            match = re.search(r'<p[^>]*>(.*?)</p>', stripped, re.DOTALL)
            if match:
                text = re.sub(r'<[^>]+>', '', match.group(1))
                text = clean_text(decode_entities(text))
                if text:
                    sections.append({"type": "p", "text": text})
                continue

            # Links with text (standalone)
            match = re.search(r'<a[^>]*>(.*?)</a>', stripped, re.DOTALL)
            if match:
                text = re.sub(r'<[^>]+>', '', match.group(1))
                text = clean_text(decode_entities(text))
                if text and len(text) > 3:
                    sections.append({"type": "cta", "text": text})
                continue

            # Span with text (hero meta etc.)
            match = re.search(r'<span[^>]*>(.*?)</span>', stripped, re.DOTALL)
            if match:
                text = re.sub(r'<[^>]+>', '', match.group(1))
                text = clean_text(decode_entities(text))
                if text and len(text) > 2:
                    sections.append({"type": "body", "text": text})
                continue

    return sections


# ── Deduplication helper ───────────────────────────────────────────────────
def dedupe_sections(sections: list[dict]) -> list[dict]:
    """Remove consecutive duplicate entries."""
    result = []
    for s in sections:
        if result and result[-1]["type"] == s["type"] and result[-1]["text"] == s["text"]:
            continue
        result.append(s)
    return result


# ── Build flowables for one page ───────────────────────────────────────────
def build_page_flowables(
    page_title: str,
    page_url: str,
    raw_content: str,
    styles: dict,
) -> list:
    """Convert one Astro page into a list of ReportLab flowables."""
    elements = []

    # Page title & URL
    elements.append(Paragraph(page_title, styles["page_title"]))
    elements.append(Paragraph(page_url, styles["page_url"]))
    elements.append(section_rule())

    sections = extract_sections(raw_content)
    sections = dedupe_sections(sections)

    for sec in sections:
        t = sec["type"]
        text = sec["text"]

        # Escape ReportLab XML special chars
        safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        if t == "section_break":
            elements.append(Spacer(1, 6))
            elements.append(HRFlowable(width="40%", thickness=0.3, color=GOLD,
                                       spaceBefore=8, spaceAfter=4))
            elements.append(Paragraph(safe.upper(), styles["section_label"]))
        elif t == "eyebrow":
            elements.append(Paragraph(safe, styles["eyebrow"]))
        elif t == "h1":
            elements.append(Paragraph(safe, styles["h1"]))
        elif t == "h2":
            elements.append(Paragraph(safe, styles["h2"]))
        elif t == "h3":
            elements.append(Paragraph(safe, styles["h3"]))
        elif t == "h4":
            elements.append(Paragraph(safe, styles["h4"]))
        elif t == "blockquote":
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(f"\u201c{safe}\u201d", styles["quote"]))
            elements.append(Spacer(1, 4))
        elif t == "li":
            elements.append(Paragraph(f"\u2022  {safe}", styles["bullet"]))
        elif t == "dt":
            elements.append(Paragraph(f"<b>{safe}</b>", styles["body"]))
        elif t == "dd":
            elements.append(Paragraph(f"    {safe}", styles["body"]))
        elif t == "cta":
            elements.append(Paragraph(safe, styles["cta"]))
        elif t == "price":
            elements.append(Paragraph(safe, styles["price"]))
        elif t == "tier_label":
            elements.append(Paragraph(safe, styles["tier_label"]))
        elif t == "form_field":
            elements.append(Paragraph(f"[Feld: {safe}]", styles["form_label"]))
        elif t == "select_option":
            elements.append(Paragraph(safe, styles["form_label"]))
        elif t == "draft_note":
            elements.append(Paragraph(f"\u26a0 {safe}", styles["draft_note"]))
        elif t == "note":
            elements.append(Paragraph(safe, styles["note"]))
        elif t == "p":
            elements.append(Paragraph(safe, styles["body"]))
        else:
            elements.append(Paragraph(safe, styles["body"]))

    return elements


# ── Main ───────────────────────────────────────────────────────────────────
def main():
    styles = build_styles()

    # Define pages in display order
    pages = [
        ("Home (Startseite)", "/", PAGES_DIR / "index.astro"),
        ("About (Über mich)", "/about", PAGES_DIR / "about.astro"),
        ("Services (Übersicht)", "/services", PAGES_DIR / "services" / "index.astro"),
        ("Tier I: Active Travel & Alpine", "/services/travel-alpine",
         PAGES_DIR / "services" / "travel-alpine.astro"),
        ("Tier II: Behavioral & Harmony Coaching", "/services/behavioral-harmony",
         PAGES_DIR / "services" / "behavioral-harmony.astro"),
        ("Tier III: Elite Relief & Emergency", "/services/elite-relief",
         PAGES_DIR / "services" / "elite-relief.astro"),
        ("For Agencies (B2B)", "/agencies", PAGES_DIR / "agencies.astro"),
        ("Contact (Kontakt)", "/contact", PAGES_DIR / "contact.astro"),
        ("Privacy Policy (Datenschutz)", "/privacy", PAGES_DIR / "privacy.astro"),
        ("Imprint (Impressum)", "/imprint", PAGES_DIR / "imprint.astro"),
    ]

    # Build document
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=22 * mm,
        bottomMargin=22 * mm,
        title="Riviera & Ridge — Website-Texte zur Durchsicht",
        author="Felix (für SG)",
    )

    content_frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height,
        id="content",
    )

    cover_frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height,
        id="cover",
    )

    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=on_cover),
        PageTemplate(id="content", frames=[content_frame], onPage=on_page),
    ])

    # Assemble flowables
    story = []

    # Cover page (drawn by on_cover callback)
    story.append(NextPageTemplate("content"))
    story.append(PageBreak())

    # Table of contents
    story.append(Paragraph("Inhaltsverzeichnis", styles["h1"]))
    story.append(Spacer(1, 8))
    for i, (title, url, _) in enumerate(pages, 1):
        story.append(Paragraph(f"{i}. {title}  <i>({url})</i>", styles["toc_entry"]))
    story.append(Spacer(1, 12))
    story.append(thin_rule())
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "\u26a0 Platzhalter in eckigen Klammern [...] werden vor dem Launch "
        "mit echten Daten gefüllt (Adresse, Telefonnummer, UID etc.).",
        styles["note"],
    ))
    story.append(PageBreak())

    # Each page
    for i, (title, url, filepath) in enumerate(pages):
        raw = filepath.read_text(encoding="utf-8")
        flowables = build_page_flowables(
            page_title=f"{i+1}. {title}",
            page_url=f"rivieraandridge.com{url}",
            raw_content=raw,
            styles=styles,
        )
        story.extend(flowables)

        # Page break between pages (not after the last)
        if i < len(pages) - 1:
            story.append(PageBreak())

    # Build PDF
    doc.build(story)
    print(f"PDF erstellt: {OUTPUT}")
    print(f"  {len(pages)} Seiten extrahiert")


if __name__ == "__main__":
    main()
