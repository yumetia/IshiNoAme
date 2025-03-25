# scenes.py
import pyxel # type: ignore
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def draw_name_scene(username):
    pyxel.cls(0)
    pyxel.text(SCREEN_WIDTH // 10 , SCREEN_HEIGHT // 5, f'Your name:{username}' , pyxel.COLOR_WHITE)

def draw_start_scene():
    pyxel.blt(0, 0, 0, 32, 0, 160, 120)
    
    pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10, "Click to Start", pyxel.COLOR_RED)
    pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10 + (100), "Press L to check leaderboard", pyxel.COLOR_YELLOW)

def draw_game_over():
    pyxel.text(SCREEN_WIDTH // 2 - (20), SCREEN_HEIGHT // 2, "GAME OVER", pyxel.COLOR_RED)

# leaderboard

def draw_leaderboard():
    pyxel.cls(0)  
    # db connect and handle
    pyxel.text(10, 10, "LEADERBOARD", pyxel.COLOR_WHITE)
    pyxel.text(10, 20, "Press ENTER to return", pyxel.COLOR_YELLOW)
