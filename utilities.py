import sys
from typing import Any, List, Optional

def print_cond(cond: bool, *objects: Any, sep: str = ' ', end: str = '\n', file = sys.stdout, flush: bool = False) -> None:
    if cond:
        print(*objects, sep=sep, end=end, file=file, flush=flush)



def safe_to_float(value: Any, default: float | None = None) -> float | None:
    if value is None:
        return default
    try:
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        return float(value) if value not in {"", "#N/A N/A", "#N/A Invalid Security"} else default
    except (ValueError, TypeError):
        return default

def contains_which(str : str, list : List[str]) -> Optional[str]:
    for item in list:
        if item in str:
            return item
    return None
