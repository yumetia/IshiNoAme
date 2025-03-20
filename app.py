# app.py
import pyxel
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, STONE_INTERVAL, START_SCENE, PLAY_SCENE, STONE_SPEED,PLAY_SCREEN_COLOR
from stone import Stone
from player import Player
from scenes import draw_start_scene, draw_game_over

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="石の雨")
        pyxel.load("my_resource.pyxres")

        self.current_scene = START_SCENE
        self.score = 0
        pyxel.run(self.update, self.draw)

    def reset_play_scene(self):
        self.score = 0
        self.is_colliding = False
        self.game_over_timer = 60
        self.stone_speed = STONE_SPEED

        self.player = Player()  
        self.stones = []
        self.current_scene = PLAY_SCENE

    def update_start_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.reset_play_scene()

    def update_play_scene(self):
        if self.is_colliding:
            return

        self.score += 1
        if pyxel.frame_count < 1000:
            self.stone_speed += 0.005

        self.player.move()

        if pyxel.frame_count % STONE_INTERVAL == 0:
            self.stones.append(Stone(pyxel.rndi(0, SCREEN_WIDTH - 6), 0, self.stone_speed))

        for stone in self.stones.copy():
            stone.update()

            if (self.player.x <= stone.x <= self.player.x + 8) and (self.player.y <= stone.y <= self.player.y + 8):
                self.is_colliding = True

            if stone.y >= SCREEN_HEIGHT:
                self.stones.remove(stone)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if self.current_scene == START_SCENE:
            self.update_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.update_play_scene()

    def draw(self):
        pyxel.cls(eval(PLAY_SCREEN_COLOR))
        pyxel.text(2, 2, f"{self.score}", pyxel.COLOR_GREEN)

        if self.current_scene == START_SCENE:
            draw_start_scene()
        elif self.current_scene == PLAY_SCENE:
            if self.is_colliding:
                self.game_over_timer -= 1
                draw_game_over()
                if self.game_over_timer < 30:
                    self.current_scene = START_SCENE
                return

            for stone in self.stones:
                stone.draw()

            self.player.draw()
