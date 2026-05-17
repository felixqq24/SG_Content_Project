"""Generate a shareable PDF with the three colour palette proposals for SG."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


OUTPUT = Path(__file__).parent / "palette_proposals.pdf"

PALETTES = [
    {
        "key": "A",
        "name": "Midnight Governess",
        "tagline": "Dunkelblau dominant · Gold streng als Akzent",
        "description": (
            "Ruhig, vertrauensbildend, diskret-luxuriös. Dunkelblau trägt die Marke, "
            "Violett/Purpur erscheinen nur subtil, Gold bleibt konsequent Akzent. "
            "Safe-Premium-Option für HNW-Familien und Agenturen."
        ),
        "swatches": [
            ("Primary", "Midnight Navy", "#0E1A3A"),
            ("Secondary", "Deep Indigo", "#2A2A5C"),
            ("Accent", "Antique Gold", "#B8893A"),
            ("Accent 2", "Muted Violet", "#6B4E8E"),
            ("Background", "Warm Ivory", "#F6F1E8"),
            ("Surface", "Soft Cream", "#FBF7EF"),
            ("Text", "Ink Navy", "#0E1A3A"),
            ("Text Muted", "Slate", "#5A5F73"),
        ],
        "notes": [
            "Midnight Navy auf Warm Ivory: ~15.8:1 (WCAG AAA).",
            "Antique Gold: nur Linien / Icons / grosse Buttons - kein Text.",
            "Slate auf Warm Ivory: ~5.6:1 (AA).",
        ],
    },
    {
        "key": "B",
        "name": "Royal Care",
        "tagline": "Purpur + Dunkelblau paritätisch · Gold sichtbar",
        "description": (
            "SGs Input am direktesten umgesetzt: Purpur und Dunkelblau teilen sich die "
            "Hauptrolle, Gold bleibt Akzent. Königlich-luxuriös. Risiko: Boutique-Hotel-"
            "Look - muss durch Bildsprache (echte Kinder, Naturlicht) geerdet werden."
        ),
        "swatches": [
            ("Primary", "Royal Purple", "#4A2C6D"),
            ("Secondary", "Deep Night", "#1C2548"),
            ("Accent", "Soft Gold", "#C9A24B"),
            ("Accent 2", "Plum Violet", "#7A4E9E"),
            ("Background", "Pearl", "#FAF6EF"),
            ("Surface", "Lavender Mist", "#EFE9F2"),
            ("Text", "Near-Black Plum", "#1A1426"),
            ("Text Muted", "Dust Violet", "#5E5470"),
        ],
        "notes": [
            "Royal Purple auf Pearl: ~10.4:1 (AAA).",
            "Soft Gold: ausschliesslich dekorativ, niemals Text.",
            "Deep Night auf Lavender Mist: ~12.1:1 (AAA).",
        ],
    },
    {
        "key": "C",
        "name": "Alpine Velvet",
        "tagline": "Dunkelblau + Violett · warmer Sandton · Gold-Akzent",
        "description": (
            "Hybrid aus Premium und Alpenlicht. Dunkelblau als Anker, Violett als zweiter "
            "Leitton, warmes Sandbeige bringt Wärme (Natur, Ski, Outdoor-Resilienz). "
            "Empfohlen, wenn die Zermatt/Nature-Facette sichtbar bleiben soll."
        ),
        "swatches": [
            ("Primary", "Alpine Blue", "#19325E"),
            ("Secondary", "Velvet Violet", "#5B3A7A"),
            ("Accent", "Warm Gold", "#BE9147"),
            ("Accent 2", "Glacier", "#A9B8C9"),
            ("Background", "Sand Linen", "#F2EADB"),
            ("Surface", "Off-White", "#FBF8F1"),
            ("Text", "Alpine Blue", "#19325E"),
            ("Text Muted", "Stone", "#5F5A4E"),
        ],
        "notes": [
            "Alpine Blue auf Sand Linen: ~10.9:1 (AAA).",
            "Velvet Violet auf Off-White: ~8.4:1 (AAA) - auch für Text nutzbar.",
            "Warm Gold: nur Non-Text. Stone auf Sand Linen: ~5.1:1 (AA).",
        ],
    },
]


def relative_luminance(hex_color: str) -> float:
    """Return WCAG relative luminance for a hex colour."""
    r = int(hex_color[1:3], 16) / 255
    g = int(hex_color[3:5], 16) / 255
    b = int(hex_color[5:7], 16) / 255

    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def readable_text_colour(hex_color: str):
    """Return black or white depending on background luminance."""
    return black if relative_luminance(hex_color) > 0.45 else white


def draw_cover(c: canvas.Canvas) -> None:
    width, height = A4
    c.setFillColor(HexColor("#0E1A3A"))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    c.setFillColor(HexColor("#B8893A"))
    c.rect(25 * mm, height - 40 * mm, 30 * mm, 0.6 * mm, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(25 * mm, height - 55 * mm, "[Markenname]")
    c.setFont("Helvetica", 14)
    c.drawString(25 * mm, height - 65 * mm, "Farbpaletten - drei Richtungen zur Auswahl")

    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor("#A9B8C9"))
    c.drawString(25 * mm, height - 80 * mm, "Ausgangsmaterial: Violett · Purpur · Gold · Dunkelblau")
    c.drawString(25 * mm, height - 86 * mm, "Entwurf V1 · 23. April 2026")

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(25 * mm, height - 110 * mm, "So liest sich dieses Dokument")
    c.setFont("Helvetica", 10.5)
    intro = [
        "Drei Palettenrichtungen, jeweils auf einer Seite.",
        "Jede Palette zeigt: Farbfelder mit HEX, Rollen, Wirkung,",
        "Kontrast-Hinweise und eine kleine Mock-Anwendung (Hero + Button).",
        "",
        "Alle Kontrastwerte sind Richtwerte nach WCAG 2.1.",
        "Vor finalem Launch: mit Stark / WebAIM gegen die finale Typografie nachmessen.",
    ]
    y = height - 120 * mm
    for line in intro:
        c.drawString(25 * mm, y, line)
        y -= 5.5 * mm

    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(HexColor("#A9B8C9"))
    c.drawString(25 * mm, 20 * mm, "Intern · nicht zur Weitergabe an Agenturen vor Freigabe durch SG.")

    c.showPage()


def draw_swatch_grid(c: canvas.Canvas, x: float, y: float, w: float, h: float, swatches) -> None:
    cols = 4
    rows = 2
    cell_w = w / cols
    cell_h = h / rows
    for idx, (role, name, hex_code) in enumerate(swatches):
        col = idx % cols
        row = idx // cols
        cx = x + col * cell_w
        cy = y + h - (row + 1) * cell_h
        c.setFillColor(HexColor(hex_code))
        c.rect(cx, cy, cell_w - 2 * mm, cell_h - 2 * mm, fill=1, stroke=0)

        text_col = readable_text_colour(hex_code)
        c.setFillColor(text_col)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(cx + 3 * mm, cy + cell_h - 7 * mm, role.upper())
        c.setFont("Helvetica", 9)
        c.drawString(cx + 3 * mm, cy + cell_h - 12 * mm, name)
        c.setFont("Helvetica", 8)
        c.drawString(cx + 3 * mm, cy + 4 * mm, hex_code)


def draw_mock(c: canvas.Canvas, x: float, y: float, w: float, h: float, palette) -> None:
    swatches = {s[0]: s[2] for s in palette["swatches"]}
    bg = swatches.get("Background", "#FFFFFF")
    primary = swatches.get("Primary", "#000000")
    accent = swatches.get("Accent", "#000000")
    text = swatches.get("Text", "#000000")
    muted = swatches.get("Text Muted", "#555555")

    c.setFillColor(HexColor(bg))
    c.rect(x, y, w, h, fill=1, stroke=0)

    # Accent hairline
    c.setFillColor(HexColor(accent))
    c.rect(x + 8 * mm, y + h - 14 * mm, 20 * mm, 0.5 * mm, fill=1, stroke=0)

    # Headline
    c.setFillColor(HexColor(text))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x + 8 * mm, y + h - 24 * mm, "Presence over performance.")
    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor(muted))
    c.drawString(x + 8 * mm, y + h - 31 * mm, "Fachlich fundierte Nanny-Begleitung fuer Familien, die Ruhe suchen.")

    # Primary button
    btn_w, btn_h = 36 * mm, 9 * mm
    c.setFillColor(HexColor(primary))
    c.rect(x + 8 * mm, y + 10 * mm, btn_w, btn_h, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 11 * mm, y + 14 * mm, "Gespräch anfragen")

    # Ghost card
    c.setFillColor(HexColor(swatches.get("Surface", bg)))
    c.rect(x + w - 50 * mm, y + 10 * mm, 42 * mm, h - 45 * mm, fill=1, stroke=0)
    c.setFillColor(HexColor(text))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + w - 47 * mm, y + h - 42 * mm, "Qualifikationen")
    c.setFillColor(HexColor(muted))
    c.setFont("Helvetica", 8.5)
    for i, line in enumerate([
        "Staatl. gepr. Erzieherin",
        "Yoga- & Skilehrerin",
        "Soziale Arbeit (Elementar)",
    ]):
        c.drawString(x + w - 47 * mm, y + h - 50 * mm - i * 5 * mm, "- " + line)


def draw_palette_page(c: canvas.Canvas, palette) -> None:
    width, height = A4
    margin = 18 * mm

    # Header bar in primary colour
    primary = palette["swatches"][0][2]
    c.setFillColor(HexColor(primary))
    c.rect(0, height - 38 * mm, width, 38 * mm, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(margin, height - 22 * mm, f"Palette {palette['key']} · {palette['name']}")
    c.setFont("Helvetica", 11)
    c.drawString(margin, height - 30 * mm, palette["tagline"])

    # Description
    c.setFillColor(black)
    c.setFont("Helvetica", 10)
    text_obj = c.beginText(margin, height - 48 * mm)
    text_obj.setLeading(14)
    # wrap
    import textwrap
    for line in textwrap.wrap(palette["description"], width=95):
        text_obj.textLine(line)
    c.drawText(text_obj)

    # Swatch grid
    grid_y = height - 120 * mm
    grid_h = 60 * mm
    draw_swatch_grid(c, margin, grid_y, width - 2 * margin, grid_h, palette["swatches"])

    # Mock
    mock_y = 50 * mm
    mock_h = 55 * mm
    c.setFillColor(HexColor("#CCCCCC"))
    c.rect(margin - 0.3 * mm, mock_y - 0.3 * mm, width - 2 * margin + 0.6 * mm, mock_h + 0.6 * mm, fill=0, stroke=1)
    draw_mock(c, margin, mock_y, width - 2 * margin, mock_h, palette)

    # Notes
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, 38 * mm, "Kontrast & Einsatz")
    c.setFont("Helvetica", 9.5)
    y = 32 * mm
    for note in palette["notes"]:
        c.drawString(margin, y, "· " + note)
        y -= 5 * mm

    # Footer
    c.setFillColor(HexColor("#888888"))
    c.setFont("Helvetica", 8)
    c.drawString(margin, 10 * mm, "[Markenname] · Farbpaletten V1 · 23. April 2026")
    c.drawRightString(width - margin, 10 * mm, f"Seite {palette['key']}")

    c.showPage()


def draw_comparison(c: canvas.Canvas) -> None:
    width, height = A4
    margin = 18 * mm

    c.setFillColor(HexColor("#0E1A3A"))
    c.rect(0, height - 30 * mm, width, 30 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(margin, height - 20 * mm, "Vergleich & Empfehlung")

    c.setFillColor(black)
    headers = ["Kriterium", "A · Midnight", "B · Royal Care", "C · Alpine Velvet"]
    rows = [
        ["Dominanz", "Dunkelblau", "Purpur + Blau", "Blau + Violett"],
        ["Gold-Einsatz", "streng Akzent", "sichtbarer Akzent", "warmer Akzent"],
        ["Wirkung", "diskret-luxuriös", "königlich, opulent", "alpin-premium, warm"],
        ["Risiko", "zu zurückhaltend", "Kitsch-Risiko", "komplexer zu orchestrieren"],
        ["Zielgruppe", "HNW + Agenturen", "HNW / Concierge", "HNW + Ski Zermatt"],
        ["Global-Governess-Fit", "★★★★★", "★★★★☆", "★★★★☆"],
        ["Nahbarkeit / Wärme", "★★★☆☆", "★★☆☆☆", "★★★★☆"],
        ["Umsetzungs-Safety", "★★★★★", "★★★☆☆", "★★★★☆"],
    ]

    col_x = [margin, margin + 55 * mm, margin + 100 * mm, margin + 140 * mm]
    y = height - 42 * mm
    c.setFont("Helvetica-Bold", 10)
    for i, h in enumerate(headers):
        c.drawString(col_x[i], y, h)
    c.setFillColor(HexColor("#B8893A"))
    c.rect(margin, y - 2 * mm, width - 2 * margin, 0.4 * mm, fill=1, stroke=0)
    c.setFillColor(black)

    c.setFont("Helvetica", 9.5)
    y -= 8 * mm
    for row in rows:
        for i, cell in enumerate(row):
            c.drawString(col_x[i], y, cell)
        y -= 7 * mm

    # Empfehlung
    y -= 4 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Empfehlung")
    y -= 7 * mm
    c.setFont("Helvetica", 10)
    recs = [
        "- Schnell & sicher: Palette A (Midnight Governess).",
        "- Wenn Violett/Purpur sichtbar bleiben soll: Palette C (Alpine Velvet).",
        "- Palette B nur mit starker, geerdeter Bildsprache (echte Familien, Naturlicht).",
    ]
    for r in recs:
        c.drawString(margin, y, r)
        y -= 6 * mm

    # Nächste Schritte
    y -= 4 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Nächste Schritte")
    y -= 7 * mm
    c.setFont("Helvetica", 10)
    steps = [
        "1. SG wählt eine Richtung (oder mischt, z. B. 'A, aber Violett präsenter wie in C').",
        "2. Echte Mock-Screens (Hero + Service-Karte) rendern.",
        "3. WCAG-Kontraste gegen finale Typografie nachmessen.",
        "4. Finalisieren in brand/visual.md.",
    ]
    for s in steps:
        c.drawString(margin, y, s)
        y -= 6 * mm

    c.setFillColor(HexColor("#888888"))
    c.setFont("Helvetica", 8)
    c.drawString(margin, 10 * mm, "[Markenname] · Farbpaletten V1 · 23. April 2026")


def main() -> None:
    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    c.setTitle("Farbpaletten - [Markenname]")
    c.setAuthor("SG_Content_Projekt")
    draw_cover(c)
    for palette in PALETTES:
        draw_palette_page(c, palette)
    draw_comparison(c)
    c.save()
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
