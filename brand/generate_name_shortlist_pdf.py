"""Generate the Saskia name-shortlist reaction PDF.

Layout:
- Cover (why & how to react).
- For each of 6 directions: a header + intro + table of candidates with
  ❤ / ✓ / ✗ checkbox rows + a one-line comment field.
- Final pages: free space for own ideas + return-info.
"""

from __future__ import annotations

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
    KeepTogether,
    Table,
    TableStyle,
)

# --- Unicode font for ❤ ✓ ✗ ☐ glyphs ---------------------------------------
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


OUTPUT = Path(__file__).parent / "name_shortlist_saskia.pdf"

# Palette B (Royal Care) — decided 2026-04-24
NAVY = HexColor("#0E1A3A")
PURPLE = HexColor("#5E3A8A")  # Royal Purple
PEARL = HexColor("#F4EEDF")  # Pearl
GOLD = HexColor("#B8893A")
MUTED = HexColor("#5A5F73")


# --- Data -----------------------------------------------------------------

DIRECTIONS = [
    {
        "id": 1,
        "title": "Richtung 1 — Atem · Ruhe · Innehalten",
        "intro": "Der tiefe Atemzug als Markenkern. Weich, reduziert, mehrsprachig lesbar.",
        "candidates": [
            ("01", "Atelio", "Klang zwischen „atelier“ und „atem“. Italienisch lesbar."),
            ("02", "Respira", "Italienisch „atme“. Direkt deine Kern-Metapher."),
            ("03", "Quieta", "Lateinisch „die Stille“. Premium-Klang, sehr ruhig."),
            ("04", "Soffio", "Italienisch „Atemhauch“. Leicht — vielleicht zu zart."),
            ("05", "Anima", "Lateinisch „Atem, Seele, Leben“. Wärmer, tiefer."),
        ],
    },
    {
        "id": 2,
        "title": "Richtung 2 — Fels · Erdung · Halt",
        "intro": "Ruhe unter Druck. Antizipation. Das Signal an die Eltern.",
        "candidates": [
            ("06", "Terra Alta", "„Hohe Erde“. Alpin + erdverbunden, ski-welt-anschlussfähig."),
            ("07", "Aequora", "Lateinisch „ruhige See“. Fels-in-der-Brandung eingebaut."),
            ("08", "Saldo", "Italienisch „fest, solide“. Kurz. Risiko: Finanz-Klang."),
            ("09", "Fermo", "Italienisch „fest, ruhig“. Klingt nach Präsenz."),
            ("10", "Grund", "Deutsch, sehr geerdet. Walliser-Nähe. Hart."),
            ("11", "Ankora", "Italienisch „Anker“ mit „ancora“-Doppellesart."),
        ],
    },
    {
        "id": 3,
        "title": "Richtung 3 — Licht · Himmel · Morgen",
        "intro": "Direkt aus deinem Bild vom azurblauen Himmel über Zermatt.",
        "candidates": [
            ("12", "Azura", "Dein eigenes Bild. International, premium, weiblich."),
            ("13", "Chiara", "Italienisch „klar, hell“. Schön — nah an Vornamen."),
            ("14", "Aurelia", "Lateinisch „die Goldene“. Warm, würdevoll."),
            ("15", "Mattina", "Italienisch „Morgen“. Dein 7:38-Uhr-Bild."),
            ("16", "Serena", "Italienisch „heiter, wolkenlos“. Häufig."),
            ("17", "Alba", "„Morgendämmerung“. Kurz, international, ruhig."),
        ],
    },
    {
        "id": 4,
        "title": "Richtung 4 — Obhut · Rahmen · stille Führung",
        "intro": "Die sanfte Autorität. Das Sicherheitsnetz, die Leitplanken.",
        "candidates": [
            ("18", "Custos", "Lateinisch „Hüter:in“. Stark. Eher maskulin."),
            ("19", "Custodia", "Weibliche Form. „Obhut, Hut“."),
            ("20", "Inobia", "Kunstwort („in Obhut“). Markenfähig, erklärungsbedürftig."),
            ("21", "Rahmen", "Deutsch, direkt. Bewusst spröde."),
            ("22", "Aulas", "Lateinisch „geschützter Raum“. Unverbraucht."),
            ("23", "Maeva", "Polynesisch „willkommen“. Warm, weiblich."),
        ],
    },
    {
        "id": 5,
        "title": "Richtung 5 — Ort · Berg · Zermatt dezent",
        "intro": "Lokal verankert, international aussprechbar. Keine Postkarten-Klischees.",
        "candidates": [
            ("24", "Furg", "Vom Furgsattel. Sehr kurz. International holprig."),
            ("25", "Gornera", "Wasserlauf bei Zermatt. Weich, lokal, weiblich."),
            ("26", "Monte Serra", "„Ruhiger Berg“. Klingt nach Residenz."),
            ("27", "Nivea", "„Schneeweiß“ — nur zur Illustration, TM-blockiert."),
            ("28", "Alpina", "Zu generisch. Richtung-Anker, kein Kandidat."),
            ("29", "Matter", "Matterhorn + englisches „to matter“. Clever, riskant."),
            ("30", "Firn", "Sommergletscher-Schnee. Sehr alpin, reduziert."),
        ],
    },
    {
        "id": 6,
        "title": "Richtung 6 — Haltung · mehrsprachig · warm",
        "intro": "Worte aus deinem sprachlichen Kosmos (IT · FR · DE · EN).",
        "candidates": [
            ("31", "Vero", "Italienisch „wahr, echt“. Kurz, premium."),
            ("32", "Con Brio", "„Mit Leben“. Musik-Anleihe. Schwung, nicht laut."),
            ("33", "Chez Nous", "Französisch „bei uns“. Familiär, CH-nah."),
            ("34", "Di Cuore", "Italienisch „von Herzen“ — dein eigenes Wort."),
            ("35", "Cara", "Italienisch „liebe“. Klein, melodisch."),
            ("36", "Dolce", "Italienisch „sanft“. Risiko Niedlich-Falle."),
            ("37", "Presente", "„Anwesend, präsent“. Direkt die Positionierung."),
            ("38", "Suvera", "Kunstwort „sous-vera“ — unter dem Wahren."),
            ("39", "Mare Serena", "„Ruhige See“. Fels-in-der-Brandung-Bild."),
            ("40", "Halt", "Deutsch, ein Wort. Ehrlich, erdig, hart."),
        ],
    },
]


