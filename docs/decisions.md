# Decisions — SG_Content_Projekt

> ADR-light: Eine Zeile Kontext, eine Entscheidung, eine kurze Begründung. Neue Einträge oben.

---

## 2026-04-18 — Workspace-Zweck

- **Entscheidung:** Dieser Workspace ist Content-/Projekt-Hub für den gesamten Aufbau (Discovery → Positionierung → Website → Reichweite), nicht nur Website-Code.
- **Begründung:** Kontext, Entscheidungen und Texte bleiben an einem Ort; AI-Assistenten unterstützen konsistent; spätere Website kann denselben Kontext nutzen.

## 2026-04-18 — Phasen-Reihenfolge: Content vor Tech

- **Entscheidung:** Tech-Stack-Entscheidung (Framework, Hosting) wird **erst nach** Content-Klarheit getroffen (Positionierung, Zielgruppen, Sitemap).
- **Begründung:** Technische Anforderungen (CMS-Bedarf, Mehrsprachigkeit, Self-Service-Pflege) ergeben sich aus den Inhalten, nicht umgekehrt.
- **Kandidaten für Phase 5:** Astro · Next.js · Framer.

## 2026-04-18 — Projektname bleibt, Markenname folgt

- **Entscheidung:** Technischer Workspace-Name bleibt `SG_Content_Projekt`. Markenname für das Nanny-Angebot wird nach dem Discovery-Interview in `brand/` festgelegt.
- **Begründung:** Markenname ist Ergebnis der Positionierungsarbeit, nicht Voraussetzung. Bis dahin Platzhalter `[Markenname]` in Content-Dateien.

## 2026-04-18 — Template-Herkunft entfernt

- **Entscheidung:** JF-Hospitality-Template-Branding aus `copilot-instructions.md` und Repo entfernt. Security-/AI-Guardrails in schlanker Form behalten. JF-Tech-Docs (architecture, engineering_guidelines, e2e_testing_guidelines, ui_ux_guidelines, incident-response) nach `docs/_template/` archiviert.
- **Begründung:** Projekt ist bewusst kein JF-Hospitality-Kontext. Tech-Docs sind in Phase 5 (Website-Umsetzung) reaktivierbar, stören aber in Konzeptphase.

## 2026-04-18 — DSGVO: Roh-Transkripte nicht committen

- **Entscheidung:** `interview/raw/` ist via `.gitignore` ausgeschlossen. Roh-Transkripte, Audiodateien, VTT/SRT bleiben lokal.
- **Begründung:** Interview enthält persönliche Aussagen von SG, teilweise sensibel. Einwilligung wird vor Aufnahme eingeholt (siehe `interview/setup.md`). Nur kuratierte, freigegebene Inhalte landen im Repo.

## 2026-04-18 — Sprache: DE primär, EN sekundär

- **Entscheidung:** Website und Content auf Deutsch (primär) und Englisch (sekundär). Code und technische Kommentare ausschließlich Englisch.
- **Begründung:** "Internationale Nanny" adressiert explizit auch nicht-deutschsprachige Familien. Zweisprachigkeit bewusst einplanen (beeinflusst Tech-Stack-Wahl in Phase 5).

## 2026-04-18 — CI/CD entfernt

- **Entscheidung:** `.github/workflows/ci.yml` (JF-Hospitality Docker-Deploy-Template) entfernt.
- **Begründung:** Nichts zu bauen/deployen in Konzeptphase. Wird mit Website-Projekt in Phase 5 neu eingerichtet, passend zum gewählten Tech-Stack.
