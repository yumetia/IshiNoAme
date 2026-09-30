

from app import App
from settings import NAME_SCENE, PLAY_SCENE


def test_initial_scene(app):
    assert app.current_scene == NAME_SCENE

def test_reset_play_scene(app):
    app.reset_play_scene()
    assert app.score == 0
    assert app.current_scene == PLAY_SCENE
    assert isinstance(app.player, object)
    assert app.stones == []
    assert app.items == []

def test_scene_transition(app):
    # Simulation transition
    app.current_scene = NAME_SCENE
    app.reset_play_scene()
    assert app.current_scene == PLAY_SCENE
