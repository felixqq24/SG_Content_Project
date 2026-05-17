# Visual Identity

Sammlung visueller Richtungsentscheidungen. Status: **Arbeits-Palette steht** (SG-Freigabe 2026-04-26 via WhatsApp). Typografie & Bildsprache folgen.

## Arbeits-Palette „SG Core 4" (freigegeben 2026-04-26)

SG hat per WhatsApp ihre vier Lieblingsfarben genannt — diese ersetzen die V1-Palettenwahl als verbindliche Arbeitsgrundlage. Die Kombination ist im Kern eine **Mischung aus Palette A (Navy) und einer tieferen Variante von Palette B (Royal Purple)**, mit Pearl als Background und Gold als Hairline-Akzent.

| Rolle | Name | HEX | Verwendung |
|---|---|---|---|
| Primary (Anker) | **Midnight Navy** | `#0E1A3A` | Header, Navigation, Footer, primäre Buttons |
| Secondary | **Royal Purple** | `#4A2C6D` | Sektionen mit emotionaler Schwere („Über", „Polyvagal/Yoga"), Karten-Header, Hover |
| Accent | **Antique Gold** | `#B8893A` | Hairlines, Icons, Underlines, aktive Zustände — **niemals Flächen** |
| Background | **Warm Pearl** | `#FAF6EF` | Seiten-Grund, neutrale Sektionen |

> **Erweiterung empfohlen** (für WCAG-AA und Hierarchie, vor Mock-Screen festzulegen):
>
> - **Text Primary** auf Pearl: `#0E1A3A` (Navy) — Kontrast 14:1 ✓
> - **Text Muted** auf Pearl: ein wärmer-grauer Wert um `#5A5266` — vor Live-Test prüfen
> - **Surface** für Karten auf Pearl: `#FFFFFF` oder `#F2EBDC`
> - **Lavendel-Sand-Variante** für die Respira-Spur (siehe [name.md](name.md)): hellerer Purpurton (z. B. `#B9A8D0`) als zarter Tint statt `#4A2C6D` als Vollton.

### Farbsignal-Logik

- **Navy + Pearl + Gold** = Sungold-Spur (Sonnenwarme Hochwertigkeit, klassischer Premium-Eindruck).
- **Royal Purple + Pearl + sanftes Sand-Akzent** = Respira-Spur (Atem, Lavendel-Erdung, weiblich-ruhig).
- Beide Spuren teilen Navy & Pearl als Konstante — die Marken-Entscheidung bewegt nur Akzentgewicht.

### Risiken / Pitfalls

- `#4A2C6D` ist **dunkler und kühler als der ursprüngliche Royal Purple** (`#5E3A8A`) aus Palette B — Lesbarkeit auf Pearl ist gut, aber als großflächiger Hintergrund wirkt er fast schwarz. → Sparsam einsetzen oder mit Lavendel-Tint kombinieren.
- Navy + Royal Purple nebeneinander erzeugen eine sehr dunkle Bildsprache. → Pearl als luftiger Background ist nicht optional, sondern strukturell notwendig.
- Gold nur als **Hairline / Icon / 1-px-Linie**. Nie als Button-Fläche, sonst Kitsch.

### Nächster Schritt

→ Mock-Screen (Hero + Service-Karte) in **beiden Spuren parallel**, damit SG den Unterschied sehen statt vorstellen muss.

---

## Historie / Original-Input

### Farb-Input von SG (2026-04-23)

SGs erste Farbpräferenzen (unkuratiert, als Ausgangsmaterial für die Palette):

- **Violett**
- **Purpur**
- **Gold**
- **Dunkelblau**

### Erste Einordnung (noch nicht freigegeben)

- Die Kombination signalisiert **Premium / Hochwertigkeit** und passt zur HNW-Zielgruppe (Global Governess).
- Violett + Purpur + Gold liegen nah am „royal / luxury"-Spektrum — Risiko: zu opulent, zu „Spa/Boutique-Hotel", könnte an Wärme und Nahbarkeit verlieren, die für Care-Arbeit mit Kindern zentral ist.
- Dunkelblau als Anker wirkt seriös, ruhig, vertrauensbildend — guter Gegenpol zu Violett/Gold.
- Gold funktioniert am besten als **Akzent** (Linien, Hairlines, Icons), nicht als Flächenfarbe — sonst Kitsch-Risiko.

### Offene Fragen an SG

