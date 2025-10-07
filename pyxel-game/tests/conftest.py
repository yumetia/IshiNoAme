# tests/conftest.py
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

@pytest.fixture(autouse=True)
def mock_pyxel(monkeypatch):
    import types
    pyxel_mock = types.SimpleNamespace(
        init=lambda *a, **k: None,
        load=lambda *a, **k: None,
        run=lambda *a, **k: None,
        btn=lambda *a, **k: False,
        btnp=lambda *a, **k: False,
        rndi=lambda a, b: a,
        cls=lambda *a, **k: None,
        text=lambda *a, **k: None,
        quit=lambda: None,
        MOUSE_BUTTON_LEFT=1,
        KEY_RETURN=2,
        KEY_SPACE=3,
        KEY_ESCAPE=4,
        COLOR_RED=8,
        frame_count=0,
    )
    monkeypatch.setitem(sys.modules, "pyxel", pyxel_mock)
