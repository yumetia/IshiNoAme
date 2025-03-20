# scenes.py
import pyxel
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def draw_start_scene():
    pyxel.blt(0, 0, 0, 32, 0, 160, 120)
    pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10, "Click to Start", pyxel.COLOR_RED)

def draw_game_over():
    pyxel.text(SCREEN_WIDTH // 2 -(20), SCREEN_HEIGHT // 2, "GAME OVER", pyxel.COLOR_RED)