# --- Styles ---------------------------------------------------------------

def build_styles():
    base = getSampleStyleSheet()
    return {
        "h1": ParagraphStyle(
            "H1", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=16, leading=20, textColor=NAVY,
            spaceBefore=6, spaceAfter=4, keepWithNext=1,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=13, leading=17, textColor=PURPLE,
            spaceBefore=14, spaceAfter=4, keepWithNext=1,
        ),
        "intro": ParagraphStyle(
            "Intro", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=10.5, leading=14, textColor=MUTED, spaceAfter=8,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"], fontName="Helvetica",
            fontSize=10.5, leading=15, textColor=colors.black, spaceAfter=6,
        ),
        "num": ParagraphStyle(
            "Num", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=10, leading=13, textColor=MUTED, alignment=TA_CENTER,
        ),
        "name": ParagraphStyle(
            "Name", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=12, leading=15, textColor=NAVY,
        ),
        "why": ParagraphStyle(
            "Why", parent=base["Normal"], fontName="Helvetica",
            fontSize=9.5, leading=12, textColor=MUTED,
        ),
        "box": ParagraphStyle(
            "Box", parent=base["Normal"], fontName=UNICODE_FONT,
            fontSize=14, leading=16, textColor=NAVY, alignment=TA_CENTER,
        ),
        "boxlabel": ParagraphStyle(
            "BoxLabel", parent=base["Normal"], fontName="Helvetica",
            fontSize=7.5, leading=9, textColor=MUTED, alignment=TA_CENTER,
        ),
        "hint": ParagraphStyle(
            "Hint", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=9.5, leading=13, textColor=MUTED, spaceAfter=4,
        ),
    }


def section_divider():
    return HRFlowable(width="100%", thickness=0.5, color=GOLD,
                      spaceBefore=6, spaceAfter=8)


def answer_line():
    return HRFlowable(width="98%", thickness=0.3, color=colors.grey,
                      spaceBefore=4, spaceAfter=16)


# --- Candidate row --------------------------------------------------------

