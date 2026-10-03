#!/usr/bin/env bash
# 安装 interview-prep skill 到 Claude Code / Claude Desktop
#
#   ./install.sh          安装中文版
#   ./install.sh en       安装英文版
#
# 装完重启 Claude Code，然后直接说你的情况就行，例如：
#   「我下周四面 XX 公司的 XX 岗，这是 job posting」
set -euo pipefail
cd "$(dirname "$0")"

LANG_CHOICE="${1:-zh}"
case "$LANG_CHOICE" in
  zh|中文) SRC="skills/interview-prep-zh"; NAME="interview-prep-zh" ;;
  en|english) SRC="skills/interview-prep"; NAME="interview-prep" ;;
  *) echo "用法: ./install.sh [zh|en]"; exit 1 ;;
esac

# Claude Code 读 ~/.claude/skills，Claude Desktop 在 macOS 上也是这里
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

if [ ! -d "$SRC" ]; then
  echo "找不到 $SRC —— 请在仓库根目录运行这个脚本。"; exit 1
fi

mkdir -p "$DEST"

# 两个语言版本会抢同一批触发词，装一个就够了
OTHER="interview-prep"; [ "$NAME" = "interview-prep" ] && OTHER="interview-prep-zh"
if [ -d "$DEST/$OTHER" ]; then
  echo "检测到已安装 $OTHER。"
  echo "两个语言版本会互相抢触发，建议只留一个。"
  read -r -p "删掉 $OTHER 吗？[y/N] " a
  [[ "$a" =~ ^[Yy]$ ]] && rm -rf "${DEST:?}/$OTHER" && echo "  已删除 $OTHER"
fi

if [ -d "$DEST/$NAME" ]; then
  read -r -p "$NAME 已存在，覆盖？[y/N] " a
  [[ "$a" =~ ^[Yy]$ ]] || { echo "取消。"; exit 0; }
  rm -rf "${DEST:?}/$NAME"
fi

cp -R "$SRC" "$DEST/$NAME"

cat <<EOF

装好了：$DEST/$NAME

下一步
  1. 重启 Claude Code
  2. 直接说你的情况，不用点名这个 skill：
       我下周四面 XX 公司的 XX 岗，这是 job posting
       （把招聘启事粘上）
  3. 它会自己认出来该干什么

模拟面试器是另一个东西，不用安装：
  用 Chrome 打开 interviewer/index.html 就能跑。

EOF
