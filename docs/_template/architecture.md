# Architektur — {{PROJEKT}}

> **Stand:** {{DATUM}}

---

## Systemübersicht

<!-- TODO: ASCII-Diagramm oder Beschreibung der Gesamtarchitektur -->
<!-- Beispiel: -->
<!--
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Browser    │───▶│  nginx/TLS   │───▶│  App (Docker)│
└──────────────┘    └──────────────┘    └──────┬───────┘
                                               │
                                        ┌──────▼───────┐
                                        │  PostgreSQL   │
                                        └──────────────┘
-->

---

## Netzwerk-Topologie

| Verbindung | Von | Nach | Wie |
|-----------|-----|------|-----|
| Browser → App | Internet | nginx | `https://{{DOMAIN}}` |
| nginx → App | Host | Docker | `127.0.0.1:{{PORT}}` |
| App → DB | Docker | PostgreSQL | `host.docker.internal:5432` |
| App → Auth | Docker | Auth-Provider | OIDC via HTTPS |

---

## Tech-Stack

| Schicht | Technologie | Version |
|---------|------------|---------|
| Framework | <!-- TODO --> | |
| Sprache | <!-- TODO --> | |
| Datenbank | PostgreSQL | 15 |
| Auth | <!-- TODO --> | |
| Container | Docker Compose | |
| Reverse Proxy | nginx | |

---

## Auth-Flow

<!-- TODO: Auth-Flow beschreiben -->
<!-- z.B. OIDC mit Authentik, API-Key-Auth für externe Clients, etc. -->

---

## Datenbank-Architektur

<!-- TODO: Datenmodell-Übersicht -->
<!-- Mindestens: welche Haupt-Entitäten, welche Relationen, welcher ORM -->

---

## Deployment

<!-- TODO: Deployment-Diagramm und -Prozess -->
<!-- Verweis auf docs/incident-response.md für Rollback -->

Siehe auch: [Incident Response](incident-response.md)
