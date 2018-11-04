import sys
from pathlib import Path

if sys.platform == 'win32':
    CACHE_ROOT = Path.home() / 'AppData/Local/pyalc'
else:
    CACHE_ROOT = Path.home() / '.cache/pyalc'
