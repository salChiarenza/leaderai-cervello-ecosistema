#!/usr/bin/env bash
# Hook UserPromptSubmit condiviso Claude Code + Codex.
# Inietta nel contesto dell'agente le ultime modifiche a AGENT_CHAT.md (radice della casa)
# se il file e' stato toccato negli ultimi WINDOW_MIN minuti.
# Cosi' i due agenti vedono in tempo reale le note dell'altro senza dover rileggere a mano.

set -euo pipefail

CASA="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
CHAT="$CASA/AGENT_CHAT.md"
WINDOW_MIN=60
LINES=40

if [ ! -f "$CHAT" ]; then
  exit 0
fi

# Se il file non e' stato modificato di recente, niente da iniettare
if [ -z "$(find "$CHAT" -mmin -$WINDOW_MIN 2>/dev/null)" ]; then
  exit 0
fi

CONTENT="$(head -n $LINES "$CHAT")"
LAST_MOD="$(stat -f '%Sm' -t '%Y-%m-%d %H:%M' "$CHAT")"

# Output JSON compatibile con UserPromptSubmit di Claude Code e Codex CLI.
# Entrambi accettano hookSpecificOutput.additionalContext.
HEADER="AGENT_CHAT.md modificata di recente (ultima: $LAST_MOD). Prime $LINES righe del file:"

if command -v jq >/dev/null 2>&1; then
  jq -n \
    --arg header "$HEADER" \
    --arg content "$CONTENT" \
    '{
      "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": ($header + "\n\n" + $content)
      }
    }'
else
  # Fallback senza jq: escape minimo
  ESC_CONTENT=$(printf '%s' "$CONTENT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')
  ESC_HEADER=$(printf '%s' "$HEADER" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')
  printf '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":%s}}\n' \
    "$(python3 -c "import json,sys; print(json.dumps(${ESC_HEADER}+chr(10)+chr(10)+${ESC_CONTENT}))")"
fi
