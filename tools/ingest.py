#!/usr/bin/env python3
"""Wrapper: python tools/ingest.py <transcript.txt>"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

from sermon_insight_wiki.wiki_ingest import ingest_transcript_path  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/ingest.py <transcript.txt> [video_id]")
        sys.exit(2)
    ingest_transcript_path(Path(sys.argv[1]), video_id=sys.argv[2] if len(sys.argv) > 2 else None)


if __name__ == "__main__":
    main()
