"""Generate a PDF of the web copy V2 draft for SG to review.

Updated 2026-05-31: Riviera & Ridge, Triple-Tier model, pricing included.
Uses markdown-to-PDF via reportlab with the project colour palette.
"""

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
)


OUTPUT = Path(__file__).parent.parent / "content" / "web_copy_v2.pdf"

NAVY = HexColor("#0E1A3A")
GOLD = HexColor("#B8893A")
VIOLET = HexColor("#4A2C6D")
MUTED = HexColor("#5A5F73")
PEARL = HexColor("#FAF6EF")

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


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=24, leading=28, textColor=NAVY, spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=11, leading=15, textColor=MUTED, spaceAfter=14,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=17, leading=22, textColor=NAVY, spaceBefore=18, spaceAfter=8,
            keepWithNext=1,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=13, leading=17, textColor=VIOLET, spaceBefore=12, spaceAfter=4,
            keepWithNext=1,
        ),
        "h3": ParagraphStyle(
            "H3", parent=base["Heading3"], fontName="Helvetica-Bold",
            fontSize=11, leading=15, textColor=NAVY, spaceBefore=9, spaceAfter=3,
            keepWithNext=1,
        ),
        "eyebrow": ParagraphStyle(
            "Eyebrow", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=8.5, leading=12, textColor=GOLD, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"], fontName="Helvetica",
            fontSize=10.5, leading=15, textColor=colors.black, spaceAfter=6,
            alignment=TA_LEFT,
        ),
        "hint": ParagraphStyle(
            "Hint", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=9.5, leading=13, textColor=MUTED, spaceAfter=6,
        ),
        "pull": ParagraphStyle(
            "Pull", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=13, leading=18, textColor=NAVY,
            leftIndent=10, spaceBefore=4, spaceAfter=8,
        ),
        "quote": ParagraphStyle(
            "Quote", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=10.5, leading=15, textColor=NAVY,
            leftIndent=12, rightIndent=8, spaceBefore=4, spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"], fontName="Helvetica",
            fontSize=10.5, leading=15, textColor=colors.black,
            leftIndent=14, bulletIndent=2, spaceAfter=2,
        ),
        "cta": ParagraphStyle(
            "CTA", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=10, leading=14, textColor=GOLD, spaceAfter=8,
        ),
        "check": ParagraphStyle(
            "Check", parent=base["Normal"], fontName=UNICODE_FONT,
            fontSize=10.5, leading=16, textColor=colors.black,
            leftIndent=14, spaceAfter=2,
        ),
    }


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
    canvas.drawString(20 * mm, 12 * mm, "Riviera & Ridge · Web Copy V2 · Entwurf zur Freigabe")
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
    canvas.drawString(25 * mm, A4[1] - 80 * mm, "Web Copy · Entwurf V2")
    canvas.setFont("Helvetica", 12)
    canvas.drawString(25 * mm, A4[1] - 93 * mm, "Home · About · Services (Triple-Tier) · Agencies · Contact")

    canvas.setFillColor(HexColor("#A9B8C9"))
    canvas.setFont("Helvetica-Oblique", 11)
    canvas.drawString(25 * mm, A4[1] - 106 * mm, "Primärsprache Englisch · DE-Vorfassung zur Orientierung · 31. Mai 2026")

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 11)
    intro = [
        "Liebe Saskia,",
        "",
        "das hier ist der aktualisierte Textentwurf V2 für deine Website unter",
        "dem Namen Riviera & Ridge. Englisch ist die Primärsprache,",
        "Deutsch und Französisch werden erst übersetzt, wenn die EN-Fassung sitzt.",
        "",
        "NEU in V2:",
        "   • Markenname Riviera & Ridge eingesetzt (kein Platzhalter mehr)",
        "   • Triple-Tier-Modell (Active Travel · Behavioral · Relief)",
        "   • Preise ab CHF 65/h bzw. ab CHF 8.500/Monat",
        "   • Alpine-Pakete (Essential · VIP · UHNW Companion)",
        "   • Kontaktseite mit Kalender + Callback + Formular",
        "   • B2B-Seite mit 2 Booking-Tracks für Agenturen",
        "   • Privacy Policy & Impressum (Grundgerüst)",
        "",
        "Was ich von dir brauche:",
        "   1.  Klingt das nach dir? Wo nicht?",
        "   2.  Stimmen die fachlichen Aussagen?",
        "   3.  Welche Sätze möchtest du auf keinen Fall so stehen lassen?",
        "   4.  Sind die Preise korrekt dargestellt?",
    ]
    y = A4[1] - 124 * mm
    for line in intro:
        canvas.drawString(25 * mm, y, line)
        y -= 5.5 * mm

    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(25 * mm, 32 * mm, "Richtwert für Rückmeldung: diese oder nächste Woche.")
    canvas.setFillColor(HexColor("#A9B8C9"))
    canvas.setFont("Helvetica-Oblique", 9)
    canvas.drawString(25 * mm, 25 * mm,
        "Intern · nicht zur Weitergabe an Familien oder Agenturen vor Freigabe.")
    canvas.restoreState()


