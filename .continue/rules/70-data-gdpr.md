---
globs: ["**/user*", "**/profile*", "**/personal*", "**/customer*", "**/gdpr*", "**/consent*"]
alwaysApply: false
---
# DSGVO & Datenschutz

## Datenminimierung & Zweckbindung

- **PII-Minimierung** — Nur personenbezogene Daten erheben und speichern, die für den konkreten Zweck erforderlich sind. Keine Vorratsspeicherung.
- **Zweckbindung** — Daten nur für den erhobenen Zweck verwenden. Keine Zweckentfremdung ohne neue Rechtsgrundlage.
- **Löschpflichten** — Löschfristen definieren und technisch umsetzen. Right-to-Erasure (Art. 17 DSGVO) muss implementierbar sein.

## Logging & Exports

- **Keine PII in Logs/Error-Reports** — Namen, E-Mail-Adressen, IPs, Zahlungsdaten gehören nicht in Log-Dateien, Error-Tracker oder Analytics.
- **Datenexport** — Systeme müssen perspektivisch Nutzerdaten exportieren können (Art. 20 DSGVO — Datenportabilität).
- **Einwilligungsmanagement** — Wo Einwilligung die Rechtsgrundlage ist, muss diese dokumentiert und widerrufbar sein.
