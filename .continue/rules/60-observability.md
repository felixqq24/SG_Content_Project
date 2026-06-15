---
description: "Laden bei Logging, Error-Handling, Health-Checks, Incident-Response, Monitoring"
alwaysApply: false
---
# Observability & Monitoring

## Logging

- **Strukturiertes Logging** — JSON-Format bevorzugen. Log-Levels konsequent: ERROR (Systemfehler), WARN (unerwartetes Verhalten), INFO (geschäftsrelevante Events), DEBUG (Entwicklung).
- **Keine PII/Secrets in Logs** — Nur IDs, Aktionstypen und technische Metadaten loggen.

## Health & Error Tracking

- **Health-Endpoints** — Jede deploybare App MUSS einen `/health` oder `/api/health` Endpoint haben (ohne Auth).
- **Error Tracking** — Production-Apps SOLLTEN ein Error-Tracking-Tool nutzen (Sentry o.ä.), damit Fehler nicht nur durch User-Beschwerden entdeckt werden.
- **Request-Correlation** — Bei Microservice-Architekturen: Correlation-IDs über Service-Grenzen mitführen.

## Logging-Verhalten

- **Logging ist fire-and-forget** — Logging-Fehler blockieren nie den Hauptflow, werden aber als Warning geloggt.


## Delivery-Metriken

Mindestens beobachten:
- Dauer von Build- und Check-Läufen
- PR-Durchlaufzeit
- Anzahl fehlgeschlagener Checks
- Prod-Incidents / Hotfixes pro Monat

## Hotfix-Nachaudit

Verkürzte Prozesse für Hotfixes sind erlaubt, aber nur mit:
- kurzer Dokumentation von Ursache und Risiko
- erfolgreichem Smoke-/Health-Check nach Deployment
- Review / Nachaudit innerhalb von 24h