def candidate_row(styles, num, name, why):
    """A single candidate row with three checkboxes + comment line."""
    box = "\u2610"  # ☐

    head_data = [[
        Paragraph(num, styles["num"]),
        Paragraph(name, styles["name"]),
        Paragraph(box, styles["box"]),
        Paragraph(box, styles["box"]),
        Paragraph(box, styles["box"]),
    ]]
    head = Table(
        head_data,
        colWidths=[12 * mm, 92 * mm, 18 * mm, 18 * mm, 18 * mm],
        rowHeights=[9 * mm],
    )
    head.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (2, 0), (4, 0), "CENTER"),
        ("BOX", (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ("BACKGROUND", (0, 0), (0, 0), PEARL),
    ]))

    why_data = [[
        Paragraph("", styles["num"]),
        Paragraph(why, styles["why"]),
        Paragraph("", styles["num"]),
        Paragraph("", styles["num"]),
        Paragraph("", styles["num"]),
    ]]
    labels = Table(
        why_data,
        colWidths=[12 * mm, 92 * mm, 18 * mm, 18 * mm, 18 * mm],
        rowHeights=[7 * mm],
    )
    labels.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (1, 0), (1, 0), 2),
        ("TOPPADDING", (1, 0), (1, 0), 2),
    ]))

    return KeepTogether([head, labels, Spacer(1, 2 * mm)])


# --- Cover ----------------------------------------------------------------

def on_cover(canvas, doc):
    canvas.saveState()
    # Background
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    # Purple band
    canvas.setFillColor(PURPLE)
    canvas.rect(0, A4[1] - 22 * mm, A4[0], 6 * mm, fill=1, stroke=0)
    # Gold accent
    canvas.setFillColor(GOLD)
    canvas.rect(25 * mm, A4[1] - 58 * mm, 30 * mm, 0.8 * mm, fill=1, stroke=0)

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 30)
    canvas.drawString(25 * mm, A4[1] - 75 * mm, "40 Namen")
    canvas.setFont("Helvetica", 16)
    canvas.drawString(25 * mm, A4[1] - 86 * mm, "Deine Reaktion — in fünf Minuten.")

    canvas.setFillColor(HexColor("#C9BEEA"))
    canvas.setFont("Helvetica-Oblique", 11)
    canvas.drawString(25 * mm, A4[1] - 99 * mm, "25. April 2026 · von Felix")

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 11)
    lines = [
        "Liebe Saskia,",
        "",
        "wie besprochen: Hier sind 40 Namenskandidaten in sechs Richtungen.",
        "Viele werden dir nicht gefallen — genau das ist der Punkt.",
        "Ich brauche deine Nein-Reaktionen genauso wie die Ja-Reaktionen.",
        "",
        "So geht’s:",
    ]
    y = A4[1] - 120 * mm
    for line in lines:
        canvas.drawString(25 * mm, y, line)
        y -= 6 * mm

    y -= 2 * mm
    # Instructions with colored marks
    canvas.setFont(UNICODE_FONT, 16)
    canvas.setFillColor(HexColor("#F2A0B8"))
    canvas.drawString(25 * mm, y, "\u2764")
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 11)
    canvas.drawString(34 * mm, y + 1, "ankreuzen, wenn der Name dich warm berührt.")
    y -= 7 * mm
    canvas.setFont(UNICODE_FONT, 16)
    canvas.setFillColor(HexColor("#A8D4BA"))
    canvas.drawString(25 * mm, y, "\u2713")
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 11)
    canvas.drawString(34 * mm, y + 1, "ankreuzen, wenn er interessant ist — „könnte ich mir vorstellen“.")
    y -= 7 * mm
    canvas.setFont(UNICODE_FONT, 16)
    canvas.setFillColor(HexColor("#E0A0A0"))
    canvas.drawString(25 * mm, y, "\u2717")
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 11)
    canvas.drawString(34 * mm, y + 1, "ankreuzen, wenn er weg soll. Ohne Begründung. Bauch reicht.")
    y -= 10 * mm

    canvas.setFont("Helvetica-Oblique", 10.5)
    canvas.setFillColor(HexColor("#C9BEEA"))
    for txt in [
        "Nicht alles kreuzen. Das meiste darf leer bleiben.",
        "Wenn dir ein eigener Name einfällt: ganz hinten ist Platz dafür.",
    ]:
        canvas.drawString(25 * mm, y, txt)
        y -= 6 * mm

    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(25 * mm, 28 * mm, "Richtwert: bis Montagabend, 27. April.")
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 9.5)
    canvas.drawString(25 * mm, 22 * mm, "Rückweg: Foto/Screenshot per WhatsApp oder kurzer Anruf.")

    canvas.restoreState()


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 12 * mm, "[Markenname] · 40 Namen · Reaktion für Saskia")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Seite {doc.page}")
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.4)
    canvas.line(20 * mm, 15 * mm, A4[0] - 20 * mm, 15 * mm)
    canvas.restoreState()


