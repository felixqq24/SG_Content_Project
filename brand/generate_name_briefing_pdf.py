"""Generate a PDF of the Saskia name-briefing document."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
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
)

# Register a Unicode-capable font for characters Helvetica does not ship
# (checkboxes, radio circles, etc.).
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


OUTPUT = Path(__file__).parent / "name_briefing_saskia.pdf"

NAVY = HexColor("#0E1A3A")
GOLD = HexColor("#B8893A")
VIOLET = HexColor("#6B4E8E")
MUTED = HexColor("#5A5F73")
IVORY = HexColor("#F6F1E8")


def build_styles():
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "Title", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=22, leading=26, textColor=NAVY, spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=11, leading=15, textColor=MUTED, spaceAfter=14,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=15, leading=20, textColor=NAVY, spaceBefore=14, spaceAfter=6,
            keepWithNext=1,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=12, leading=16, textColor=VIOLET, spaceBefore=10, spaceAfter=4,
            keepWithNext=1,
        ),
        "h3": ParagraphStyle(
            "H3", parent=base["Heading3"], fontName="Helvetica-Bold",
            fontSize=10.5, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=2,
            keepWithNext=1,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"], fontName="Helvetica",
            fontSize=10.5, leading=15, textColor=colors.black, spaceAfter=6,
            alignment=TA_LEFT,
        ),
        "checkbox": ParagraphStyle(
            "Checkbox", parent=base["Normal"], fontName=UNICODE_FONT,
            fontSize=11, leading=18, textColor=colors.black, spaceAfter=4,
            alignment=TA_LEFT,
        ),
        "hint": ParagraphStyle(
            "Hint", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=9.5, leading=13, textColor=MUTED, spaceAfter=6,
        ),
        "quote": ParagraphStyle(
            "Quote", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=10.5, leading=15, textColor=NAVY,
            leftIndent=12, rightIndent=8, spaceBefore=4, spaceAfter=10,
            borderColor=GOLD, borderWidth=0, borderPadding=0,
        ),
        "answer": ParagraphStyle(
            "Answer", parent=base["Normal"], fontName="Helvetica",
            fontSize=10.5, leading=22, textColor=colors.grey, spaceAfter=2,
            leftIndent=6,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"], fontName="Helvetica",
            fontSize=10.5, leading=15, textColor=colors.black, spaceAfter=3,
            leftIndent=14, bulletIndent=2,
        ),
        "footer": ParagraphStyle(
            "Footer", parent=base["Normal"], fontName="Helvetica",
            fontSize=8, textColor=MUTED,
        ),
    }
    return styles


def answer_line():
    """Return a horizontal line for handwritten answers."""
    return HRFlowable(width="95%", thickness=0.4, color=colors.grey,
                      spaceBefore=6, spaceAfter=10)


def section_divider():
    return HRFlowable(width="100%", thickness=0.6, color=GOLD,
                      spaceBefore=8, spaceAfter=12)


def on_page(canvas, doc):
    canvas.saveState()
    # Footer
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 12 * mm, "[Markenname] · Namensfindung · Denkhilfe für Saskia")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Seite {doc.page}")
    # thin gold rule
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.4)
    canvas.line(20 * mm, 15 * mm, A4[0] - 20 * mm, 15 * mm)
    canvas.restoreState()


def on_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    # Gold accent
    canvas.setFillColor(GOLD)
    canvas.rect(25 * mm, A4[1] - 50 * mm, 30 * mm, 0.8 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 32)
    canvas.drawString(25 * mm, A4[1] - 68 * mm, "Dein Markenname")
    canvas.setFont("Helvetica", 14)
    canvas.drawString(25 * mm, A4[1] - 80 * mm, "Eine Denkhilfe für dich, Saskia")

    canvas.setFillColor(HexColor("#A9B8C9"))
    canvas.setFont("Helvetica-Oblique", 11)
    canvas.drawString(25 * mm, A4[1] - 95 * mm, "23. April 2026 · von Felix")

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 11)
    intro_lines = [
        "Liebe Saskia,",
        "",
        "das hier ist kein fertiger Vorschlag und auch keine Checkliste,",
        "die du abarbeiten musst. Es ist ein Werkzeug, damit du dich in Ruhe",
        "deinem eigenen Markennamen nähern kannst.",
        "",
        "Nimm dir eine halbe Stunde, einen Kaffee, einen Stift — oder tipp direkt hinein.",
        "Nichts hier ist schon beantwortet, alles darf sich noch ändern.",
        "",
        "Wir suchen keinen perfekten Namen.",
        "Wir suchen einen, mit dem du gerne am Telefon rangehst.",
        "",
        "Wenn du fertig bist (oder steckenbleibst): schick mir das Dokument",
        "zurück oder ruf an. Aus dem, was du aufschreibst, leiten wir dann",
        "gemeinsam eine Shortlist ab.",
    ]
    y = A4[1] - 120 * mm
    for line in intro_lines:
        canvas.drawString(25 * mm, y, line)
        y -= 6 * mm

    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(25 * mm, 30 * mm, "Kein Zeitdruck. Richtwert: bis Ende der Woche, wenn es leicht geht.")

    canvas.restoreState()


def build_story(styles):
    story = []

    # Why this step
    story.append(Paragraph("Warum dieser Schritt wichtig ist", styles["h1"]))
    story.append(Paragraph(
        "Der Markenname blockiert gerade mehrere Dinge: Domain, E-Mail, Visitenkarten, "
        "Social-Profile, die Startseite. Wenn er steht, fällt vieles zügig. Wichtiger aber: "
        "<b>Der Name ist die erste Entscheidung, die wirklich nach dir klingt.</b> "
        "Er entscheidet, ob eine Familie in Dubai oder in Zürich beim ersten Googeln "
        "das Gefühl hat „das passt“ — noch bevor sie einen Text liest.",
        styles["body"]))
    story.append(section_divider())

    # Teil 1
    story.append(Paragraph("Teil 1 — Das Gefühl vor dem Wort", styles["h1"]))
    story.append(Paragraph(
        "Bitte zuerst dieser Teil. Nicht in Namen denken. In Bildern und Wörtern, die kein Name sein müssen.",
        styles["hint"]))

    q11 = [
        ("1.1 Wenn die Marke ein Raum wäre — wie fühlt es sich darin an?",
         "Drei Wörter. Die ersten, die kommen."),
        ("1.2 Welche drei Worte sollen im Kopf einer Mutter hängenbleiben, die deinen Namen zum ersten Mal hört?",
         None),
        ("1.3 Welche drei Worte sollen nicht hängenbleiben?",
         "z. B. „niedlich“, „günstig“, „Kita“, „Au-pair“ — alles erlaubt"),
    ]
    for q, hint in q11:
        story.append(Paragraph(q, styles["h3"]))
        if hint:
            story.append(Paragraph(hint, styles["hint"]))
        for _ in range(3):
            story.append(answer_line())

    story.append(Paragraph(
        "1.4 Nenn eine Marke (Hotel, Label, Manufaktur, Ausrüster), "
        "bei der du denkst: „So würde ich mich anfühlen wollen.“ — und warum in einem Satz.",
        styles["h3"]))
    for _ in range(2):
        story.append(answer_line())

    story.append(Paragraph("1.5 Nenn eine Marke, die du bewusst nicht sein willst.", styles["h3"]))
    for _ in range(2):
        story.append(answer_line())

    story.append(PageBreak())

    # Teil 2
    story.append(Paragraph("Teil 2 — Was der Name leisten muss", styles["h1"]))
    story.append(Paragraph("Kurze Ja/Nein- oder Skalen-Fragen. Schnell, aus dem Bauch.", styles["hint"]))

    story.append(Paragraph("2.1 Soll der Name …", styles["h2"]))
    checkboxes = [
        "… deinen eigenen Namen enthalten (z. B. „Saskia Gertz Nannying“)?     ☐ Ja    ☐ Nein    ☐ Vielleicht",
        "… ein englisches Wort sein?     ☐ Ja    ☐ Nein    ☐ Egal",
        "… ein deutsches Wort sein?     ☐ Ja    ☐ Nein    ☐ Egal",
        "… ein erfundenes Kunstwort sein dürfen (wie „Spotify“)?     ☐ Ja    ☐ Nein",
        "… einen Ortsbezug haben (Zermatt, Alpen, Berg)?     ☐ Ja    ☐ Nein    ☐ Dezent ok",
        "… das Wort „Nanny“ enthalten?     ☐ Ja    ☐ Nein",
        "… das Wort „Care“ enthalten?     ☐ Ja    ☐ Nein",
    ]
    for line in checkboxes:
        story.append(Paragraph(line, styles["checkbox"]))

    for title, lo, hi in [
        ("2.2 Premium-Skala — wie laut darf der Name „Premium“ sagen?",
         "1 = fast unsichtbar", "5 = klar luxuriös"),
        ("2.3 Wärme-Skala — wie warm darf der Name klingen?",
         "1 = kühl-professionell", "5 = sehr herzlich"),
        ("2.4 International-Skala — wie wichtig ist dir, dass der Name sofort international funktioniert?",
         "1 = DACH reicht", "5 = muss global funktionieren"),
    ]:
        story.append(Paragraph(title, styles["h3"]))
        story.append(Paragraph(
            f"{lo} &nbsp;&nbsp; ☐ 1 &nbsp;&nbsp; ☐ 2 &nbsp;&nbsp; ☐ 3 &nbsp;&nbsp; ☐ 4 &nbsp;&nbsp; ☐ 5 &nbsp;&nbsp; {hi}",
            styles["checkbox"]))

    story.append(PageBreak())

    # Teil 3
    story.append(Paragraph("Teil 3 — Sprachliche Anker (freies Assoziieren)", styles["h1"]))
    story.append(Paragraph(
        "Keine Namen. Nur Wörter, die du magst. In jeder Sprache, die dir liegt.",
        styles["hint"]))

    anchors = [
        ("3.1 Berg, Natur, Stille, Licht", "z. B. „Lichtung“, „Firn“, „Halt“, „Horizon“"),
        ("3.2 Ruhe, Atem, Präsenz", None),
        ("3.3 Führung, Rahmen, Vertrauen", "z. B. „Kompass“, „Anker“, „Lotse“, „Walser“"),
        ("3.4 Familie, Kind, Menschsein — ohne Klischee",
         "Bewusst nicht „Baby“, „Kleinkind“, „süß“. Haltungsbegriffe."),
        ("3.5 Wörter aus einer Sprache, die du liebst",
         "Italienisch, Französisch, Lateinisch, Walliserdeutsch, Schwyzerdütsch — alles willkommen."),
    ]
    for q, hint in anchors:
        story.append(Paragraph(q, styles["h3"]))
        if hint:
            story.append(Paragraph(hint, styles["hint"]))
        for _ in range(3):
            story.append(answer_line())

    story.append(PageBreak())

    # Teil 4
    story.append(Paragraph("Teil 4 — Dreimal „wenn“", styles["h1"]))
    story.append(Paragraph("Je ein Satz. Bauchentscheidung.", styles["hint"]))

    for q in [
        "4.1 Wenn die Marke ein Mensch wäre, dann …",
        "4.2 Wenn die Marke eine Uhrzeit wäre, dann …",
        "4.3 Wenn die Marke ein Ort in Zermatt oder in den Bergen wäre, dann …",
    ]:
        story.append(Paragraph(q, styles["h3"]))
        for _ in range(2):
            story.append(answer_line())

    # Teil 5
    story.append(Paragraph("Teil 5 — Erste eigene Kandidaten (optional)", styles["h1"]))
    story.append(Paragraph(
        "Nur wenn dir schon etwas einfällt. Kein Zwang. Wirklich kein Zwang. "
        "Auch halbfertige, auch blöde, auch welche, bei denen du dich schämst. "
        "Schlechte Ideen sind wichtig — sie zeigen, in welche Richtung du denkst.",
        styles["hint"]))

    for i in range(1, 9):
        story.append(Paragraph(f"{i}.", styles["body"]))
        story.append(answer_line())

    story.append(Paragraph(
        "Bei welchem dieser Namen hast du ein leises „ja“ im Bauch — "
        "auch wenn du nicht weißt, warum?",
        styles["h3"]))
    for _ in range(2):
        story.append(answer_line())

    story.append(PageBreak())

    # Teil 6
    story.append(Paragraph("Teil 6 — Harte Ausschlüsse", styles["h1"]))
    story.append(Paragraph(
        "Was darf der Name auf keinen Fall tun, klingen oder enthalten?",
        styles["body"]))
    story.append(Paragraph(
        "Beispiele, nur zur Anregung: „kein Name mit Umlaut“, "
        "„nicht nach Hundeschule klingen“, „keine Wellness-Anmutung“, "
        "„nicht wie eine Agentur“ …",
        styles["hint"]))
    for _ in range(5):
        story.append(answer_line())

    # Teil 7
    story.append(Paragraph("Teil 7 — Was der Rahmen sagt (zum Hintergrund)", styles["h1"]))
    story.append(Paragraph(
        "Das sind die Randbedingungen aus dem, was wir bisher entschieden haben. "
        "Keine Fragen, nur Kontext:",
        styles["hint"]))

    rahmen = [
        "<b>Marke soll eigenständig sein</b> — nicht „Saskia Gertz | …“. Damit perspektivisch auch andere qualifizierte Nannys unter der Marke arbeiten können.",
        "<b>Domain-Wunsch:</b> .com oder .ch frei.",
        "<b>Primärsprache der Website:</b> Englisch. DE + FR übersetzt.",
        "<b>Aussprache</b> muss für Concierges, Agenturen, Familien am Telefon leicht sein — kein Buchstabieren nötig.",
        "<b>Zielgruppe:</b> international mobile Familien, Agenturen wie Duke &amp; Duchess oder Morgan &amp; Mallet.",
        "<b>Was wir vermeiden:</b> Diagnose-Labels („Autism-Nanny“), Niedlich-Vokabular („Little Stars“, „Kids“, „Tiny“), Coaching-Sprech („Journey“, „Mindful“).",
        "<b>Was erlaubt ist:</b> ruhige Premium-Anmutung, Bergbezug dezent, internationaler Klang.",
    ]
    for r in rahmen:
        story.append(Paragraph("• " + r, styles["bullet"]))

    story.append(PageBreak())

    # Teil 8
    story.append(Paragraph("Teil 8 — Wie es weitergeht", styles["h1"]))
    story.append(Paragraph(
        "Wenn du mir dieses Dokument zurückgibst, mache ich Folgendes:",
        styles["body"]))
    steps = [
        "Ich lese deine Worte und leite daraus <b>30–50 Namenskandidaten</b> ab — breit, unzensiert.",
        "Wir filtern gemeinsam auf <b>8–12</b>, die du magst.",
        "Ich prüfe Domain, Social-Handles und Trademarks für diese 8–12.",
        "Übrig bleiben <b>2–3 echte Finalisten</b>, aus denen du wählst.",
        "Domain wird noch am selben Tag gebucht.",
    ]
    for i, s in enumerate(steps, 1):
        story.append(Paragraph(f"{i}. {s}", styles["body"]))

    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        "Du musst in diesem Dokument <b>keinen Namen finden</b>. "
        "Du musst mir nur zeigen, <b>wie sich die Marke für dich anfühlen soll</b>. "
        "Den Namen finden wir dann zu zweit.",
        styles["quote"]))

    story.append(section_divider())
    story.append(Paragraph(
        "Wenn du fertig bist: Dokument zurück per Mail oder Foto/Screenshot per WhatsApp.",
        styles["body"]))
    story.append(Paragraph(
        "Kein Zeitdruck — aber je früher, desto eher steht die Domain. "
        "Richtwert für dich: bis Ende der Woche, wenn es leicht geht.",
        styles["hint"]))

    return story


def main() -> None:
    styles = build_styles()
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=22 * mm,
        title="Markenname · Denkhilfe für Saskia",
        author="SG_Content_Projekt",
    )
    frame_content = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height, id="content"
    )
    cover_frame = Frame(0, 0, A4[0], A4[1], id="cover",
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
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