def P(text, style):
    return Paragraph(text, style)


def bullets(items, styles):
    return [Paragraph("•  " + t, styles["bullet"]) for t in items]


def build_story(styles):
    story = []

    # TOC
    story.append(P("Inhalt", styles["h1"]))
    toc = [
        "1.  Home (Startseite)",
        "2.  About · Who is behind Riviera &amp; Ridge",
        "3.  Services — Triple-Tier",
        "      3.1  Active Travel &amp; Alpine Expert",
        "      3.2  Behavioral &amp; Harmony Coaching",
        "      3.3  Elite Relief &amp; Emergency Support",
        "4.  For Agencies (B2B)",
        "5.  Contact",
        "6.  Microcopy (CTAs, Footer, Consent)",
        "7.  Pricing (Richtpreise)",
        "8.  DE-Vorfassung der Startseite",
        "9.  Offene Punkte — was noch von dir kommt",
    ]
    for t in toc:
        story.append(P(t, styles["body"]))
    story.append(section_rule())

    # ==============================================================
    # 1 HOME
    story.append(P("1 — Home", styles["h1"]))

    story.append(P("HERO", styles["eyebrow"]))
    story.append(P("<i>Eyebrow:</i> Riviera &amp; Ridge · a premium nanny, based in Zermatt, available worldwide.", styles["body"]))
    story.append(P("Presence over performance.", styles["pull"]))
    story.append(P(
        "A state-certified educator, ski and yoga instructor, and mother of four — "
        "for families who want their children seen, not managed.",
        styles["body"]))
    story.append(P("CTA:  Request a conversation   ·   How we work", styles["cta"]))

    story.append(P("Alternative Headlines (zur Auswahl)", styles["h3"]))
    story.extend(bullets([
        "<i>A person, not a placeholder.</i>",
        "<i>Calm, even when the day is not.</i>",
        "<i>Care that holds the frame.</i>",
    ], styles))

    story.append(thin_rule())

    story.append(P("INTRO (≈ 60 Wörter)", styles["eyebrow"]))
    story.append(P(
        "Riviera &amp; Ridge is a premium nanny service for internationally mobile families. "
        "One qualified professional — a <i>staatlich geprüfte Erzieherin</i> "
        "(state-certified early-childhood educator), certified ski instructor, and "
        "yoga teacher — based in Zermatt, available for weekly and monthly engagements worldwide.",
        styles["body"]))
    story.append(P(
        "For children who need more than childcare: calm, attention, and a different way of being heard.",
        styles["quote"]))

    story.append(thin_rule())

    story.append(P("TRIPLE-TIER SERVICE GRID", styles["eyebrow"]))

    story.append(P("I · Active Travel &amp; Alpine Expert", styles["h3"]))
    story.append(P(
        "Weekly and monthly engagements, in Zermatt or wherever your family travels. "
        "One qualified educator with ski and outdoor competence — on the mountain and across time zones.",
        styles["body"]))

    story.append(P("II · Behavioral &amp; Harmony Coaching", styles["h3"]))
    story.append(P(
        "For children who need a calmer voice, a clearer frame, or a different rhythm. "
        "Qualified behavioural guidance rooted in 20 years of professional practice — not therapy, but depth.",
        styles["body"]))

    story.append(P("III · Elite Relief &amp; Emergency Support", styles["h3"]))
    story.append(P(
        "Qualified, discreet cover when your live-in nanny is unavailable — or when the "
        "situation calls for someone who can step in and hold the frame at short notice.",
        styles["body"]))

    story.append(thin_rule())

    story.append(P("QUIET PROOF-STRIP", styles["eyebrow"]))
    story.append(P(
        "<i>State-certified early-childhood educator · Certified ski instructor · "
        "Yoga teacher · Mother of four · Based in Zermatt · Partner of Evolution Ski School Zermatt</i>",
        styles["quote"]))

    story.append(thin_rule())

    story.append(P("HOW WE WORK (3 Schritte)", styles["eyebrow"]))

    story.append(P("1 · Conversation", styles["h3"]))
    story.append(P(
        "Every engagement begins with a qualifying conversation. It lets us understand "
        "your family, your children, and the frame you need — and it lets you understand "
        "who you are entrusting them to.",
        styles["body"]))

    story.append(P("2 · Preparation", styles["h3"]))
    story.append(P(
        "A clear brief: routines, languages, allergies, preferences, boundaries. "
        "Written, confirmed by both sides, never assumed.",
        styles["body"]))

    story.append(P("3 · Presence", styles["h3"]))
    story.append(P(
        "Quiet, professional, present. Your children know someone is holding the frame. "
        "You know where you stand at every moment.",
        styles["body"]))

    story.append(thin_rule())

    story.append(P("CLOSING", styles["eyebrow"]))
    story.append(P("Not every family is a fit. That is the point.", styles["pull"]))
    story.append(P(
        "We work on a small number of engagements at a time. A qualifying conversation "
        "is always the first step — indicative rates from CHF, confirmed after we have spoken.",
        styles["body"]))
    story.append(P("CTA:  Request a conversation", styles["cta"]))

    story.append(PageBreak())

    # ==============================================================
    # 2 ABOUT
    story.append(P("2 — About · Who is behind Riviera &amp; Ridge", styles["h1"]))

    story.append(P("OPENING", styles["eyebrow"]))
    story.append(P("One qualified person. A rare combination.", styles["pull"]))
    story.append(P(
        "Behind Riviera &amp; Ridge is SG — a <i>staatlich geprüfte Erzieherin</i> "
        "(state-certified early-childhood educator), certified ski instructor, "
        "yoga teacher, and mother of four. Based in Zermatt. Available internationally.",
        styles["body"]))
    story.append(P(
        "Name und Foto erscheinen erst nach Shooting.",
        styles["hint"]))

    story.append(thin_rule())

    story.append(P("QUALIFICATIONS", styles["eyebrow"]))
    quals = [
        "<i>Staatlich geprüfte Erzieherin</i> — state-certified early-childhood educator (Germany).",
        "<i>Fachabitur</i> — vocational higher-education entrance qualification.",
        "Studies in Social Work, with a focus on early childhood.",
        "Certified ski instructor.",
        "Certified yoga teacher (incl. children's yoga, 3HO, ~400 h).",
        "First-aid trained for working with children.",
        "Mother of four.",
    ]
    story.extend(bullets(quals, styles))
    story.append(P(
        "<i>Each qualification is documented. Certificates available on request during the qualifying conversation.</i>",
        styles["hint"]))

    story.append(thin_rule())

    story.append(P("APPROACH", styles["eyebrow"]))
    story.append(P(
        "The way a child is spoken to in the first minute of the morning sets the tone "
        "for the day. That is where the work begins.",
        styles["quote"]))
    story.append(P(
        "Children are different. Some need movement before they can sit still. Some "
        "need quiet before they can speak. Some need a clear frame more than they "
        "need a programme. That is not a diagnosis — that is attention.",
        styles["body"]))
    story.append(P(
        "This is not therapy, and it does not replace specialists. It is childcare "
        "done by a qualified educator who is used to being present without being loud.",
        styles["body"]))

    story.append(thin_rule())

    story.append(P("A NOTE ON CHILDREN WITH PARTICULAR NEEDS", styles["eyebrow"]))
    story.append(P(
        "Some children need more calm, a different pace, or a clearer frame — for "
        "reasons that may or may not carry a name. Riviera &amp; Ridge offers depth of "
        "attention, not labels. Specialist therapies and medical guidance remain "
        "with the professionals who hold them.",
        styles["body"]))

    story.append(PageBreak())

    # ==============================================================
    # 3.1 Active Travel & Alpine
    story.append(P("3.1 — Active Travel &amp; Alpine Expert", styles["h1"]))
    story.append(P("FOR INTERNATIONALLY MOBILE FAMILIES", styles["eyebrow"]))
    story.append(P("One constant, wherever you travel.", styles["pull"]))
    story.append(P(
        "Weekly and monthly engagements, in Zermatt or abroad. For children who "
        "benefit from continuity, movement, and a calmer household rhythm.",
        styles["body"]))

    story.append(P("What this looks like", styles["h3"]))
    story.extend(bullets([
        "Week- or month-long engagements, single- or multi-location.",
        "One qualified educator as the constant reference for the children — not a rotating team.",
        "Clear written brief: routines, languages, school, allergies, boundaries.",
        "Discreet coordination with existing household staff where present.",
        "Ski accompaniment in Zermatt in partnership with <b>Evolution Ski School Zermatt</b>.",
        "Travel itinerary coordination: acclimatisation support, activity programming, outdoor competence.",
    ], styles))

    story.append(P("Typical fit", styles["h3"]))
    story.extend(bullets([
        "Families based across several residences (e.g. Zurich · London · Dubai · Zermatt).",
        "Children aged roughly 3–14, single- or multilingual.",
        "Ski families in Zermatt who want a companion with alpine competence and pedagogical depth.",
        "Households that value a professional educator over a generalist.",
    ], styles))

    story.append(P("Partner note", styles["h3"]))
    story.append(P(
        "Ski instruction in Zermatt is delivered exclusively by <b>Evolution Ski School Zermatt</b> "
        "(Fabrizio Pavan). Riviera &amp; Ridge provides the care component: preparation, "
        "transitions, quiet time, and companionship on and off the snow.",
        styles["quote"]))

    story.append(P("Indicative frame", styles["h3"]))
    story.extend(bullets([
        "Indicative rates from CHF 65/h, confirmed after the qualifying conversation.",
        "Travel, accommodation, and per diems arranged separately.",
        "Languages: English (working language), German, French.",
    ], styles))

    story.append(P("CTA:  Request a conversation", styles["cta"]))

    story.append(PageBreak())

    # ==============================================================
    # 3.2 Behavioral & Harmony
    story.append(P("3.2 — Behavioral &amp; Harmony Coaching", styles["h1"]))
    story.append(P("FOR CHILDREN WHO NEED A DIFFERENT APPROACH", styles["eyebrow"]))
    story.append(P("Calm that holds. Structure that carries.", styles["pull"]))
    story.append(P(
        "Qualified behavioural guidance for children who need more than entertainment — "
        "rooted in 20 years of professional practice as an educator.",
        styles["body"]))

    story.append(P("What this looks like", styles["h3"]))
    story.extend(bullets([
        "Engagements from days to weeks, integrated into the family's daily rhythm.",
        "Behavioural guidance: clear frames, consistent boundaries, age-appropriate emotional regulation.",
        "Conflict resolution within sibling groups or between children and existing staff.",
        "Developmental observation and enrichment — without diagnostic labelling.",
        "Mindfulness and yoga-based techniques where appropriate (certified children's yoga, 3HO).",
    ], styles))

    story.append(P("Typical fit", styles["h3"]))
    story.extend(bullets([
        "Children who respond to calm authority rather than entertainment.",
        "Families seeking a qualified educator's perspective on challenging dynamics.",
        "Households where existing care works day-to-day, but particular situations call for a different skillset.",
    ], styles))

    story.append(P("A note on scope", styles["h3"]))
    story.append(P(
        "This is not therapy, and it does not replace specialists. It is childcare and "
        "guidance delivered by a <i>staatlich geprüfte Erzieherin</i> who is trained to "
        "observe, adapt, and hold the frame — for children who benefit from a quieter presence.",
        styles["quote"]))

    story.append(P("CTA:  Request a conversation", styles["cta"]))

    story.append(PageBreak())

    # ==============================================================
    # 3.3 Elite Relief
    story.append(P("3.3 — Elite Relief &amp; Emergency Support", styles["h1"]))
    story.append(P("WHEN YOUR LIVE-IN NANNY IS UNAVAILABLE", styles["eyebrow"]))
    story.append(P("Cover that carries the household — without rewriting it.", styles["pull"]))
    story.append(P(
        "Qualified, discreet relief for established households during illness, "
        "leave, or short-term gaps. Available at short notice.",
        styles["body"]))

    story.append(P("What this looks like", styles["h3"]))
    story.extend(bullets([
        "Engagements from a weekend to several weeks.",
        "Structured hand-over — routines, allergies, preferences — read, confirmed, followed.",
        "No attempt to reinvent the household. The goal is seamless continuity.",
        "Written close-out at the end of the engagement, ready for your returning staff.",
        "Sole charge or shared care, depending on the family's structure.",
    ], styles))

    story.append(P("Typical fit", styles["h3"]))
    story.extend(bullets([
        "Families with an existing live-in nanny who needs leave or medical cover.",
        "Situations requiring a qualified educator at short notice — not an au pair, not an agency temp.",
        "Household managers or family offices coordinating on behalf of the family.",
    ], styles))

    story.append(P("CTA:  Request a conversation", styles["cta"]))

    story.append(PageBreak())

    # ==============================================================
    # 4 B2B
    story.append(P("4 — For Agencies (B2B)", styles["h1"]))
    story.append(P("PLACEMENTS VIA YOUR AGENCY", styles["eyebrow"]))
    story.append(P("A qualified educator, placed through channels you already trust.", styles["pull"]))
    story.append(P(
        "Riviera &amp; Ridge is available for placements via selected nanny and governess "
        "agencies. All contractual, logistical, and communication frames sit with "
        "your agency. We focus on the child.",
        styles["body"]))

    story.append(P("Two Booking Tracks", styles["h3"]))
    story.extend(bullets([
        "<b>Track 1 — Introductory Call (30 min):</b> For new agencies exploring a collaboration.",
        "<b>Track 2 — Placement Briefing (15 min):</b> For returning partners with a specific family brief.",
    ], styles))

    story.append(P("What we bring", styles["h3"]))
    story.extend(bullets([
        "<i>Staatlich geprüfte Erzieherin</i> with additional ski and yoga qualifications.",
        "Depth of attention for children with particular needs, without diagnostic labelling.",
        "Clean hand-overs, written close-outs, discreet communication.",
        "Working languages: English, German, French.",
    ], styles))

    story.append(P("Collaboration model", styles["h3"]))
    story.extend(bullets([
        "Single placements, relief cover, or recurring engagements (e.g. annual ski season).",
        "One point of contact on each side. No intermediary layers.",
        "Full transparency on availability, qualifications, and indicative rates.",
        "Reciprocal visibility (logo placement, subject to written agreement).",
    ], styles))

    story.append(P("CTA:  Book an introductory call", styles["cta"]))

    story.append(PageBreak())

    # ==============================================================
    # 5 Contact
    story.append(P("5 — Contact", styles["h1"]))
    story.append(P("Every engagement begins with a conversation.", styles["pull"]))
    story.append(P(
        "The qualifying conversation lets us understand your family — and lets you "
        "understand who you are entrusting your children to. It is unhurried, confidential, "
        "and without obligation. Indicative rates from CHF are shared afterwards, in writing.",
        styles["body"]))

    story.append(P("Three contact options", styles["h3"]))
    story.extend(bullets([
        "<b>Book a Qualifying Call</b> — 20 min, video or phone.",
        "<b>Request a Callback</b> — leave your number, we call within 2 working days.",
        "<b>Send an Enquiry</b> — written form, reply within 2 working days.",
    ], styles))

    story.append(P("Closing text", styles["h3"]))
    story.append(P(
        "Riviera &amp; Ridge is a one-person practice. When you write, call, or book — "
        "you reach the person who will be with your children. No call centre, no intake team, no handoff.",
        styles["quote"]))

    story.append(PageBreak())

    # ==============================================================
    # 6 Microcopy
    story.append(P("6 — Microcopy", styles["h1"]))

    story.append(P("CTAs", styles["h3"]))
    story.extend(bullets([
        "Primary:  <b>Request a conversation</b>",
        "Calendar: <b>Choose a time →</b>",
        "Callback: <b>Request a callback →</b>",
        "B2B:  <b>Book an introductory call →</b>",
        "Soft:  <i>Read more →</i>  ·  <i>How we work</i>",
    ], styles))

    story.append(P("Footer claim", styles["h3"]))
    story.append(P(
        "Riviera &amp; Ridge — a premium nanny, based in Zermatt, available worldwide.",
        styles["quote"]))

    story.append(thin_rule())

    # ==============================================================
    # 7 Pricing
    story.append(P("7 — Pricing (Richtpreise für Website)", styles["h1"]))
    story.append(P(
        "Die Zusammenarbeit wird individuell gestaltet und orientiert sich an "
        "Umfang, Reisetätigkeit, Verantwortung und Einsatzort.",
        styles["body"]))

    story.append(P("Basispreise", styles["h3"]))
    story.extend(bullets([
        "Internationale Premium-Betreuung: <b>ab CHF 65 / Stunde</b>",
        "Langfristige Arrangements: <b>ab CHF 8.500 / Monat</b>",
        "UHNW-Jahresvereinbarungen: individuell kalkuliert",
    ], styles))

    story.append(P("Alpine Family Experience — Wochenpakete", styles["h3"]))

    story.append(P("Essential Family Support", styles["h2"]))
    story.extend(bullets([
        "Tägliche Kinderbetreuung, Ski-Organisation, Mittag-/Pausenbetreuung",
        "Abendunterstützung nach Vereinbarung, leichte Concierge-Aufgaben",
        "<b>ab CHF 4.800 / Woche</b> zzgl. Unterkunft, Skipass, Reisespesen",
    ], styles))

    story.append(P("Alpine VIP Family Experience", styles["h2"]))
    story.extend(bullets([
        "Premium-Betreuung, Full Family Assistance, flexible Zeiten",
        "Wellness-/Yoga-Elemente, direkte Ski-Instructor-Abstimmung",
        "<b>CHF 7.500 – 12.000 / Woche</b> (abhängig von Kinderzahl, Season, VIP-Level)",
    ], styles))

    story.append(P("UHNW Private Ski Companion", styles["h2"]))
    story.extend(bullets([
        "On-call, diskrete Reisebegleitung, Chalet Life Management",
        "Emotional regulation, private wellness sessions",
        "<b>ab CHF 15.000 / Woche</b> plus Luxury Accommodation, Meals, Driver, Travel",
    ], styles))

    story.append(P(
        "Schlüsselmärkte: Zermatt · Verbier · Courchevel · St. Moritz · Lech · Aspen · Dubai",
        styles["hint"]))

    story.append(PageBreak())

    # ==============================================================
    # 8 DE
    story.append(P("8 — DE-Vorfassung der Startseite", styles["h1"]))
    story.append(P(
        "Nur zur Orientierung, damit sich der Ton auf Deutsch spürbar macht. "
        "Die finale DE-Fassung entsteht nach EN-Freigabe via DeepL + Review.",
        styles["hint"]))

    story.append(P("HERO (DE)", styles["eyebrow"]))
    story.append(P("Präsenz statt Programm.", styles["pull"]))
    story.append(P(
        "Staatlich geprüfte Erzieherin, zertifizierte Skilehrerin, Yogalehrerin, "
        "Mutter von vier — für Familien, die ihre Kinder gesehen wissen wollen, nicht verwaltet.",
        styles["body"]))
    story.append(P("CTA:  Gespräch anfragen   ·   So arbeiten wir", styles["cta"]))

    story.append(P("TRIPLE-TIER (DE)", styles["eyebrow"]))
    story.append(P("I · Active Travel &amp; Alpine Expert", styles["h3"]))
    story.append(P(
        "Wochen- und Monatseinsätze, in Zermatt oder überall, wohin Ihre Familie reist. "
        "Eine qualifizierte Erzieherin mit Ski- und Outdoor-Kompetenz.",
        styles["body"]))

    story.append(P("II · Behavioral &amp; Harmony Coaching", styles["h3"]))
    story.append(P(
        "Für Kinder, die eine ruhigere Stimme, einen klareren Rahmen oder einen anderen "
        "Rhythmus brauchen. Fachlich fundierte Verhaltensbegleitung — keine Therapie, aber Tiefe.",
        styles["body"]))

    story.append(P("III · Elite Relief &amp; Emergency Support", styles["h3"]))
    story.append(P(
        "Qualifizierte, diskrete Vertretung, wenn Ihre Live-in-Nanny ausfällt — oder wenn "
        "die Situation nach jemandem verlangt, der kurzfristig den Rahmen hält.",
        styles["body"]))

    story.append(PageBreak())

    # ==============================================================
    # 9 Offene Punkte
    story.append(P("9 — Offene Punkte (bitte prüfen)", styles["h1"]))
    story.append(P(
        "Diese Punkte brauchen deinen Input, bevor wir finalisieren und DE/FR übersetzen.",
        styles["hint"]))

    checks = [
        "<b>Rollenbezeichnung EN</b> — welche soll auf die Website? Shortlist: Private Family Companion · Holistic Child Development Specialist · Premium Family Support · Governess · Family Lifestyle Manager · Educational &amp; Wellness Nanny · High Profile Family Assistant",
        "<b>Preise korrekt?</b> — ab CHF 65/h, ab CHF 8.500/Monat, Alpine-Pakete CHF 4.800 / 7.500–12.000 / 15.000 — alles so richtig?",
        "<b>Fabrizio Pavan / Evolution Ski School</b> — Text-Freigabe für Partner-Nennung auf Website nochmal bestätigen.",
        "<b>Fotos</b> — 16 professionelle Shots + 2 Selfies erhalten. Bildauswahl für Hero/About/Contact: passt die Zuordnung? (Siehe Mockup.)",
        "<b>Anonymisierter Case</b> — dürfen wir eine kurze Textfassung vorbereiten?",
        "<b>Stil-Check</b> — welche Passagen klingen nicht nach dir? Bitte markieren.",
        "<b>Fehlende Themen</b> — fehlt etwas, das unbedingt rein muss?",
        "<b>Domain</b> — rivieraandridge.com + .ch registrieren? (Beide frei.)",
    ]
    for c in checks:
        story.append(P("☐  " + c, styles["check"]))

    story.append(Spacer(1, 8 * mm))
    story.append(P(
        "Wenn du fertig bist: markiertes PDF zurück per Mail, Anmerkungen in einer "
        "kurzen Sprachnachricht, oder einfach Whatsapp — alles geht.",
        styles["body"]))

    return story


def main() -> None:
    styles = build_styles()
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=22 * mm,
        title="Web Copy V2 · Riviera & Ridge",
        author="SG_Content_Projekt",
    )
    content_frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height, id="content"
    )
    cover_frame = Frame(0, 0, A4[0], A4[1], id="cover",
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=on_cover),
        PageTemplate(id="content", frames=[content_frame], onPage=on_page),
    ])

    story = [NextPageTemplate("content"), PageBreak()]
    story.extend(build_story(styles))
    doc.build(story)
    print(f"✓ PDF generiert: {OUTPUT}")


if __name__ == "__main__":
    main()
