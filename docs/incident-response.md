# Incident Response — {{PROJEKT}}

> **Ziel:** Strukturiertes Vorgehen bei Production-Problemen statt Ad-hoc-Panik.  
> **Stand:** {{DATUM}}

---

## 1. Sofortmaßnahmen bei Ausfall

### Application Down

1. **Health-Check prüfen:** `curl -s https://{{DOMAIN}}/api/health`
2. **Container-Status:** `docker ps` → läuft der Container?
3. **Logs prüfen:** `docker logs {{PROJEKT}}_app --tail 100`
4. **Neustart versuchen:** `docker compose -f docker-compose.prod.yml restart app`
5. Falls Neustart nicht hilft → Rollback (siehe unten)

### Datenbank-Probleme

1. **Connection prüfen:** `docker exec {{PROJEKT}}_app pg_isready -h host.docker.internal`
2. **Disk Space:** `df -h` auf dem Server
3. **Locks prüfen:** `SELECT * FROM pg_stat_activity WHERE state = 'active';`

---

## 2. Rollback-Strategie

### Application Rollback (Docker)

```bash
# Vorheriges Image identifizieren
docker images ghcr.io/jf-hospitality/{{PROJEKT}} --format "{{`{{.Tag}}`}} {{`{{.CreatedAt}}`}}"

# Auf vorheriges Image wechseln
# In docker-compose.prod.yml: image Tag ändern auf vorherigen SHA
docker compose -f docker-compose.prod.yml up -d app
```

### Datenbank Rollback (Migration)

<!-- TODO: An ORM anpassen (Prisma, Alembic, etc.) -->

```bash
# Letzte Migration rückgängig machen (nur wenn möglich)
# Prisma: Keine native Rollback-Funktion → manuelles SQL-Script nötig
# Alembic: alembic downgrade -1
```

**Wichtig:** Vor jeder Migration ein DB-Backup erstellen.

---

## 3. Backup & Recovery

### Backup-Verifizierung

- **RPO (Recovery Point Objective):** <!-- TODO: z.B. "Max 1 Stunde Datenverlust akzeptabel" -->
- **RTO (Recovery Time Objective):** <!-- TODO: z.B. "Max 30 Minuten bis zur Wiederherstellung" -->
- **Restore-Tests:** <!-- TODO: Frequenz definieren, z.B. "Monatlich" -->

### Backup wiederherstellen

```bash
# PostgreSQL Restore
pg_restore -h localhost -U postgres -d {{PROJEKT}} backup_file.dump
```

---

## 4. Eskalationspfade

| Schwere | Beschreibung | Verantwortlich | Reaktionszeit |
|---------|-------------|----------------|---------------|
| P1 — Kritisch | App komplett down, Datenverlust | <!-- TODO --> | Sofort |
| P2 — Hoch | Kernfunktion eingeschränkt | <!-- TODO --> | < 2 Stunden |
| P3 — Mittel | Teilfunktion betroffen, Workaround möglich | <!-- TODO --> | < 1 Tag |
| P4 — Niedrig | Kosmetisch, keine Funktionseinschränkung | <!-- TODO --> | Nächster Sprint |

---

## 5. Häufige Szenarien

### Container startet nicht nach Deployment

**Symptom:** Container restartet in Loop, Health-Check schlägt fehl.  
**Ursache:** Oft fehlende Environment-Variablen oder fehlgeschlagene Migration.  
**Lösung:**
1. `docker logs {{PROJEKT}}_app` → Fehlermeldung lesen
2. `.env` auf dem Server prüfen (fehlende Variablen?)
3. Bei Migration-Fehler: DB-State prüfen, ggf. manuell fixen
4. Rollback auf vorheriges Image wenn nötig

### Datenbank-Migration fehlgeschlagen

**Symptom:** App startet, aber Fehler bei DB-Operationen.  
**Lösung:**
1. Migration-Status prüfen
2. Fehlgeschlagene Migration identifizieren
3. Manuelles SQL-Fix oder Rollback
4. **Niemals** bestehende Migrations editieren — neues Fix-Script erstellen

### Hohe Latenz / Timeouts

**Symptom:** Requests dauern >5s oder timeout.  
**Lösung:**
1. DB-Queries prüfen (fehlende Indexes? N+1?)
2. Container-Ressourcen prüfen (CPU/Memory)
3. Externe Abhängigkeiten prüfen (Auth-Provider, APIs)
