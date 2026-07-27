# scenes.py
import pyxel # type: ignore
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def draw_username_scene(username, password, active_field, auth_mode, message):
    pyxel.cls(0)

    title = "REGISTER" if auth_mode == "register" else "LOGIN"
    title_x = (SCREEN_WIDTH - len(title) * 4) // 2
    pyxel.text(title_x, SCREEN_HEIGHT // 8, title, pyxel.COLOR_YELLOW)

    # username field
    username_color = pyxel.COLOR_WHITE if active_field == "username" else pyxel.COLOR_GRAY
    username_display = username + ("_" if active_field == "username" else "")
    pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 4, f"Username: {username_display}", username_color)

    # password field (masked)
    password_color = pyxel.COLOR_WHITE if active_field == "password" else pyxel.COLOR_GRAY
    masked = "*" * len(password) + ("_" if active_field == "password" else "")
    pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 4 + 12, f"Password: {masked}", password_color)

    # feedback message
    if message:
        pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 4 + 28, message, pyxel.COLOR_RED)

    # instructions
    footer_y = SCREEN_HEIGHT - 30
    pyxel.text(SCREEN_WIDTH // 10, footer_y, "TAB: switch field", pyxel.COLOR_GRAY)
    pyxel.text(SCREEN_WIDTH // 10, footer_y + 10, f"L: switch to {'LOGIN' if auth_mode == 'register' else 'REGISTER'}", pyxel.COLOR_GRAY)
    pyxel.text(SCREEN_WIDTH // 10, footer_y + 20, "ENTER: submit", pyxel.COLOR_GRAY)

    
def draw_start_scene():
    pyxel.blt(0, 0, 0, 32, 0, 160, 120)
    
    pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10, "Click to Start", pyxel.COLOR_RED)
    pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10 + (100), "Press L to check leaderboard", pyxel.COLOR_YELLOW)

def draw_game_over():
    pyxel.text(SCREEN_WIDTH // 2 - (20), SCREEN_HEIGHT // 2, "GAME OVER", pyxel.COLOR_RED)


def draw_leaderboard(data):
    pyxel.cls(0)

    box_x = 5
    box_y = 5
    box_width = SCREEN_WIDTH - 10
    box_height = SCREEN_HEIGHT - 20

    # box
    pyxel.rect(box_x, box_y, box_width, box_height, pyxel.COLOR_DARK_BLUE)
    pyxel.rectb(box_x, box_y, box_width, box_height, pyxel.COLOR_WHITE)  

    # title
    title = "LEADERBOARD"
    title_x = (SCREEN_WIDTH - len(title) * 4) // 2
    pyxel.text(title_x, box_y + 8, title, pyxel.COLOR_YELLOW)

    y = box_y + 25
    for i, (username, score) in enumerate(data):
        rank = f"{i + 1}."
        entry = f"{username:<10} {score:>5}"

        # color by rank
        if i == 0:
            color = pyxel.COLOR_YELLOW  
        elif i == 1:
            color = pyxel.COLOR_GRAY 
        elif i == 2:
            color = pyxel.COLOR_BROWN
        else:
            color = pyxel.COLOR_WHITE

        pyxel.text(box_x + 15, y, f"{rank} {entry}", color)
        y += 12

    # footer
    footer = "Press ENTER to return"
    footer_x = (SCREEN_WIDTH - len(footer) * 4) // 2
    pyxel.text(footer_x, SCREEN_HEIGHT - 10, footer, pyxel.COLOR_GREEN)
    