- Soll die Marke eher **königlich-luxuriös** (Violett/Purpur/Gold dominant) oder **ruhig-vertraulich** (Dunkelblau dominant, Violett/Gold als Akzent) wirken?
- Referenzen/Moodboard: Gibt es konkrete Marken, Hotels, Räume, die SG farblich gefallen?
- Toleranz gegenüber warmen Neutrals (Creme, Sand, warmes Off-White) als Hintergrundbasis?

### Nächste Schritte

1. Moodboard mit SG (Pinterest / Figma) — 5–8 Referenzen.
2. ~~2–3 Palettenvorschläge mit konkreten HEX-Werten und Rollen~~ → siehe unten.
3. Kontrast-Check gegen WCAG AA (Text auf Hintergrund min. 4.5:1).
4. Freigabe durch SG, dann finalisieren.

---

## Palettenvorschläge (V1, 2026-04-23)

Drei Richtungen, alle auf Basis von SGs Input (Violett / Purpur / Gold / Dunkelblau). Jede Palette ist WCAG-AA-tauglich, wenn Text-/Hintergrund-Paare wie angegeben verwendet werden.

Rollen pro Palette:
- **Primary** — dominante Markenfarbe, Hero/Navigation/Buttons.
- **Secondary** — unterstützend, Sektionen, Karten.
- **Accent** — sparsam, Highlights, Hairlines, Icons, aktive Zustände.
- **Background** — Seiten-Grund, große Flächen.
- **Surface** — Karten/Boxen auf Background.
- **Text Primary / Muted** — Fließtext und sekundärer Text.

---

### Palette A — „Midnight Governess" (Dunkelblau dominant, Gold als Akzent)

> Ruhig, vertrauensbildend, diskret-luxuriös. Dunkelblau trägt die Marke, Violett/Purpur tauchen nur in Gradients/Illustration auf, Gold ist konsequent nur Akzent. Empfohlen als **Safe-Premium-Option**.

| Rolle | Name | HEX | Notiz |
|---|---|---|---|
| Primary | Midnight Navy | `#0E1A3A` | Hero, Header, Buttons |
| Secondary | Deep Indigo | `#2A2A5C` | Sektionstrenner, Karten-Header |
| Accent | Antique Gold | `#B8893A` | Hairlines, Icons, Underlines (nie große Flächen) |
| Accent 2 | Muted Violet | `#6B4E8E` | Tags, Hover-States |
| Background | Warm Ivory | `#F6F1E8` | Seiten-Grund |
| Surface | Soft Cream | `#FBF7EF` | Karten, Boxen |
| Text Primary | Ink Navy | `#0E1A3A` | auf Ivory/Cream |
| Text Muted | Slate | `#5A5F73` | sekundär |

Kontrast-Checks (Richtwerte):
- Midnight Navy `#0E1A3A` auf Warm Ivory `#F6F1E8` → ~15.8:1 (AAA).
- Antique Gold `#B8893A` auf Warm Ivory → ~3.9:1 → **nur für Non-Text** (Linien, Icons ≥ 24px, Buttons mit dunklem Text).
- Slate `#5A5F73` auf Warm Ivory → ~5.6:1 (AA).

---

### Palette B — „Royal Care" (Purpur + Dunkelblau paritätisch, Gold als Akzent)

> SGs Input am direktesten umgesetzt: Purpur und Dunkelblau teilen sich die Hauptrolle, Gold bleibt Akzent. Wirkt königlich, aber durch warmes Off-White und ausreichend Weißraum nicht überladen. Risiko: „Boutique-Hotel-Look", muss durch Bildsprache (echte Kinder, Naturlicht) geerdet werden.

| Rolle | Name | HEX | Notiz |
|---|---|---|---|
| Primary | Royal Purple | `#4A2C6D` | Hero, Navigation, Buttons |
| Secondary | Deep Night | `#1C2548` | Footer, dunkle Sektionen |
| Accent | Soft Gold | `#C9A24B` | Akzente, Trenner |
| Accent 2 | Plum Violet | `#7A4E9E` | Hover, Tags |
| Background | Pearl `#FAF6EF` | `#FAF6EF` | Seiten-Grund |
| Surface | Lavender Mist | `#EFE9F2` | sehr sparsam, nur für Zitat-Boxen o. ä. |
| Text Primary | Near-Black Plum | `#1A1426` | auf Pearl |
| Text Muted | Dust Violet | `#5E5470` | sekundär |

