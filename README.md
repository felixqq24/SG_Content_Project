# SG_Content_Projekt

Content- und Webprojekt-Hub für den Aufbau eines neuen Geschäftsfeldes: **internationale Nanny mit fachlicher Qualifikation** (Schwerpunkt Kinder mit besonderen Bedürfnissen & Hochbegabung).

> **Stand:** 2026-04-18 · **Phase:** Discovery / Konzept

---

## Zweck dieses Workspaces

Der Workspace trägt den gesamten Aufbau von der ersten Idee bis zur öffentlichen Präsenz. Jede Phase erzeugt Artefakte, die Grundlage für die nächste sind:

```
Discovery-Interview  →  Positionierung & Messaging  →  Website-Konzept  →  Umsetzung  →  Reichweite
     (interview/)         (content/, brand/)            (website/)         (website/)    (outreach/)
```

Alles in einem Repo, damit Kontext, Entscheidungen und Texte an einem Ort liegen und AI-Assistenten (Copilot) konsistent unterstützen können.

---

## Einstieg

| Du willst… | Lies zuerst |
|---|---|
| Das Projekt verstehen | [docs/initial_context.md](docs/initial_context.md) |
| Wissen, was bereits entschieden ist | [docs/decisions.md](docs/decisions.md) |
| Das Discovery-Interview vorbereiten | [interview/leitfaden.md](interview/leitfaden.md) |
| Eine Content-Säule befüllen | [content/README.md](content/README.md) |
| Fachbegriffe nachschlagen | [docs/glossary.md](docs/glossary.md) |

---

## Projektstruktur

```
SG_Content_Projekt/
├── .github/
│   ├── copilot-instructions.md                     ← AI Coding Standards
│   └── instructions/
│       └── project-knowledge.instructions.md       ← Living Knowledge Base
├── docs/
│   ├── initial_context.md                          ← Was & für wen
│   ├── decisions.md                                ← ADR-light
│   ├── glossary.md                                 ← Fachbegriffe
│   ├── initialer_kontext.pdf                       ← Quelle (Brainstorm)
│   └── _template/                                  ← archivierte Tech-Docs (Phase 5+)
├── interview/                                      ← Discovery-Call mit SG
│   ├── leitfaden.md                                ← ablesbarer Gesprächsleitfaden
│   ├── vorbereitung.md                             ← Checkliste für SG
│   ├── transkript-template.md                      ← Struktur für Post-Call
│   ├── setup.md                                    ← Teams-Transkription, DSGVO
│   └── raw/                                        ← Roh-Transkripte (gitignored!)
├── research/                                       ← Wettbewerb, Keywords, Inspiration
├── brand/                                          ← Name, Tonalität, Assets
├── content/                                        ← Positioning, Personas, Messaging, Copy
├── website/                                        ← Sitemap, Wireframes, Code (ab Phase 5)
└── outreach/                                       ← Kanäle, Content-Kalender, KPIs
```

---

## Workflow

1. **Discovery-Interview** mit SG führen ([interview/leitfaden.md](interview/leitfaden.md)) → Teams-Call, 45–60 min.
2. **Transkript strukturieren** ([interview/transkript-template.md](interview/transkript-template.md)).
3. **Content-Ableitungen** füllen: [content/positioning.md](content/positioning.md), [content/target_personas.md](content/target_personas.md), [content/messaging_framework.md](content/messaging_framework.md) etc.
4. **Markenentscheidung** in [brand/](brand/) treffen (Name, Farben, Tonalität).
5. **Website konzipieren** in [website/](website/) (Sitemap → Wireframes → Copy → Tech-Stack).
6. **Reichweite aufbauen** über [outreach/](outreach/) (Kanäle, Kalender).

---

## Arbeitsprinzipien

- **Entscheidungen festhalten** — jede wichtige Entscheidung bekommt einen Eintrag in [docs/decisions.md](docs/decisions.md).
- **Fakten statt Erfindungen** — Qualifikationen, Referenzen und Zitate nur aus belegter Quelle. Markenname, Preisstrukturen etc. bleiben Platzhalter bis entschieden.
- **Respektvolle Sprache** — personenzentriert bei Kindern mit besonderen Bedürfnissen ("Kind mit Autismus", nicht "autistisches Kind"). Siehe [.github/copilot-instructions.md §14](.github/copilot-instructions.md).
- **Sprache:** Inhalte DE (primär) / EN (sekundär). Code EN.
- **DSGVO:** Roh-Transkripte und persönliche Aussagen gehören **nicht** in Git. `interview/raw/` ist gitignored.

---

## Nächster Schritt

→ [interview/leitfaden.md](interview/leitfaden.md) prüfen und Teams-Call mit SG terminieren.
