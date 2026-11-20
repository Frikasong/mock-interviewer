#!/usr/bin/env bash
# Install the interview-prep skill into any AI agent that reads Agent Skills (SKILL.md).
# 把 interview-prep skill 装进任何支持 Agent Skills（SKILL.md）的 AI 工具。
#
#   ./install.sh                      Chinese edition, into every agent found on this computer
#   ./install.sh en                   English edition
#   ./install.sh en codex gemini      only into the agents you name
#   ./install.sh --list               show supported agents and where each one reads skills
#
# Agents: claude codex gemini copilot cursor opencode goose amp windsurf
# Any other tool: ./install.sh en --dir /path/to/its/skills
set -euo pipefail
cd "$(dirname "$0")"

# agent | folder it reads skills from | folder whose existence means it is installed
AGENTS=(
  "claude|$HOME/.claude/skills|$HOME/.claude"
  "codex|$HOME/.codex/skills|$HOME/.codex"
  "gemini|$HOME/.gemini/skills|$HOME/.gemini"
  "copilot|$HOME/.copilot/skills|$HOME/.copilot"
  "cursor|$HOME/.cursor/skills|$HOME/.cursor"
  "opencode|$HOME/.config/opencode/skills|$HOME/.config/opencode"
  "goose|$HOME/.config/goose/skills|$HOME/.config/goose"
  "amp|$HOME/.config/agents/skills|$HOME/.config/agents"
  "windsurf|$HOME/.codeium/windsurf/skills|$HOME/.codeium/windsurf"
)

LANG_CHOICE="zh"; WANT=(); CUSTOM=""; FORCE=0
while [ $# -gt 0 ]; do
  case "$1" in
    zh|中文) LANG_CHOICE="zh" ;;
    en|english) LANG_CHOICE="en" ;;
    --dir) CUSTOM="${2:?--dir needs a path}"; shift ;;
    -y|--yes) FORCE=1 ;;
    --list)
      printf "%-10s %s\n" agent "skills folder"
      for a in "${AGENTS[@]}"; do IFS='|' read -r n d _ <<<"$a"; printf "%-10s %s\n" "$n" "$d"; done
      exit 0 ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) WANT+=("$1") ;;
  esac
  shift
done

if [ "$LANG_CHOICE" = "en" ]; then SRC="skills/interview-prep"; NAME="interview-prep"; OTHER="interview-prep-zh"
else SRC="skills/interview-prep-zh"; NAME="interview-prep-zh"; OTHER="interview-prep"; fi
[ -f "$SRC/SKILL.md" ] || { echo "Cannot find $SRC — run this from the repository root."; exit 1; }

TARGETS=()
if [ -n "$CUSTOM" ]; then
  TARGETS+=("custom|$CUSTOM")
elif [ ${#WANT[@]} -gt 0 ]; then
  for w in "${WANT[@]}"; do
    hit=""
    for a in "${AGENTS[@]}"; do IFS='|' read -r n d _ <<<"$a"; [ "$n" = "$w" ] && hit="$n|$d"; done
    [ -n "$hit" ] || { echo "Unknown agent: $w (see ./install.sh --list)"; exit 1; }
    TARGETS+=("$hit")
  done
else
  for a in "${AGENTS[@]}"; do IFS='|' read -r n d home <<<"$a"; [ -d "$home" ] && TARGETS+=("$n|$d"); done
  if [ ${#TARGETS[@]} -eq 0 ]; then
    echo "No supported AI agent found in your home folder."
    echo "Name one (./install.sh $LANG_CHOICE codex), or give its skills folder (./install.sh $LANG_CHOICE --dir PATH)."
    echo "Using a chat website instead? Paste portable/$NAME.md into the chat — no install needed."
    exit 1
  fi
fi

ask() { [ "$FORCE" = 1 ] && return 0; read -r -p "$1 [y/N] " a; [[ "$a" =~ ^[Yy]$ ]]; }

DONE=()
for t in "${TARGETS[@]}"; do
  IFS='|' read -r agent dest <<<"$t"
  mkdir -p "$dest"
  # The two editions answer the same requests; keep one per agent.
  if [ -d "$dest/$OTHER" ] && ask "[$agent] $OTHER is installed too and will compete with $NAME. Remove it?"; then
    rm -rf "${dest:?}/$OTHER"
  fi
  if [ -d "$dest/$NAME" ]; then
    ask "[$agent] $NAME is already installed. Replace it?" || { echo "[$agent] skipped"; continue; }
    rm -rf "${dest:?}/$NAME"
  fi
  cp -R "$SRC" "$dest/$NAME"
  DONE+=("$agent → $dest/$NAME")
done

echo
if [ ${#DONE[@]} -eq 0 ]; then echo "Nothing installed."; exit 0; fi
echo "Installed $NAME:"
for d in "${DONE[@]}"; do echo "  $d"; done
cat <<EOF

Next: restart the agent, then just describe your situation — no need to name the skill:
  "I'm interviewing at <employer> for <role> next Thursday, here's the posting."
  「我下周四面 XX 公司的 XX 岗，这是 job posting」

The practice tool needs no install: open interviewer/index.html in Chrome.
EOF
