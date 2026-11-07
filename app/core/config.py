import os
import sys
from functools import lru_cache


def _flag(name: str) -> bool:
    return os.environ.get(name, "").strip() in {"1", "true", "yes", "on"}


@lru_cache
def is_demo_mode() -> bool:
    if _flag("NEDSCANNER_DEMO"):
        return True
    return "--demo" in sys.argv
