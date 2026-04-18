# Website

Alles rund um die spätere Webpräsenz von `[Markenname]`.

## Status

**Noch nicht aktiv.** Der Ordner wird ab Phase 5 befüllt, sobald die Content-Grundlagen (Positioning, Personas, Messaging, Proof-Points) stehen.

## Erwartete Artefakte (ab Phase 5)

| Datei | Zweck |
|---|---|
| `sitemap.md` | IA / Seitenstruktur |
| `wireframes.md` | Textuelle Wireframes pro Seite (Hero, Sections, CTAs) |
| `copy/` | Seitentexte pro Sprache und Route (`copy/de/home.md`, `copy/en/home.md`, …) |
| `tech_decision.md` | Bewertung Astro / Next.js / Framer / CMS-Optionen, finale Wahl |
| `implementation/` | Der tatsächliche Projekt-Code (sobald Tech-Stack steht) |

## Voraussetzungen für Start

- [ ] `content/positioning.md` befüllt und freigegeben
- [ ] `content/target_personas.md` befüllt
- [ ] `content/messaging_framework.md` befüllt
- [ ] `content/proof_points.md` mit verwertbaren Belegen
- [ ] `brand/name.md` mit finalem Markennamen und Domain
- [ ] Entscheidung DE-only oder DE+EN-Launch (siehe `docs/decisions.md`)

## Tech-Stack-Entscheidungs-Hinweise

Bei der Tech-Wahl in Phase 5 berücksichtigen:
- **Mehrsprachigkeit DE/EN** — native Unterstützung wichtig
- **Self-Service-Pflege durch SG** — CMS-Bedarf prüfen (vs. Code-Edit)
- **Bildlastig** (Nanny → visuelle Vertrauensbildung) — Asset-Optimierung out-of-the-box
- **SEO-First** (Familien suchen über Google) — SSG / SSR
- **Low-Ops** — kein komplexer Server nötig
- Archivierte technische Guidelines in [../docs/_template/](../docs/_template/) reaktivieren sobald Stack steht
