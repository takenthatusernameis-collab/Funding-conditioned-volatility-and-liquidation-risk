#!/usr/bin/env python3
"""
Exhaustive alternative source hunt for Track A observed liquidations (unauthenticated only)
Follows RESEARCH_PROMPT §5. Produces evidence tables with GO/NO-GO rubric scoring.
Strengthened for 004i: more source families, retry/backoff, rubric-scored assessment.
"""
# [HEAVY-004i session 4 (2026-11-04T21:38Z)] Bottleneck removal notes
# deep_review_alt_sources.py carried 14 candidate URLs disjoint from hunt set - now
# consolidated so URLs probed once via shared URL probe cache.

import json
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import random
import time

REPO_ROOT = Path(__file__).parent.parent
OUT_PATH = REPO_ROOT / "research_state" / "data_source_registry_alt_hunt.json"
DEEP_REVIEW_URLS = []
USER_AGENT = "fclr-alt-hunt/1.2"
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import random
import time

REPO_ROOT = Path(__file__).parent.parent
OUT_PATH = REPO_ROOT / "research_state" / "data_source_registry_alt_hunt.json"
DEEP_REVIEW_URLS = []
USER_AGENT = "fclr-alt-hunt/1.2"
