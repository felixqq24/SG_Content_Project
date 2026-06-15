---
alwaysApply: true
---
# Karpathy Coding Principles (verbindlich für alle Agent-Aktionen)

Diese vier Prinzipien stammen aus Andrej Karpathys Beobachtungen zu LLM-Coding-Fehlverhalten. Sie sind die **oberste Verhaltensregel** für jeden Agent-Call — vor den JF-Grundprinzipien.

## Think Before Coding
- Bevor du Code schreibst: **benenne deine Annahmen explizit**.
- Wenn etwas unklar ist: **frage nach** statt zu raten.
- Wenn mehrere Interpretationen möglich sind: stelle sie dar, wähle nicht stillschweigend.
- Wenn ein einfacherer Weg existiert: sage das. Push back when warranted.

## Simplicity First
- Schreibe das **minimum an Code** das die Anforderung löst.
- Keine Features, Abstraktionen, Konfigurierbarkeit oder Error-Handling für Szenarien die nicht gefragt waren.
- Wenn du 200 Zeilen schreibst wo 50 reichen: **vereinfache**.
- Test: "Würde ein Senior Engineer sagen das ist overcomplicated?"

## Surgical Changes
- **Ändere nur was die Aufgabe erfordert.**
- Keine "Verbesserungen" an angrenzendem Code, Kommentaren, Formatierung.
- Match existierenden Style exakt, auch wenn du es anders machen würdest.
- Unrelated dead code: **erwähnen**, nicht löschen.
- Test: Jede geänderte Zeile muss direkt auf die User-Anforderung zurückführbar sein.

## Goal-Driven Execution
- Vage Aufgaben in **verifizierbare Kriterien** übersetzen.
- Beispiel: "Validierung hinzufügen" → "Failing tests für ungültige Inputs schreiben, dann grün machen".
- Bei Multi-Step: Plan mit Verifikation pro Schritt:
  ```
  1. [Schritt] → verify: [konkreter Check]
  2. [Schritt] → verify: [konkreter Check]
  ```

---

# Global Operating Model

## Grundprinzipien (ausnahmslos)

- **Secure by Default** — Jede Konfiguration und Schnittstelle ist im Ausgangszustand sicher. Unsichere Optionen müssen bewusst und dokumentiert aktiviert werden.
- **Zero Trust** — Keine Komponente wird implizit vertraut. Jede Anfrage wird authentifiziert, autorisiert und validiert — unabhängig vom Ursprung.
- **Fail Secure** — Bei Fehlern oder unerwarteten Zuständen fällt das System in einen sicheren Zustand. Fehler dürfen **niemals** Zugriff gewähren, der ohne den Fehler nicht bestünde.
- **Least Privilege** — Jeder Benutzer, Dienst und Prozess erhält ausschließlich die Berechtigungen, die für die spezifische Aufgabe erforderlich sind.
- **Input ist feindlich** — Alle externen Eingaben (User-Daten, API-Responses, Dateien, Webhooks) werden als potenziell bösartig behandelt und vor Verarbeitung validiert.
- **Defense in Depth** — Sicherheit hängt nie von einer einzelnen Maßnahme ab. Auth, Validierung, Netzwerk und Monitoring bilden unabhängige Schutzschichten.

## Verhalten bei Codeänderungen

- Arbeite produktionsorientiert und defensiv.
- Bevorzuge kleine, saubere Änderungen statt großer unsicherer Umbauten.
- Behalte Tenant-Isolation, Security, DSGVO, Wartbarkeit und Testbarkeit immer bei.
- Wenn Informationen fehlen, triff konservative Entscheidungen.
- Verwende bestehende Patterns des Projekts, außer diese verletzen Standards.
- Erzeuge keine stillen Breaking Changes.
- Wenn du Code änderst, beachte auch Fehlerbehandlung, Logging und Tests.
- KI-Output ist untrusted — behandle jeden KI-generierten Code wie Output eines Junior-Entwicklers: nicht vertrauenswürdig bis reviewed.
- Phantom-Dependency-Schutz — jede vorgeschlagene Dependency muss gegen die offizielle Registry verifiziert werden: existiert es? Wer ist der Maintainer? Bekannte Vulnerabilities?
- Review-Fokus bei KI-Code — Besondere Aufmerksamkeit auf: Input-Validierung, Auth-Logik, neue Dependencies, Business-Logic-Alignment.
- Known Pitfalls pflegen (PFLICHT) — JEDER Bugfix der durch eine externe API-Fehlermeldung, ein falsches Feldnamen-Mapping, ein unerwartetes Framework-Verhalten oder einen Datenstruktur-Fehler verursacht wurde MUSS SOFORT als Pitfall-Eintrag dokumentiert werden — BEVOR der Task als abgeschlossen gemeldet wird. Format: `**[Titel]**: Symptom → Lösung. (Bereich)`. Eintrag in BEIDE Dateien: `.github/copilot-instructions.md` (Projekt-spezifische Known Pitfalls) UND `.github/instructions/project-knowledge.instructions.md` (passende Sektion). Agent-Workflow: Vor Debugging die Pitfalls-Sektion ZUERST prüfen.
- Project Knowledge Base pflegen (PFLICHT) — Wenn du während der Arbeit ein grundlegendes Projektfakt entdeckst (Infrastruktur, Architektur-Entscheidung, Workaround, API-Feldnamen, Datenformate), das zukünftige Sessions wissen müssten: trage es SOFORT eigenständig in `.github/instructions/project-knowledge.instructions.md` ein — BEVOR der Task als abgeschlossen gemeldet wird. Keine Duplikate, max 40 Einträge, veraltete entfernen wenn Limit erreicht.
- Testdaten aus DB ableiten — Beim Erstellen neuer Testdaten oder Sample-Daten IMMER zuerst existierende DB-Einträge prüfen und Feldnamen/Formate daraus ableiten. NIEMALS Feldnamen raten (z.B. `email` statt `emailAddress`, `title` statt `nameTitle`).

---

# Karpathy Compliance für Code-Änderungen

- Jeder Diff muss **Karpathy-konform** sein:
  - [ ] Annahmen explizit oder geklärt
  - [ ] Minimaler Scope (kein Scope Creep)
  - [ ] Nur betroffene Dateien geändert
  - [ ] Bestehender Style exakt gematcht
  - [ ] Verifizierbares Ergebnis (Test, Build, Lint, manueller Check)
- Bei PR-Review: **Karpathy-Checklist** als zusätzlicher Review-Layer
