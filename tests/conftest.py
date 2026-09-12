import sys
from pathlib import Path

# Ensure tests can import the top-level app package regardless of cwd.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
