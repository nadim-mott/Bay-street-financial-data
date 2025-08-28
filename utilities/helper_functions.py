import sys
from typing import Any, List, Optional
import os, shutil

def print_cond(cond: bool, *objects: Any, sep: str = ' ', end: str = '\n', file = sys.stdout, flush: bool = False) -> None:
    if cond:
        print(*objects, sep=sep, end=end, file=file, flush=flush)



def safe_to_float(value: Any, default: float | None = None) -> float | None:
    if value is None:
        return default
    try:
        if isinstance(value, str):
            value = value.replace(",", "").strip()
            value = value.replace(" ", "").strip()
            value = value.replace("$", "").strip()
        return float(value) if value not in {"", "#N/A N/A", "#N/A Invalid Security"} else default
    except (ValueError, TypeError):
        return default

def contains_which(str : str, list : List[str]) -> Optional[str]:
    for item in list:
        if item in str:
            return item
    return None



def remove_folder_contents():
    folder = '/path/to/folder'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))