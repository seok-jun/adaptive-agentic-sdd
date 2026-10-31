#!/usr/bin/env bash
# Creates a disposable demo repository, a local bare origin, tracker and worktree folders,
# and the agent prompt for the macOS first-use check. Safe to rerun: it replaces $ROOT.
set -euo pipefail

ROOT="${1:-$HOME/adaptive-sdd-mac-test}"
SHA="${2:-1d91d9448621c29e39c248bf1c1f23a098ecb02d}"
HERE="$(cd "$(dirname "$0")" && pwd)"

case "$ROOT" in
  "$HOME"/*) ;;
  *) echo "ROOT must be under \$HOME: $ROOT" >&2; exit 2 ;;
esac

rm -rf "$ROOT"
mkdir -p "$ROOT/sample/catalog" "$ROOT/sample/members" "$ROOT/sample/tests/catalog" "$ROOT/sample/tests/members" "$ROOT/tracker" "$ROOT/wt"
cd "$ROOT/sample"
touch catalog/__init__.py members/__init__.py tests/__init__.py tests/catalog/__init__.py tests/members/__init__.py

cat > catalog/search.py <<'EOF'
"""Catalog search helpers."""


def page(items, number, size):
    """Return page `number` (1-based) of `items`, `size` items per page."""
    if number < 1 or size < 1:
        raise ValueError("number and size must be positive")
    start = (number - 1) * size
    end = start + size - 1
    return items[start:end]
EOF

cat > members/registry.py <<'EOF'
"""Member registry."""


def normalize_email(email):
    return email.strip().lower()
EOF

cat > tests/catalog/test_search.py <<'EOF'
import unittest

from catalog.search import page


class PageTests(unittest.TestCase):
    def test_rejects_non_positive(self):
        with self.assertRaises(ValueError):
            page([1, 2, 3], 0, 2)
EOF

cat > tests/members/test_registry.py <<'EOF'
import unittest

from members.registry import normalize_email


class NormalizeTests(unittest.TestCase):
    def test_strips_and_lowercases(self):
        self.assertEqual(normalize_email("  A@B.COM "), "a@b.com")
EOF

printf '# Library demo\n\nModules: `catalog/` (search), `members/` (registry).\n\nTests: `python3 -m unittest discover -s tests -t .`\n' > README.md
printf '# Agent notes\n\nKeep changes small and add a regression test for every bug fix.\n' > AGENTS.md

git init -q -b main
git add -A
git -c user.name=demo -c user.email=demo@example.invalid commit -qm "initial demo"
git init -q --bare "$ROOT/remote.git"
git remote add origin "$ROOT/remote.git"
git push -q origin main
python3 -m unittest discover -s tests -t . 2>&1 | tail -1

sed -e "s#__ROOT__#$ROOT#g" -e "s#__SHA__#$SHA#g" "$HERE/prompt.template.md" > "$ROOT/prompt.md"
echo "ready: $ROOT"
echo "next: cd \"$ROOT/sample\" && claude --add-dir \"$ROOT\"   (then paste $ROOT/prompt.md)"
