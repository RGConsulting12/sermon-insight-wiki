#!/usr/bin/env python3
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

from sermon_insight_wiki.cli import query_main  # noqa: E402

if __name__ == "__main__":
    query_main()
