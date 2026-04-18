#!/usr/bin/env bash
# JF Project Template — Init Script
# Ersetzt alle {{PLATZHALTER}} in Template-Dateien.
# Einmalig ausführen nach "Use this template" → Repo klonen.
# Das Script löscht sich nach erfolgreicher Ausführung selbst.

set -euo pipefail

# ── Eingaben ────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════╗"
echo "║   JF Project Template — Init         ║"
echo "╚══════════════════════════════════════╝"
echo ""

read -rp "Projektname (z.B. quotering-api): " PROJECT_NAME
read -rp "Kurzbeschreibung (1 Satz): " PROJECT_DESCRIPTION
read -rp "Domain/URL (z.B. app.quotering.de): " PROJECT_DOMAIN
read -rp "Deploy-Verzeichnis (default: /opt/apps/${PROJECT_NAME}): " DEPLOY_DIR
DEPLOY_DIR="${DEPLOY_DIR:-/opt/apps/${PROJECT_NAME}}"

CURRENT_DATE=$(date +"%Y-%m-%d")

echo ""
echo "→ Ersetze Platzhalter in Template-Dateien..."

# ── Dateien mit Platzhaltern ────────────────────────────────
FILES=(
  "README.md"
  ".github/copilot-instructions.md"
  ".github/workflows/ci.yml"
  ".env.example"
  "docs/engineering_guidelines.md"
  "docs/e2e_testing_guidelines.md"
  "docs/ui_ux_guidelines.md"
  "docs/incident-response.md"
)

for FILE in "${FILES[@]}"; do
  if [ -f "$FILE" ]; then
    perl -pi -e "s/\\{\\{PROJEKT\\}\\}/${PROJECT_NAME}/g" "$FILE"
    perl -pi -e "s/\\{\\{DATUM\\}\\}/${CURRENT_DATE}/g" "$FILE"
    perl -pi -e "s/\\{\\{DOMAIN\\}\\}/${PROJECT_DOMAIN}/g" "$FILE"
    perl -pi -e "s|/opt/apps/\\{\\{PROJEKT\\}\\}|${DEPLOY_DIR}|g" "$FILE"
    echo "  ✓ ${FILE}"
  else
    echo "  ⚠ ${FILE} nicht gefunden — übersprungen"
  fi
done

# ── copilot-instructions.md: Beschreibung einfügen ─────────
perl -pi -e "s/<!-- TODO: Kurzbeschreibung einfügen -->/${PROJECT_DESCRIPTION}/g" \
  ".github/copilot-instructions.md"

echo ""
echo "→ Eintrag in project-knowledge.instructions.md..."
cat >> ".github/instructions/project-knowledge.instructions.md" << EOF

## Infrastructure

- Project name: ${PROJECT_NAME}
- Domain: ${PROJECT_DOMAIN}
- Deploy directory: ${DEPLOY_DIR}
- Init date: ${CURRENT_DATE}
EOF

echo ""
echo "✅ Init abgeschlossen."
echo ""
echo "Nächste Schritte:"
echo "  1. docs/architecture.md mit tatsächlicher Architektur befüllen"
echo "  2. docs/engineering_guidelines.md — Tech-Stack-Platzhalter ersetzen"
echo "  3. docs/e2e_testing_guidelines.md — Auth-Provider-Abschnitt anpassen"
echo "  4. .env.example — projektspezifische Variablen ergänzen"
echo "  5. README.md — Install/Dev/Test/Build Commands eintragen"
echo ""

# ── Self-destruct ────────────────────────────────────────────
read -rp "init.sh jetzt löschen? (empfohlen) [Y/n]: " DELETE_SELF
DELETE_SELF="${DELETE_SELF:-Y}"
if [[ "$DELETE_SELF" =~ ^[Yy]$ ]]; then
  rm -- "$0"
  echo "→ init.sh gelöscht."
fi
echo ""
