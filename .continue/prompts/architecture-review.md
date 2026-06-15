---
name: Architecture Review
description: Architektur-Analyse eines Features oder Moduls nach JF-Standards
---

Du führst ein Architektur-Review für JF-Hospitality durch.

## Think Before Analyzing
1. Lese relevante Dateien: `docs/architecture.md`, `.continue/rules/10-architecture.md`.
2. Identifiziere den Scope: Welche Domäne, welche Layer?
3. Nenne deine Annahmen explizit.

## Prüfpunkte

### Layer-Integrität
- Ist Business-Logic in der richtigen Schicht (nicht in Routen, nicht in DB-Layer)?
- Sind Side Effects (DB, Netzwerk, Logging) klar gekapselt?
- Gibt es zirkuläre Abhängigkeiten?

### Domain-Struktur
- Sind Module klein und fokussiert (kein God-Service)?
- Sind Interfaces klar definiert?
- Folgt die Benennung den JF-Konventionen?

### Datenzugriff
- DB-Queries im korrekten Scope (Tenant-Schema)?
- IDs nur innerhalb ihres Kontexts verwendet?
- N+1 Query Probleme?

### API-Design
- RESTful? Basis-URL `/api/v1/*`?
- Response-Shape `{ data, error, meta }`?
- Error Codes konsistent?
- Versionierung bei Breaking Changes?

### Skalierbarkeit
- Rate Limiting vorhanden?
- Caching-Strategie sinnvoll?
- Multi-Instance Ready (kein In-Memory-State ohne Redis)?

## Output-Format
Architektur-Diagramm (ASCII/Mermaid) des analysierten Moduls.
Findings mit Empfehlungen: 🔴 Kritisch / 🟡 Verbesserung / 🟢 Gut gelöst.
