# UI/UX Guidelines — SG_Content_Projekt

> Stand: 2026-04-18

Diese Guidelines definieren grundlegende UI/UX-Prinzipien und konkrete Patterns für SG_Content_Projekt.  
Sie sind bewusst leichtgewichtig gehalten und sollen Entscheidungen beschleunigen, Konsistenz fördern und spätere Erweiterungen vereinfachen.  

---

## 1. Ziele und Scope

- **Zielgruppe:** <!-- TODO: Zielgruppe beschreiben, z. B. "Interne JF-Nutzung und Power-User, primär Desktop" -->
- **Ziel:** <!-- TODO: Kernziel der UI beschreiben, z. B. "Schnelles Erfassen und Bearbeiten von Daten mit klaren Workflows und minimaler kognitiver Last" -->
- **Scope dieser Guidelines:**  
  - Layout & Navigation  
  - Komponenten-Standards (Buttons, Formulare, Modals)  
  - Zustände & Feedback (Loading, Empty, Error, Realtime)  
  - Text & Microcopy  
  - UX-Prinzipien speziell für interne Tools  

Branding, Farbpalette und detaillierte Typografie orientieren sich an den bestehenden JF-Designentscheidungen und den Defaults von Tailwind/shadcn/ui.  

---

## 2. Design-Prinzipien

1. **Workflows vor „Schönheit"**  
   Entscheidungen orientieren sich primär an Geschwindigkeit und Klarheit der täglichen Arbeit, nicht an maximalem visuellen „Wow". Interne Tools profitieren stärker von Effizienz und Fehlervermeidung als von dekorativer Ästhetik.  

2. **Konsistenz schlägt Individualität**  
   Gleiche Aktionen sehen überall gleich aus und verhalten sich gleich (z. B. Primär-Button, Confirm-Pattern, Error-Darstellung). Design-Systeme empfehlen klar dokumentierte, wiederverwendbare Patterns, um die kognitive Last zu reduzieren.  

3. **Klarheit vor Komplexität**  
   Informationen werden nach Relevanz gestaffelt: Primäre Inhalte prominent, sekundäre in Tabs, Accordions oder „More"-Bereichen. Klare visuelle Hierarchie (Typografie, Kontrast, Spacing) erleichtert das Scannen von Informationen.  

4. **Fehler früh und klar kommunizieren**  
   Formulare verwenden Inline-Validierung, verständliche Fehlermeldungen und konkrete Handlungsempfehlungen. Fehler sollten möglichst nah an der Interaktion kommuniziert werden.  

5. **Feedback auf jede Nutzeraktion**  
   Jede relevante Aktion (Erstellen, Speichern, Verschieben, Senden) erhält visuelles Feedback (Loading-Indicator, State-Änderung, Toast). Klare Rückmeldungen sind zentral für wahrgenommene Performance und Vertrauenswürdigkeit.  

6. **„Safe Defaults" und Undo, wo sinnvoll**  
   Statt harter Löschungen bevorzugen wir Archivierung oder „Soft Delete" mit Möglichkeit zur Wiederherstellung, sofern technisch vertretbar. Kritische Aktionen sollen abgesichert und wenn möglich reversibel sein.  

---

## 3. Layout & Navigation

### 3.1. Grundlayout

- **Desktop-first:**  
  <!-- TODO: Zielplattform beschreiben --> Die Applikation ist primär für Desktop-Bildschirme ausgelegt, Mobile-Optimierung ist Post-MVP.  
- **Layout-Prinzip:**  
  - Linke Sidebar: globale Navigation (z. B. Hauptbereiche, Projekte, Views).  
  - Hauptbereich: primäre Inhaltsanzeige (Listen, Detail-Views, Dashboards).  
  - Optionale rechte Sidebar: zusätzliche Kontextinfos (z. B. Details, Chat, Activity).  
  Dieses Drei-Spalten-Muster ist Nutzern vertraut und skaliert gut.  

### 3.2. Navigation

- **Primäre Navigation:**  
  <!-- TODO: Hauptnavigation definieren, z. B. Projektauswahl, Views, Notifications -->
- **Sekundäre Navigation:**  
  Tabs innerhalb eines Bereichs, falls notwendig.  
- **Breadcrumbs:**  
  <!-- TODO: Breadcrumb-Struktur definieren, z. B. "Bereich / Unterkategorie / Detail" -->
  Breadcrumbs sind klickbar und dienen als schnelle Navigation zurück.  

---

## 4. Komponenten-Standards

### 4.1. Buttons

