---
alwaysApply: true
---
# Engineering

## Codequalität

- **Strict Mode** — TypeScript: `strict: true`, `noUncheckedIndexedAccess: true`. Python: Type Hints + Strict Linting.
- **Kein `any` / `@ts-ignore` / `type: ignore`** — Ohne dokumentierte Begründung verboten.
- **Naming:** camelCase (Variablen/Funktionen), PascalCase (Klassen/Components), snake_case (DB-Spalten, Python).
- **Sprache:** Code und Kommentare auf Englisch. UI-Texte und Fehlermeldungen auf Deutsch.
- **Imports:** Konsistente Import-Organisation. Path-Aliases (`@/` → `src/`) wo vom Framework unterstützt.

## Refactoring & Wartbarkeit

- Schreibe lesbaren, wartbaren und konsistenten Code.
- Nutze vorhandene Namenskonventionen, Typisierung und Error-Handling-Muster.
- Refactoring darf Verhalten nicht unbeabsichtigt ändern.
- Vermeide unnötige Komplexität und versteckte Seiteneffekte.
- Ergänze oder aktualisiere Tests bei relevanten Änderungen.
- Reduziere technische Schulden, aber nicht auf Kosten der Stabilität.

## AI-gestützte Entwicklung

- **Review-Fokus bei KI-Code** — Besondere Aufmerksamkeit auf: Input-Validierung, Auth-Logik, neue Dependencies, Business-Logic-Alignment.
- **Known Pitfalls pflegen (PFLICHT)** — JEDER Bugfix durch externe API-Fehler, falsches Feldnamen-Mapping, unerwartetes Framework-Verhalten oder Datenstruktur-Fehler MUSS SOFORT als Pitfall-Eintrag dokumentiert werden — BEVOR der Task als abgeschlossen gemeldet wird. Format: `**[Titel]**: Symptom → Lösung. (Bereich)`. Eintrag in BEIDE Dateien: `.github/copilot-instructions.md` UND `.github/instructions/project-knowledge.instructions.md`.
- **Project Knowledge Base pflegen (PFLICHT)** — Wenn du ein grundlegendes Projektfakt entdeckst (Infrastruktur, Architektur-Entscheidung, Workaround, API-Feldnamen, Datenformate): trage es SOFORT in `.github/instructions/project-knowledge.instructions.md` ein — BEVOR der Task als abgeschlossen gemeldet wird. Keine Duplikate, max 40 Einträge, veraltete entfernen wenn Limit erreicht.
- **Testdaten aus DB ableiten** — Beim Erstellen neuer Testdaten IMMER zuerst existierende DB-Einträge prüfen und Feldnamen/Formate daraus ableiten. NIEMALS Feldnamen raten.

## Supply Chain & Dependency Security

- **Lock-Files committen** — `package-lock.json`, `poetry.lock`, `uv.lock` etc. MÜSSEN im Repo sein. Deterministische Builds.
- **Regelmäßige Audits** — `npm audit` / `pip audit` regelmäßig ausführen. Critical/High Vulnerabilities zeitnah fixen.
- **Dependency-Prüfung** — Vor jeder neuen Dependency: Lizenz prüfen, Maintainer verifizieren, bekannte CVEs checken.
- **Pinning-Strategie** — Exakte Versionen in Lock-Files. Keine offenen Ranges in Production-Dependencies.
- **Minimale Dependencies** — Kein Paket für Trivialfunktionen. Weniger Dependencies = weniger Angriffsfläche.

## Git-Workflow

- **Conventional Commits** — `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`, `security:`.
- **Feature Branches** — Neue Features und Fixes auf separaten Branches entwickeln. PR/Review für Production-Merges.
- **Build vor Merge** — Type-Checks, Linter und Tests MÜSSEN grün sein bevor Code in den Hauptbranch gemergt wird.
- **Keine Secrets in Git-History** — Wenn Secrets versehentlich committet wurden: sofort rotieren, nicht nur in neuem Commit entfernen.


## Deterministische Engineering Gates

AI-Checks ergänzen die Qualitätssicherung, ersetzen aber keine deterministischen Gates.
Vor Merge in produktive Branches gelten mindestens:
- Lint
- Typecheck
- Build
- Unit-/Integrationstests
- Contract-Tests bei externen APIs
- Secret Scan / Dependency Audit

## Definition of Done

Ein Feature/Fix ist erst done, wenn:
- Anforderungen und Annahmen geklärt sind
- Tests für positive und negative Pfade vorliegen
- Logging / Error-Handling berücksichtigt wurde
- Security- und Tenant-Aspekte geprüft wurden
- Build / Lint / Typecheck erfolgreich sind
- Review oder dokumentierte Freigabe erfolgt ist
