# Interview-Setup — Teams-Transkription & DSGVO

## Technisches Setup

### Teams-Transkription aktivieren

1. Call starten.
2. In der Besprechungsleiste oben rechts → **Weitere Aktionen (…)** → **Transkription starten**.
3. Sprache auf **Deutsch** setzen (ggf. anpassen wenn Teile auf Englisch).
4. Live-Transkription ist sichtbar → zur Kontrolle, dass es läuft.
5. Nach dem Call: **Mehr → Besprechungsdetails → Transkript herunterladen** (DOCX/VTT).

### Backup-Option

Falls Teams-Transkription nicht funktioniert:
- Call über Teams-native Aufnahme mitschneiden.
- Separat lokal aufnehmen (z. B. QuickTime → Audio-only) als Fallback.
- Nachgelagert mit einem Tool transkribieren (z. B. Whisper lokal, MacWhisper, Mac-Diktat) — **lokal, keine Cloud-Upload-Tools mit PII**.

---

## DSGVO / Einwilligung

### Vor dem Call

- SG **informieren**, dass der Call aufgezeichnet und transkribiert wird.
- Zweck erklären: „Damit wir danach das Material strukturiert für Positionierung, Messaging und Website nutzen können."
- **Einwilligung schriftlich** (kurze Mail oder WhatsApp reicht) einholen und ablegen in `interview/raw/einwilligung_YYYY-MM-DD.md` (nicht committen) oder außerhalb des Repos.
- Widerrufsrecht klarstellen: „Du kannst jederzeit sagen, dass Teile raus sollen oder alles."

### Einwilligungs-Textbaustein (Vorschlag)

> „Ich, [SG], bin damit einverstanden, dass unser Gespräch am [Datum] per Microsoft Teams aufgezeichnet und transkribiert wird. Zweck ist die strukturierte Nutzung des Materials für die Positionierung, Messaging und Website-Entwicklung meines neuen Geschäftsfeldes als internationale Nanny. Das Roh-Material (Audio, wörtliches Transkript) bleibt lokal bei Felix Kraemer und wird nicht veröffentlicht. Abgeleitete, kuratierte Inhalte werden mir vor einer Veröffentlichung zur Freigabe vorgelegt. Ich kann meine Einwilligung jederzeit widerrufen."

### Zu Call-Beginn (zum Ablesen)

> „Bevor wir starten — ich hab die Transkription eingeschaltet. Das Roh-Transkript bleibt komplett bei mir lokal, nichts davon landet öffentlich. Für alles, was wir später irgendwo verwenden — Website, Social, Proof-Points — schaue ich dir vorher eine kuratierte Fassung zur Freigabe. Passt das so?"

### Umgang mit Dritten im Transkript

- Namen von **früheren Familien** oder **Kindern** standardmäßig **anonymisieren** (z. B. „Familie M. mit Tochter, 7, Autismus-Spektrum").
- Direkte Zitate über Dritte nur mit deren **expliziter schriftlicher Zustimmung**.
- Für unsere bestehende Referenz (Lotta) liegt bereits eine freigegebene Fassung vor → klar kennzeichnen.

---

## Dateiablage

| Art | Ort | Commit? |
|---|---|---|
| Audio-Datei (`.m4a`, `.mp3`) | `interview/raw/` | **Nein** (gitignored) |
| VTT/SRT-Untertitel | `interview/raw/` | **Nein** (gitignored) |
| Wörtliches Transkript | `interview/raw/transkript_YYYY-MM-DD.md` | **Nein** (gitignored) |
| Einwilligung | `interview/raw/einwilligung_YYYY-MM-DD.md` oder außerhalb Repo | **Nein** |
| Kuratierte Fassung (freigegeben) | `interview/transkript-template.md` befüllt | **Ja** (nach SG-Freigabe) |

Die `.gitignore` schließt `interview/raw/` und gängige Audio-/Untertitelformate in `interview/` aus (siehe [.gitignore](../.gitignore)).

---

## Nach dem Call — DSGVO-Checkliste

- [ ] Roh-Transkript in `interview/raw/` abgelegt (lokal, nicht committed).
- [ ] Audio-/Videodatei in `interview/raw/` abgelegt (lokal, nicht committed).
- [ ] Einwilligung archiviert.
- [ ] Kuratierte Fassung erstellt.
- [ ] SG zur Freigabe vorgelegt.
- [ ] Erst nach Freigabe: commit + push.