# --- Story ----------------------------------------------------------------

def column_header(styles):
    """Row with column labels for the checkbox columns."""
    uf = UNICODE_FONT
    data = [[
        Paragraph("Nr.", styles["hint"]),
        Paragraph("Name &nbsp;·&nbsp; Warum dieser Name in der Liste ist", styles["hint"]),
        Paragraph(f'<font name="{uf}">\u2764</font> warm', styles["hint"]),
        Paragraph(f'<font name="{uf}">\u2713</font> ok', styles["hint"]),
        Paragraph(f'<font name="{uf}">\u2717</font> weg', styles["hint"]),
    ]]
    t = Table(
        data,
        colWidths=[12 * mm, 92 * mm, 18 * mm, 18 * mm, 18 * mm],
        rowHeights=[6 * mm],
    )
    t.setStyle(TableStyle([
        ("ALIGN", (2, 0), (4, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (2, 0), (4, 0), UNICODE_FONT),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, GOLD),
    ]))
    return t


def build_story(styles):
    story = []

    story.append(Paragraph("Was du hier siehst", styles["h1"]))
    story.append(Paragraph(
        "Sechs Richtungen. Jede Richtung trägt eine andere Stimmung der Marke — Atem, Fels, Licht, "
        "Obhut, Berg, Haltung. Innerhalb jeder Richtung stehen zwischen fünf und zehn Namen. "
        "Neben jedem Namen steht eine Mini-Begründung, damit du weißt, warum er auf der Liste steht. "
        "Die Begründung ist kein Verkauf — nur Kontext.",
        styles["body"]))
    story.append(Paragraph(
        "Du musst nichts davon begründen. Ein Kreuz reicht. Wenn dir ein Wort einfällt, "
        "das sofort einen Namen auslöst — die Kommentarzeile unter jeder Richtung ist dafür da.",
        styles["body"]))
    story.append(section_divider())

    for d in DIRECTIONS:
        story.append(Paragraph(d["title"], styles["h2"]))
        story.append(Paragraph(d["intro"], styles["intro"]))
        story.append(column_header(styles))
        for num, name, why in d["candidates"]:
            story.append(candidate_row(styles, num, name, why))

        # comment line per direction
        story.append(Paragraph(
            "Kommentar zu dieser Richtung (optional): was hat dich berührt, was fehlt?",
            styles["hint"]))
        story.append(answer_line())
        story.append(answer_line())

    # Own ideas page
    story.append(PageBreak())
    story.append(Paragraph("Deine eigenen Ideen", styles["h1"]))
    story.append(Paragraph(
        "Wenn dir beim Lesen Wörter, Klänge oder Bilder gekommen sind — schreib sie hierher. "
        "Auch halbe Ideen, Fragmente, fremdsprachige Wörter. Alles erlaubt.",
        styles["intro"]))
    for _ in range(10):
        story.append(answer_line())

    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("Rückweg", styles["h1"]))
    story.append(Paragraph(
        "Foto oder Screenshot der ausgefüllten Seiten per WhatsApp. "
        "Alternativ kurzer Anruf und wir gehen es durch. "
        "Danach filtere ich auf acht bis zwölf Namen, prüfe Domains und Trademarks, "
        "und wir sprechen am Montagabend über die Finalisten.",
        styles["body"]))

    return story


def main() -> None:
    styles = build_styles()
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=22 * mm,
        title="40 Namen · Reaktion für Saskia",
        author="SG_Content_Projekt",
    )
    frame_content = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height, id="content",
    )
    cover_frame = Frame(
        0, 0, A4[0], A4[1], id="cover",
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=on_cover),
        PageTemplate(id="content", frames=[frame_content], onPage=on_page),
    ])

    story = [NextPageTemplate("content"), PageBreak()]
    story.extend(build_story(styles))
    doc.build(story)
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
