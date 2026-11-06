#!/usr/bin/env bash
# Creates a disposable demo repository, a local bare origin, tracker and worktree folders,
# and the agent prompt for the historical macOS first-use check. Existing paths are refused.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

ROOT="${1:-$HOME/adaptive-sdd-mac-test}"
SHA="${2:-1d91d9448621c29e39c248bf1c1f23a098ecb02d}"
HERE="$(cd "$(dirname "$0")" && pwd)"

# Resolve before creating anything; never delete or reuse a caller-supplied directory.
ROOT="$(python3 - "$ROOT" "$HOME" <<'PY'
from pathlib import Path
import sys
requested = Path(sys.argv[1]).expanduser()
home = Path(sys.argv[2]).resolve(strict=True)
target = requested.resolve()
if requested.exists() or requested.is_symlink() or target == home or home not in target.parents:
    raise SystemExit("ROOT must be a new directory strictly below HOME")
print(target)
PY
)"
mkdir "$ROOT"
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

printf '__pycache__/\n' > .gitignore

git init -q -b main
git add -A
git -c user.name=demo -c user.email=demo@example.invalid commit -qm "initial demo"
git init -q --bare "$ROOT/remote.git"
git remote add origin "$ROOT/remote.git"
git push -q origin main
python3 -m unittest discover -s tests -t . 2>&1 | tail -1

python3 - "$HERE/prompt.template.md" "$ROOT" "$SHA" <<'PY'
from pathlib import Path
import sys
source, root, sha = sys.argv[1:]
text = Path(source).read_text(encoding="utf-8")
(Path(root) / "prompt.md").write_text(text.replace("__ROOT__", root).replace("__SHA__", sha), encoding="utf-8")
PY
echo "ready: $ROOT"
echo "next: cd \"$ROOT/sample\" && claude --add-dir \"$ROOT\"   (then paste $ROOT/prompt.md)"
