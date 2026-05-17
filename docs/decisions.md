# Decisions — SG_Content_Projekt

> ADR-light: Eine Zeile Kontext, eine Entscheidung, eine kurze Begründung. Neue Einträge oben.

---

## 2026-05-17 — Tech-Stack: Netlify + Astro (Free Tier)

- **Entscheidung:** Website wird mit **Astro** (Static Site Generator) gebaut und auf **Netlify** (Free Tier) gehostet. Deployment via GitHub (Push → Build → Deploy).
- **Begründung:** (1) Netlify Built-in Forms eliminieren Backend-Code für alle 4 Formulare (Contact, Callback, B2B Placement, PDF-Gate) — minimaler Wartungsaufwand. (2) Astro ist optimal für Content-Sites mit wenig JS, unterstützt Markdown Content Collections für EN/DE/FR, und Islands-Architektur für Kalender-Embed. (3) Free Tier reicht: 100 Form-Submissions/Monat (Premium-Nische braucht <50), 100 GB Bandwidth, Deploy Previews für SG-Review inklusive. (4) Keine Sensitivdaten auf der Website (Qualifizierungsgespräche per Telefon/Teams) → kein erhöhtes DSGVO-Schutzniveau nötig → WAF/Enterprise-Features nicht erforderlich.
- **Verworfene Alternativen:** Cloudflare Pages (stärkste Security, aber Workers-Komplexität für Formulare unverhältnismäßig), Vercel (bestes DX, aber kein Built-in Form Handling), GitHub Pages (zu limitiert für Formulare/Headers).
- **Upgrade-Pfad:** Netlify Pro ($19/Monat) bei >100 Submissions/Monat oder Bedarf an Password-Protected Previews.

## 2026-05-17 — Keine Sensitivdaten auf der Website

- **Entscheidung:** Die Website verarbeitet **ausschließlich Kontaktdaten** für Terminvereinbarung (Name, E-Mail, Telefon, Land, Kinderzahl/-alter, Engagement-Zeitraum). Informationen über besondere Bedürfnisse, Verhaltensbeobachtungen oder Gesundheitsdaten werden **nicht** über Website-Formulare erhoben, sondern im Qualifizierungsgespräch (Telefon/Teams) besprochen.
- **Begründung:** Vermeidet Art. 9 DSGVO auf der Website komplett. Reduziert Formularkomplexität, DSGVO-Aufwand und Hosting-Anforderungen. Sensitivdaten gehören in den persönlichen Dialog, nicht in ein Webformular.

## 2026-05-17 — Triple-Tier-Service-Modell (ersetzt alte 3-Säulen-Struktur)

- **Entscheidung:** Die Service-Struktur wird von den drei Säulen (Global Governess / Nanny-Vertretung / Ski+Care) auf das **Triple-Tier-Modell** umgestellt: I. Active Travel & Alpine Expert · II. Behavioral & Harmony Coaching · III. Elite Relief & Emergency Support. Ski+Care ist jetzt Teil von Tier I, pädagogische Tiefe ist eigenständiger Tier II.
- **Begründung:** SGs Eigenformulierung (WhatsApp 2026-05-17). Bildet die tatsächliche Leistungsstaffelung besser ab als die alte geografisch/situativ geteilte Struktur. Korrespondiert mit Positionierung und Content Pillars.

## 2026-04-20 — Hero-Track: Premium-Nanny / Global Governess (konsolidiert)

- **Entscheidung:** Die drei vorgedachten Tracks (Global Governess · Confidence & Rehab Coach · Nature Resilience Mentor) werden auf **einen Hero-Track** konsolidiert: **Premium-Nanny / Global Governess**. Confidence- und Nature-Resilience-Facetten bleiben Teil des Profils, werden aber nicht als separate Angebote vermarktet.
- **Sekundäre Säulen:** (a) Nanny-Vertretung/Relief für Familien mit bestehender Live-in-Nanny, (b) Ski + Care-Kombi in Zermatt in Kooperation mit Evolution Ski School (Ski-Teil unter deren Lizenz, Care-Teil unter SGs Marke).
- **Begründung:** Klare Botschaft nach außen, eine Buchungseinheit, kein Paket-Wirrwarr. Drei-Tracks-Architektur war strategisch wertvoll, aber für Marke/Website zu komplex.

## 2026-04-20 — Website-Primärsprache: Englisch

- **Entscheidung:** Website-Primärsprache ist **Englisch**. Deutsch und Französisch werden via DeepL übersetzt gepflegt.
- **Begründung:** Zielgruppe ist international und mobil (HNW-Familien). Englisch ist der kleinste gemeinsame Nenner; SG baut ohnehin ihr Englisch aus. Korrigiert damit die frühere Entscheidung „DE primär, EN sekundär".

## 2026-04-20 — Richtpreise „ab CHF" werden auf der Website ausgewiesen

