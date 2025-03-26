# scenes.py
import pyxel # type: ignore
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

from database import get_top_players

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
    pyxel.text(10, 10, "LEADERBOARD", pyxel.COLOR_WHITE)
    # get the top 5 and print each one 
    records = get_top_players()
    y = 10
    for i,(username,score) in enumerate(records):
        pyxel.text(10,y+(10), f'{i} : {str(username)} {str(score)}',pyxel.COLOR_CYAN)
        y+=10

    pyxel.text(10, SCREEN_HEIGHT-(10), "Press ENTER to return", pyxel.COLOR_YELLOW)
