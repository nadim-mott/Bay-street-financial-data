import sys
from typing import Any

def print_cond(cond: bool, *objects: Any, sep: str = ' ', end: str = '\n', file = sys.stdout, flush: bool = False) -> None:
    if cond:
        print(*objects, sep=sep, end=end, file=file, flush=flush)



def safe_to_float(value: Any, default : float | None = None) -> float | None:
  if value is None:
    return default
  try:
    return float(value) if value not in {"", "#N/A N/A", "#N/A Invalid Security"} else default
  except (ValueError, TypeError):
    return default