- **Entscheidung:** Auf der Website werden **Richtpreise („ab CHF …")** pro Leistungsbaustein ausgewiesen — keine Preistabelle, keine Paket-Matrix.
- **Begründung:** Zwei Effekte: Premium-Signal und Vorfilter gegen unpassende Anfragen. SG war zunächst gegen Preisangaben, wurde im Call überzeugt. Konkrete Zahlen folgen nach Richtpreis-Kalkulation.

## 2026-04-20 — Qualifizierungs-/Erstgespräch vor jeder Buchung

- **Entscheidung:** Jede Buchung wird über ein beiderseitig verpflichtendes **Qualifizierungsgespräch** eingeleitet. SG behält sich explizit vor, Aufträge abzulehnen.
- **Begründung:** Schutz der Marke, Schutz von SG, und Matching-Qualität. Passt zu Premium-Positionierung und Richtpreis-Logik.

## 2026-04-20 — Rechtliche Trennung Nanny ↔ Ski

- **Entscheidung:** Ski-Begleitung in Zermatt läuft **ausschließlich** über Evolution Ski School (Fabrizio Pavan) und wird dort abgerechnet. Der Nanny-/Care-Teil läuft unter SGs Marke. Eigenständiges Ski-Unterrichten unter SGs Marke in Zermatt ist nicht zulässig.
- **Begründung:** Klare Aussage des Partners; ohne diese Trennung gefährdet SG den Standortzugang. Provisionsmodell mit Fabrizio ist separat zu verhandeln.

## 2026-04-20 — Zielgruppen-Ansprache: nicht diagnostisch

- **Entscheidung:** Die Website adressiert Kinder mit Besonderheiten (Individualismus bis Asperger-/Autismus-Spektrum, Allergien, Reizempfindlichkeit) **nicht über Diagnose-Labels**, sondern über Leistungsversprechen (Ruhe, andere Ansprache, Wohlgefühl, Druck rausnehmen, beobachten statt funktionieren). Personenzentrierte Sprache durchgängig.
- **Begründung:** SGs klare Haltung: kein Stigmatisierungs-Vokabular, keine defizitäre Sprache. Trotzdem fachlicher Tiefgang sichtbar — über den Stil, nicht über Labels.

## 2026-04-20 — B2B-Bereich mit Agentur-Logos und Reciprocal Linking

- **Entscheidung:** Die Website erhält einen eigenen **B2B-Bereich** mit Booking-Pfad für Agenturen. Zielgruppe in der Ansprache: **Duke & Duchess**, **Tiziana Di Gento**, **Morgan & Mallet**, **Nanny4YourKid**. Deren Logos werden (nach Freigabe) auf der Homepage platziert; im Gegenzug wird Gegen-Verlinkung angestrebt.
- **Begründung:** „Vorschussvertrauen" für Endkund:innen plus Sichtbarkeits-/Entitäts-Signal für Suchmaschinen und LLMs.

## 2026-04-20 — Kontaktkanäle und Marken-Profile

- **Entscheidung:** Kontaktpfade: Kontaktformular · Domain-E-Mail · **WhatsApp Business** (separates Markenprofil) · separate Telefonnummer. Social-Media-Profile (Instagram, Facebook) laufen unter der **Marke**, nicht privat.
- **Begründung:** Niederschwellige Kontaktaufnahme und klare Trennung privat/geschäftlich. WhatsApp Business ermöglicht professionelles Profilbild, Öffnungszeiten und automatisierte Antworten.

## 2026-04-20 — Offline-Assets: Visitenkarten + halber A5-Flyer für Concierges

- **Entscheidung:** Erste Offline-Assets sind Visitenkarten und ein halber A5-Flyer (einmal gefaltet, taschentauglich) für Zermatt-Concierges. Digital und gedruckt verfügbar. Erster Canva-Entwurf über Chris (Felix' Firma), sobald Marke steht.
- **Begründung:** Concierges sind lokaler Multiplikator — wenn sie die Marke nicht kennen, brauchen sie etwas Greifbares zum Weiterreichen.

## 2026-04-20 — Nordstern 6 Monate

- **Entscheidung:** Nordstern für die ersten 6 Monate: **erster internationaler Einsatz im August/September 2026** ODER **etablierte wiederkehrende Nanny-Vertretungen** (Relief für Live-in-Nannies).
- **Begründung:** Beide Varianten beweisen Tragfähigkeit des Modells. Einkommenszielrahmen ~8.000 CHF/Monat Umsatz bleibt Arbeitshypothese; Detail (brutto/netto, Tage, Spesen) wird nach erstem Einsatz kalibriert.

## 2026-04-20 — Markenname: Brainstorming mit LLM, kurzfristige Entscheidung

- **Entscheidung:** Markenname und Domain (`.com` oder `.ch`) werden per LLM-gestütztem Brainstorming in `brand/name.md` erarbeitet. Eigenständiger Markenname (kein „SG | Untertitel").
- **Begründung:** Name blockiert Website, E-Mail, Social-Profile und Druckmaterial. Eigenständiger Name unterstützt B2B-Anmutung und perspektivisch eigene Nanny-Ausbildung unter der Marke.

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

## 2026-04-18 — Sprache: DE primär, EN sekundär ~~(abgelöst am 2026-04-20)~~

- **Entscheidung:** Website und Content auf Deutsch (primär) und Englisch (sekundär). Code und technische Kommentare ausschließlich Englisch.
- **Begründung:** "Internationale Nanny" adressiert explizit auch nicht-deutschsprachige Familien. Zweisprachigkeit bewusst einplanen (beeinflusst Tech-Stack-Wahl in Phase 5).
- **Status:** Abgelöst durch Entscheidung vom 2026-04-20 (EN primär, DE+FR sekundär). Code bleibt englisch.

## 2026-04-18 — CI/CD entfernt

- **Entscheidung:** `.github/workflows/ci.yml` (JF-Hospitality Docker-Deploy-Template) entfernt.
- **Begründung:** Nichts zu bauen/deployen in Konzeptphase. Wird mit Website-Projekt in Phase 5 neu eingerichtet, passend zum gewählten Tech-Stack.
