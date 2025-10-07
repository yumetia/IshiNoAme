import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from player import Player

def test_player_initial_position():
    p = Player()
    assert hasattr(p, "x")
    assert hasattr(p, "y")

def test_player_movement(monkeypatch):
    # avoid pyxel.btn during the test
    monkeypatch.setattr("pyxel.btn", lambda key: False)
    p = Player()
    old_x, old_y = p.x, p.y
    p.move()
    # player doesnt move if nokey is pressed 
    assert p.x == old_x
    assert p.y == old_y
