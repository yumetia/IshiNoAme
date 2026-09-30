
from player import Player
from settings import PLAYER_SPEED

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

def test_player_move_right(monkeypatch):
    # moves right working properly 
    monkeypatch.setattr("pyxel.btn",lambda key: "KEY_RIGHT")
    p = Player()
    old_x = p.x
    p.move()
    assert old_x == p.x + PLAYER_SPEED
