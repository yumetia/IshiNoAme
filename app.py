# app.py
from curses import KEY_BACKSPACE
import pyxel # type: ignore

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, STONE_INTERVAL, START_SCENE, PLAY_SCENE,LEADERBOARD_SCENE,NAME_SCENE, STONE_SPEED,PLAY_SCREEN_COLOR
from stone import Stone
from player import Player
from scenes import draw_name_scene, draw_start_scene, draw_game_over, draw_leaderboard

from database import create_table,insert_player,update_score

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="石の雨")
        pyxel.load("my_resource.pyxres")
        self.current_scene = NAME_SCENE
        self.score = 0
        self.step_speed = 30
        self.stone_interval = STONE_INTERVAL

        create_table()
        self.username = ""

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
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.reset_play_scene()
        elif pyxel.btnp(pyxel.KEY_L):
            self.current_scene = LEADERBOARD_SCENE
            

    def update_play_scene(self):
        if self.is_colliding:
            update_score(self.username,self.score)
            return

        self.score += 10

        if self.score>self.step_speed:
            self.step_speed+=30 
            if self.score<3000:
                self.stone_speed += 0.05
            elif self.stone_interval > 5:            
                self.stone_interval-= 1

        self.player.move()

        if pyxel.frame_count % self.stone_interval == 0:
            self.stones.append(Stone(pyxel.rndi(0, SCREEN_WIDTH - 6), 0, self.stone_speed))

        for stone in self.stones.copy():
            stone.update()

            if (self.player.x <= stone.x <= self.player.x + 8) and (self.player.y <= stone.y <= self.player.y + 8):
                self.is_colliding = True

            if stone.y >= SCREEN_HEIGHT:
                self.stones.remove(stone)

    def update_leaderboard_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.current_scene = START_SCENE
    
    def update_name_scene(self):
        # Process regular keys to append characters
        for attr in dir(pyxel):
            if attr.startswith("KEY_") and attr not in ("KEY_BACKSPACE", "KEY_RETURN"):
                keycode = getattr(pyxel, attr)
                if pyxel.btnp(keycode):
                    try:
                        self.username += chr(keycode)
                    except ValueError:
                        print("Key code does not correspond to a valid ASCII character.")
        
        # Process backspace (remove last character) once per update
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and self.username:
            self.username = self.username[:-1]
            print(self.username)
        
        # Process return key to change scene if the username is long enough
        if pyxel.btnp(pyxel.KEY_RETURN) and len(self.username) > 2:
            insert_player(self.username)
            self.current_scene = START_SCENE

        
    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if self.current_scene == NAME_SCENE:
            self.update_name_scene()
        elif self.current_scene == START_SCENE:
            self.update_start_scene()
        elif self.current_scene == LEADERBOARD_SCENE:
            self.update_leaderboard_scene()
        elif self.current_scene == PLAY_SCENE:
            self.update_play_scene()

    
        
    def draw(self):
        if self.current_scene == NAME_SCENE:
            draw_name_scene(self.username)
        elif self.current_scene == START_SCENE:
            draw_start_scene()
        elif self.current_scene == PLAY_SCENE:
            if self.score>3000:
                pyxel.cls(pyxel.COLOR_DARK_BLUE)
            else:
                pyxel.cls(eval(PLAY_SCREEN_COLOR))
            pyxel.text(2, 2, f"{self.score}", pyxel.COLOR_GREEN)
            if self.is_colliding:
                self.game_over_timer -= 1
                draw_game_over()
                if self.game_over_timer < 30:
                    self.current_scene = START_SCENE
                return
            for stone in self.stones:
                stone.draw()
            self.player.draw()

        elif self.current_scene == LEADERBOARD_SCENE:
            draw_leaderboard()