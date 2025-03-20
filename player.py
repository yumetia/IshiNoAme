# player.py
import pyxel
from settings import SCREEN_WIDTH, PLAYER_SPEED

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_WIDTH // 2

    def move(self):
        if pyxel.btn(pyxel.KEY_LEFT) and self.x > -4:
            self.x -= PLAYER_SPEED
        elif pyxel.btn(pyxel.KEY_RIGHT) and self.x < SCREEN_WIDTH - 12:
            self.x += PLAYER_SPEED

        if pyxel.btn(pyxel.KEY_UP):
            self.y -= PLAYER_SPEED
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.y += PLAYER_SPEED

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 0, 16, 16, pyxel.COLOR_BLACK)