- **Varianten**  
  - Primary: für wichtigste Aktion auf einem Screen (z. B. „Erstellen", „Speichern").  
  - Secondary: weniger kritische Aktionen (z. B. „Abbrechen", „Filter zurücksetzen").  
  - Destructive: in Rot, nur für Aktionen mit Datenverlust (z. B. „Löschen").  

- **Positionierung**  
  - In Formularen: Primary auf der rechten Seite, Secondary/Cancel links davon.  
  - In Dialogen: Destructive rechts, Cancel links.  

### 4.2. Formulare

- **Labels & Inputs**  
  - Labels immer sichtbar, nicht als Placeholder-Ersatz.  
  - Pflichtfelder mit `*` kennzeichnen und in der Fehlerbeschreibung erklären.  
  - Feldreihenfolge entspricht mentalem Modell des Users.  

- **Validation**  
  - Inline-Validierung bei Blur oder nach Submit; Fehler unter dem Feld mit klarer Erklärung.  
  - Keine rein farbbasierte Fehlermarkierung (zusätzliche Icons/Text zur Barrierefreiheit).  

### 4.3. Modals, Drawer, Seiten

- **Modal**  
  - Für kleinere, fokussierte Aktionen (z. B. Erstellen, schnelle Bearbeitung).  
- **Drawer (rechte Sidebar)**  
  - Für Detailanzeigen, die gleichzeitig Kontext im Hintergrund behalten sollen.  
- **Eigene Seite**  
  - Für komplexe oder kritische Prozesse (z. B. Einstellungen, Admin-Bereiche).  

### 4.4. Tabellen & Listen

- **Tabellen**  
  <!-- TODO: Spalten und Sortierung projektspezifisch definieren -->
  - Sortierbar nach relevanten Feldern.  
  - Sticky Header bei vielen Einträgen.  

- **Responsive Verhalten**  
  - Für kleinere Viewports: weniger kritische Spalten ausblenden oder als Stack untereinander anzeigen.  

<!-- Optional: Boards (Kanban) — falls zutreffend -->
<!--
### 4.5. Boards (Kanban)

- **Columns**
  - Standard-Spalten (z. B. Backlog, In Progress, Review, Done), konfigurierbar.
- **Cards**
  - Zeigen: Schlüsselinfo (ID, Titel, Status, Assignee).
  - Drag-and-Drop ändert Status und speichert sofort, mit kurzem „Saved"-Feedback.
-->

---

## 5. Zustände & Feedback

### 5.1. Loading-Zustände

- **Page-Level Loading**  
  - Skeletons für zentrale Bereiche, kein globaler Spinner.  
- **Inline Loading**  
  - Buttons zeigen Spinner + Disabled, wenn eine Aktion läuft (z. B. „Speichern…").  

### 5.2. Empty States

- **Leere Listen/Bereiche**  
  - Kurze Erklärung (z. B. „Noch keine Einträge.") + prominente CTAs (z. B. „Erstellen").  
- **Leere Filter-Ergebnisse**  
  - Hinweis, dass ein Filter aktiv ist und einfache Möglichkeit, Filter zurückzusetzen.  

### 5.3. Error States

- **Form-Fehler**  
  - Direkt am Feld, mit kurzer Ursache und Handlungsanweisung.  
- **API-/Netzwerkfehler**  
  - Toast oder Inline-Alert: „Aktion konnte nicht gespeichert werden. Bitte erneut versuchen."  
  - Bei dauerhaften Fehlern: Option „Details anzeigen" mit technischer Info (für interne Nutzer).  

### 5.4. Realtime-Feedback (falls zutreffend)

<!-- TODO: Falls die App Realtime-Features nutzt (WebSocket, SSE), Feedback-Patterns hier dokumentieren -->
<!-- Beispiele: -->
<!-- - Neue Daten erscheinen ohne Reload (z. B. Chat-Messages, Live-Updates) -->
<!-- - Dezente Hinweise wenn sich geöffnete Daten extern ändern ("Wurde aktualisiert — Änderungen anzeigen") -->

---

## 6. Text & Microcopy

- **Sprache & Ton**  
  - Klar, knapp, professionell; keine „verspielten" Fehlermeldungen.  
  - Terminologie konsistent innerhalb der App und mit der restlichen JF-Suite.  

- **Buttons**  
  - Vermeide generische Labels: statt „OK" lieber „Speichern", statt „Abschicken" lieber konkrete Aktion benennen.  

- **Bestätigungsdialoge**  
  - Text beschreibt Aktion + Konsequenz, z. B. „Dieses Element wird archiviert und nicht mehr in der Übersicht angezeigt. Du kannst es später wiederherstellen."  

---

## 7. UX-Prinzipien für interne Tools

Diese Punkte gelten speziell für JF-interne/halb-interne Werkzeuge:

1. **Optimize for Speed**  
   - Tastaturkürzel für häufige Aktionen.  
   - Fokus-Management: Nach „Erstellen" Fokus auf sinnvolles Feld, nach Speichern auf nächstem Element.  

2. **Information Density „Medium"**  
   - Höhere Informationsdichte als bei öffentlich vermarkteten Produkten ist zulässig, solange Lesbarkeit und Struktur gewahrt bleiben.  
   - Lange Tabellen und komplexe Views sind erlaubt, wenn Filter und Sortierung gut nutzbar sind.  

3. **Fehlerprävention statt Fehlerbehebung**  
   - Kritische Aktionen immer mit Confirm-Dialog und klarer Warnung.  
   - Wo möglich, Defaults so wählen, dass sie „sichere" Entscheidungen fördern.  

---

## 8. Barrierefreiheit & Basis-Standards

- **Kontrast & Farben**  
  - Mindestens WCAG AA für Text/Icons anstreben, insbesondere bei Status-Badges und Buttons.  
- **Fokuszustände**  
  - Alle interaktiven Elemente haben sichtbare Fokuszustände (nicht entfernt, auch wenn standardmäßig unschön).  
- **Semantik**  
  - Überschriften/Listen/Buttons korrekt semantisch markieren, damit Screenreader funktionieren und Keyboard-Navigation stabil bleibt.  

Auch wenn das Tool primär intern genutzt wird, sollten diese Basisstandards eingehalten werden, um die Nutzbarkeit zu erhöhen und spätere Erweiterungen zu erleichtern.  
