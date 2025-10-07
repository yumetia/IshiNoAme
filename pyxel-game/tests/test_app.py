# tests/test_app.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import App
from settings import NAME_SCENE, PLAY_SCENE

def test_initial_scene():
    app = App(auto_run=False)
    assert app.current_scene == NAME_SCENE

def test_reset_play_scene():
    app = App(auto_run=False)
    app.reset_play_scene()
    assert app.score == 0
    assert app.current_scene == PLAY_SCENE
    assert isinstance(app.player, object)
    assert app.stones == []
    assert app.items == []

def test_scene_transition():
    app = App(auto_run=False)
    # Simule transition
    app.current_scene = NAME_SCENE
    app.reset_play_scene()
    assert app.current_scene == PLAY_SCENE
