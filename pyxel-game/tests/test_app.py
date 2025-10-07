# tests/test_app.py
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import App
from settings import NAME_SCENE, START_SCENE, PLAY_SCENE

@pytest.fixture
def app_instance(monkeypatch):
    # avoid pyxel to open graphic window during the tests
    monkeypatch.setattr("pyxel.init", lambda *args, **kwargs: None)
    monkeypatch.setattr("pyxel.load", lambda *args, **kwargs: None)
    monkeypatch.setattr("pyxel.run", lambda *args, **kwargs: None)
    return App()

def test_initial_scene(app_instance):
    """Vérifie que l'application démarre sur la scène de nom."""
    assert app_instance.current_scene == NAME_SCENE

def test_reset_play_scene(app_instance):
    """Vérifie que la scène de jeu se réinitialise correctement."""
    app_instance.reset_play_scene()
    assert app_instance.score == 0
    assert app_instance.current_scene == PLAY_SCENE
    assert hasattr(app_instance, "player")
    assert isinstance(app_instance.stones, list)

def test_scene_transition(app_instance):
    """Vérifie la transition entre les scènes."""
    app_instance.current_scene = START_SCENE
    app_instance.reset_play_scene()
    assert app_instance.current_scene == PLAY_SCENE
