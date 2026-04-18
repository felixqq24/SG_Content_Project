---
applyTo: "**"
---

<!-- Living Project Knowledge Base -->
<!-- Self-maintaining: Agent adds discovered facts autonomously during work. -->
<!-- Purpose: New chat sessions immediately know operational facts without reading docs. -->
<!-- Max 40 entries. Remove outdated ones when limit reached. No duplicates. -->
<!-- Format: One concise bullet point per fact. No prose. -->

# Project Knowledge Base

## Project Meta

- Project name: `SG_Content_Projekt`
- Project type: Content-/Webprojekt-Hub (kein Software-Produkt, keine Infrastruktur)
- Init date: 2026-04-18
- Current phase: Discovery / Konzept (Phase 0–3 abgeschlossen, Interview terminiert)
- Discovery-Interview-Termin: Montag, 20.04.2026, 18:15 Uhr (Teams, 45–60 min)
- Git-Remote: existiert bereits (privat, `origin` → `felixqq24/SG_Content_Project`)
- Brand name: TBD — wird nach Discovery-Interview in `brand/` festgelegt; bis dahin Platzhalter `[Markenname]`
- Domain: tbd

## Business Context

- Projektinhaberin: SG (Freundin; Eigenname in Repo-Dokumenten nur als "SG" oder Platzhalter, nie Vollname)
- Geschäftsfeld: Internationale Nanny mit fachlicher Qualifikation
- Qualifikationen (aus `docs/initialer_kontext.pdf`): Skilehrerin, Yogalehrerin, staatl. gepr. Erzieherin, Fachabitur, Studiengang Soziale Arbeit im Elementarbereich
- Spezialisierung: Kinder mit besonderen Bedürfnissen (Down-Syndrom, Autismus, körperliche Behinderung) + Hochbegabung
- Zielgruppe: Familien, die eine hochqualifizierte Betreuung mit spezifischer Fachexpertise suchen
- Primärsprache Inhalte: Deutsch · Sekundär: Englisch (internationale Zielgruppe)
- Code-Sprache: Englisch

## Content & Language Rules

- Personenzentrierte Sprache bei Kindern mit besonderen Bedürfnissen: "Kind mit Autismus", nicht "autistisches Kind"
- Keine defizitäre Sprache; Stärken-Fokus
- Qualifikationen/Referenzen/Erfolgsgeschichten nur mit belegter Quelle verwenden — nichts erfinden
- Markenname bleibt Platzhalter bis SG-Entscheidung

## Infrastructure

- Aktuell keine — Content-/Konzept-Phase
- Kein Deployment, keine DB, keine APIs
- CI/CD entfernt (`.github/workflows/` leer); wird ab Website-Phase reaktiviert

## Architecture

- Keine Tech-Stack-Entscheidung getroffen (bewusst, siehe `docs/decisions.md`)
- Tech-Kandidaten für Website-Phase: Astro / Next.js / Framer (Auswahl nach Content-Fertigstellung)
- Archivierte technische Vorlagen (JF-Template, Phase-5-Reaktivierung): `docs/_template/`

## DSGVO / Privacy

- Roh-Transkripte des Discovery-Interviews sind PII-haltig → `interview/raw/` via `.gitignore` ausgeschlossen
- Einwilligung SG vor Aufnahme erforderlich (dokumentiert in `interview/setup.md`)
- Nur kuratierte, freigegebene Inhalte landen im Repo

## Workarounds

<!-- Known issues requiring specific approaches — added as discovered -->

## Known Pitfalls

<!-- Format: **[Titel]**: Symptom → Lösung. (Bereich) -->
*(Noch keine Einträge)*
