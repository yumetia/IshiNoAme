import sys
import os
import pytest
# Add the project root (pyxel-game/) to sys.path so `import app` works
# regardless of which directory pytest is run from.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import App

@pytest.fixture(scope="session")
def app():
    return App(auto_run=False)
