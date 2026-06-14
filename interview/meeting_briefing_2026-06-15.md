# Meeting Briefing — 15.06.2026, 18:30 (Teams)

**Teilnehmer:** Felix + SG  
**Kontext:** Website ist live deployed, SG-Feedback vom 07.06. + 14.06. eingearbeitet  
**Live-URL:** https://rivieraandridge.com (+ riviera-and-ridge.netlify.app)

---

## 1 · Status seit letztem Kontakt

| Was | Status |
|-----|--------|
| Website live auf eigener Domain | ✅ rivieraandridge.com |
| SSL/HTTPS | ✅ aktiv |
| Auto-Deploy (GitHub → Netlify) | ✅ bei jedem Push |
| Impressum + Datenschutz mit echten Daten | ✅ eingebaut |
| SG-Feedback 14.06. eingearbeitet | ✅ deployed |

### Konkret umgesetzt (aus SG-Feedback):
- **Internationaler:** „Based in Switzerland · Available Worldwide" statt „Zermatt-only"
- **Pricing breiter:** Hourly / Weekly / Monthly statt nur Alpine-Pakete
- **Team-Hinweis:** „Where needed, qualified professionals support the work" statt „one-person practice"
- **Negative Formulierungen entfernt:** keine „not a placeholder / not entertainment" mehr
- **Brand-Satz prominenter:** „When children feel emotionally safe…" mit visuellen Pillar-Tags
- **Testimonials-Sektion:** jetzt sichtbar auf Homepage (wartet auf echte Texte)
- **Mehr Bildsprache:** „A child who feels secure travels differently"

---

## 2 · Offene Fragen für SG (Agenda)

### A — Testimonials / Empfehlungen
- Welche Bewertungen/Empfehlungen sollen auf die Homepage?
- Bitte konkrete Texte mitbringen (oder Screenshots) + gewünschte Zuordnung (z.B. „Family, London")
- Wie viele? (3 auf Homepage ideal, weitere auf eigener Unterseite möglich)
- Freigabe von den Familien schon eingeholt?

### B — Mausi-Geschichte
- Soll sie als anonymisierte Case Study auf die Website?
- Wenn ja: wo? (About-Seite / eigene Story-Seite / Testimonials)
- Wie detailliert? (2-3 Sätze vs. längere Erzählung)

### C — Fotos
- 16 Porträtfotos vorhanden (Sofa + Glasbausteinwand)
- Brauchen wir weitere? (Action, Outdoor, mit Kindern, Natur)
- Wer fotografiert? (Chris/Canva-Kontakt oder neues Shooting?)

### D — Bernadette / Team
- Soll Bernadette (Supreme, Zermatt) namentlich auf der Website?
- Oder generisch: „hand-picked professionals in my network"?
- Gibt es weitere Team-Mitglieder, die erwähnt werden sollen?

### E — Brainstorming: positive Sprache
- SG wollte über die „negativen Formulierungen" brainstormen
- Vorbereitung: welche Kernaussagen sollen transportiert werden?
  - „Ich bin keine Agentur-Aushilfe" → positiv: ?
  - „Keine Diagnose/Therapie" → positiv: „rooted in professional childcare"
  - „Kein Handoff" → positiv: „you always reach the person who leads"
- Vorschlag: 3-4 positive Brand-Statements gemeinsam formulieren

### F — Sonstiges
- **Fabrizio Pavan:** Text für Partner-Sektion freigegeben?
- **Versicherung/Haftpflicht:** Soll Info auf die Website? Welche Police?
- **.ch Domain:** Redirect rivieraandridge.ch → .com einrichten?
- **Visitenkarten/Flyer:** Stand Chris/Canva?

---

## 3 · Nächste Schritte (Vorschlag für nach dem Call)

1. Testimonials einfügen (sobald Texte vorliegen)
2. Weitere Fotos einbauen (Hero, Services-Seiten)
3. WhatsApp Business + Telefonnummer als Kontaktkanal ergänzen
4. DNS: www-Subdomain + .ch-Redirect
5. Meta-Tags / SEO final prüfen
6. Soft-Launch Kommunikation (wem zeigen wir die Seite zuerst?)

---

## 4 · Technisches (für Felix intern)

- `package-lock.json` fehlt im Repo → bei nächstem Commit ergänzen
- Netlify Forms: noch nicht getestet (Kontaktformular absenden)
- Bilder-Optimierung: nur 3 Bilder aktuell, weitere Assets nötig
- `.ch`-Redirect in `netlify.toml` konfiguriert, DNS noch nicht
