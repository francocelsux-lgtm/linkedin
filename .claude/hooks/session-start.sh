#!/bin/bash
# Session Start Hook — LinkedIn Posts Workspace
# Runs automatically at the start of every Claude Code session.
# Powered by the session-start-hook skill.
set -euo pipefail

# Only run full setup in remote/web sessions
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

echo "=== LinkedIn Posts — Session Start ==="

# Print today's date for context
echo "Date: $(date '+%Y-%m-%d %A')"

# Show current repo structure as a quick orientation
echo ""
echo "--- Skill Files ---"
ls "$CLAUDE_PROJECT_DIR"/*.md 2>/dev/null || echo "(none found)"

# Show memory folder if it exists
if [ -d "$CLAUDE_PROJECT_DIR/memory" ]; then
  echo ""
  echo "--- Memory Entries ---"
  echo "Posts logged: $(find "$CLAUDE_PROJECT_DIR/memory/posts" -name '*.md' 2>/dev/null | wc -l)"
  echo "Weekly logs:  $(find "$CLAUDE_PROJECT_DIR/memory/weekly-logs" -name '*.md' 2>/dev/null | wc -l)"
  echo "Monthly logs: $(find "$CLAUDE_PROJECT_DIR/memory/monthly-logs" -name '*.md' 2>/dev/null | wc -l)"
fi


# Show HubSpot context if available
HUBSPOT_CONTEXT="$CLAUDE_PROJECT_DIR/data/hubspot/context.md"
if [ -f "$HUBSPOT_CONTEXT" ]; then
  echo ""
  echo "--- HubSpot CRM ---"
  # Show first meaningful line (skip header and blank lines)
  grep -E "^##" "$HUBSPOT_CONTEXT" | head -4 | sed 's/^## /  /'
  # Check if synced or placeholder
  if grep -q "Sin sincronizar" "$HUBSPOT_CONTEXT" 2>/dev/null; then
    echo "  ⚠ Sin sincronizar — correr: python scripts/hubspot_sync.py"
  else
    SYNC_DATE=$(grep "_Última sincronización" "$HUBSPOT_CONTEXT" | sed "s/.*: //" | sed "s/ (.*//" || echo "desconocida")
    echo "  Última sync: $SYNC_DATE"
  fi
fi

echo ""
echo "Available slash commands:"
ls "$CLAUDE_PROJECT_DIR/.claude/commands/"*.md 2>/dev/null | xargs -I{} basename {} .md | sed 's/^/  \//' || echo "  (none yet)"

echo "=== Ready ==="
