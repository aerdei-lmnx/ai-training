"""Root conftest -- ensures the project directory is on sys.path so that
``import app`` and ``import models`` work when running pytest from the
sample-project directory.
"""

import sys
from pathlib import Path

# Add the sample-project directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))
