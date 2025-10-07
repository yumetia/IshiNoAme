# tests/conftest.py
import sys
import types
import pytest

# Global mock to avoid graphic actions
pyxel_mock = types.SimpleNamespace(
    init=lambda *a, **k: None,
    load=lambda *a, **k: None,
    run=lambda *a, **k: None,
    btn=lambda *a, **k: False,
    btnp=lambda *a, **k: False,
    rndi=lambda a, b: a,
    cls=lambda *a, **k: None,
    text=lambda *a, **k: None,
    quit=lambda *a, **k: None,

    COLOR_RED=8,
    frame_count=0,
)

sys.modules['pyxel'] = pyxel_mock

@pytest.fixture(autouse=True)
def reset_pyxel_between_tests():
    import pyxel
    yield
    try:
        pyxel.quit()
    except Exception:
        pass