Kontrast-Checks:
- Royal Purple `#4A2C6D` auf Pearl `#FAF6EF` → ~10.4:1 (AAA).
- Soft Gold `#C9A24B` auf Pearl → ~2.7:1 → **ausschließlich dekorativ** (Linien, Icons), NIE für Text.
- Deep Night `#1C2548` auf Lavender Mist `#EFE9F2` → ~12.1:1 (AAA).

---

### Palette C — „Alpine Velvet" (Dunkelblau + Violett als Duotone, Gold-Akzent, Naturton)

> Hybrid: Alpenlicht + Premium. Dunkelblau als Anker, Violett als zweiter Leitton, warmes Sandbeige bringt Wärme (Natur, Ski, Outdoor-Resilienz) in die Marke. Empfohlen, wenn die **Zermatt/Nature-Facette** sichtbar bleiben soll, ohne die Global-Governess-Positionierung zu schwächen.

| Rolle | Name | HEX | Notiz |
|---|---|---|---|
| Primary | Alpine Blue | `#19325E` | Hero, Navigation |
| Secondary | Velvet Violet | `#5B3A7A` | Sektionen, Zweitmarke |
| Accent | Warm Gold | `#BE9147` | Hairlines, Icons |
| Accent 2 | Glacier | `#A9B8C9` | sehr dezent, Illustrations-Stützfarbe |
| Background | Sand Linen | `#F2EADB` | Seiten-Grund |
| Surface | Off-White | `#FBF8F1` | Karten |
| Text Primary | Alpine Blue | `#19325E` | auf Sand/Off-White |
| Text Muted | Stone | `#5F5A4E` | sekundär |

Kontrast-Checks:
- Alpine Blue `#19325E` auf Sand Linen `#F2EADB` → ~10.9:1 (AAA).
- Velvet Violet `#5B3A7A` auf Off-White `#FBF8F1` → ~8.4:1 (AAA) — auch für Text nutzbar.
- Warm Gold `#BE9147` auf Sand Linen → ~3.2:1 → **nur Non-Text**.
- Stone `#5F5A4E` auf Sand Linen → ~5.1:1 (AA).

---

## Vergleich auf einen Blick

| Kriterium | A · Midnight Governess | B · Royal Care | C · Alpine Velvet |
|---|---|---|---|
| Dominanz | Dunkelblau | Purpur + Dunkelblau | Dunkelblau + Violett |
| Gold-Einsatz | streng Akzent | Akzent, sichtbar | Akzent, warm |
| Wirkung | diskret-luxuriös | königlich, opulent | alpin-premium, warm |
| Risiko | evtl. zu zurückhaltend | Kitsch-Risiko bei falscher Fotografie | am komplexesten zu orchestrieren |
| Beste Zielgruppe | HNW / Agenturen | HNW / Luxus-Concierge | HNW + Ski-Kombi Zermatt |
| Global-Governess-Fit | ★★★★★ | ★★★★☆ | ★★★★☆ |
| Nahbarkeit/Wärme | ★★★☆☆ | ★★☆☆☆ | ★★★★☆ |
| Umsetzungs-Safety | ★★★★★ | ★★★☆☆ | ★★★★☆ |

## Empfehlung

- **Wenn Entscheidung schnell und sicher fallen soll:** Palette A (Midnight Governess).
- **Wenn SG ihren Input Violett/Purpur unbedingt sichtbar will:** Palette C (Alpine Velvet) — liefert Violett als echte Zweitmarke, ohne ins Boutique-Hotel zu kippen.
- **Palette B** nur, wenn Bildsprache (echte Familien, Naturlicht, keine Glamour-Fotos) stark genug ist, um das Royal-Signal zu erden.

## Nächste Freigabe-Schritte

1. SG wählt eine Richtung (oder mischt: z. B. „A, aber Violett etwas präsenter wie in C").
2. Dann: echte Farbmuster auf 2 Mock-Screens (Hero + Service-Karte) rendern, bevor final committet.
3. WCAG-Kontraste gegen finale Typografie nachmessen (nicht nur Richtwerte).

## Typografie

TBD — nach Namens- und Tonalitätsentscheidung.

## Bildsprache

TBD — Fotorichtung (Naturlicht, ruhige Szenen, Kinder personenzentriert, keine gestellten Stock-Bilder).

## Logo

TBD.
