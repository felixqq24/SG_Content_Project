# Implementierungsplan: SEO & Schema.org Erweiterungen

Dieses Dokument beschreibt die technischen Schritte zur Umsetzung der Empfehlungen aus dem Senior-Review (Phase 2 - Erweiterung).

---

## 1. Automatisierung der Sitemap
**Ziel:** Ersetzung der manuellen `sitemap.xml` durch ein automatisiertes Plugin, um bei neuen Seiten (z.B. im Content-Hub) eine korrekte Indexierung sicherzustellen.

### Technische Schritte:
1.  **Dependency Installation:**
    ```bash
    pnpm add @astrojs/sitemap
    ```
2.  **Konfiguration anpassen (`website/astro.config.mjs`):**
    - Import des Plugins: `import sitemap from '@astrojs/sitemap';`
    - Hinzufügen zum `plugins`-Array: `plugins: [sitemap()]`.
    - Sicherstellen, dass die `site` Property (URL) korrekt gesetzt ist.
3.  **Cleanup:**
    - Löschen der manuellen Datei `website/public/sitemap.xml`.

### Verifikation:
- [ ] `pnpm build` ausführen.
- [ ] Prüfen, ob im `dist/` Verzeichnis eine automatisch generierte `sitemap-index.xml` oder `sitemap-0.xml` existiert.
- [ ] URL-Check: `https://rivieraandridge.com/sitemap-0.xml` aufrufen.

---

## 2. Schema.org Expansion (Local Business / Professional Service)
**Ziel:** Erhöhung der Sichtbarkeit in den Google "Local Pack" und Rich Snippets durch detailliertere semantische Daten.

### Technische Schritte:
1.  **Implementierung in `website/src/pages/index.astro` (oder `about.astro`):**
    - Hinzufügen eines `<script type="application/ld+json">` Blocks.
    - Verwendung des Typs `ProfessionalService` (spezifischer als `LocalBusiness` für Dienstleister).

2.  **Datenpunkte (Definition):**
    - `@type`: `ProfessionalService`
    - `name`: `Riviera & Ridge`
    - `image`: URL zum Hauptbild (Hero-Image).
    - `address`:
        - `@type`: `PostalAddress`
        - `streetAddress`: (Falls bekannt, sonst weglassen)
        - `addressLocality`: `Zermatt`
        - `addressRegion`: `Valais`
        - `postalCode`: `3920`
        - `addressCountry`: `CH`
    - `geo`:
        - `@type`: `GeoCoordinates`
        - `latitude`: (Koordinaten von Zermatt)
        - `longitude`: (Koordinaten von Zermatt)
    - `priceRange`: `$$` (oder entsprechend dem Premium-Segment)
    - `telephone`: (Falls vorhanden)
    - `openingHours`: `Mo-Fr 09:00-18:00` (Beispiel)
    - `url`: `https://rivieraandridge.com`

### Verifikation:
- [ ] Validierung des Codes mit dem [Google Rich Results Test](https://search.google.com/test/rich-results).
- [ ] Prüfung der korrekten Darstellung der Daten in den Suchergebnissen (simuliert).

---

## Zeitplan & Priorität

| Aufgabe | Priorität | Aufwand | Abhängigkeit |
| :--- | :--- | :--- | :--- |
| Sitemap Automatisierung | 🟢 Niedrig | Sehr gering | Keine |
| Schema.org Expansion | 🟢 Niedrig | Gering | Keine |

**Status:** Bereit zur Umsetzung.
