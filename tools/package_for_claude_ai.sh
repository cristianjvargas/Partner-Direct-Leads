#!/usr/bin/env bash
# Package each skill in .claude/skills/ as a .zip for upload to a claude.ai
# account (Settings -> Capabilities -> Skills -> Upload skill).
#
# Repo-level skills in .claude/skills/ are picked up automatically by Claude Code
# sessions in this repo and need no packaging. Use this only when you also want
# the skills available account-wide on claude.ai (Claude apps, Cowork, other repos).
#
# Usage:
#   ./tools/package_for_claude_ai.sh            # package all skills
#   ./tools/package_for_claude_ai.sh merchant   # only skills matching "merchant"
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_ROOT/.claude/skills"
OUT="$REPO_ROOT/dist/skills"
FILTER="${1:-}"

command -v zip >/dev/null || { echo "error: 'zip' is not installed." >&2; exit 1; }
[ -d "$SRC" ] || { echo "error: $SRC not found." >&2; exit 1; }

mkdir -p "$OUT"
count=0

for dir in "$SRC"/*/; do
    name="$(basename "$dir")"
    [ -f "$dir/SKILL.md" ] || { echo "  skip $name (no SKILL.md)"; continue; }
    if [ -n "$FILTER" ] && [[ "$name" != *"$FILTER"* ]]; then continue; fi

    # claude.ai requires SKILL.md at the root of a folder named for the skill.
    rm -f "$OUT/$name.zip"
    ( cd "$SRC" && zip -q -r "$OUT/$name.zip" "$name" \
        -x '*/__pycache__/*' '*.pyc' '*/.DS_Store' )
    printf "  packaged %-32s %s\n" "$name" "$(du -h "$OUT/$name.zip" | cut -f1)"
    count=$((count + 1))
done

echo
echo "$count skill(s) written to dist/skills/"
echo "Upload at: claude.ai -> Settings -> Capabilities -> Skills -> Upload skill"
