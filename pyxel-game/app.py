# app.py
import pyxel  # type: ignore

API_URL = "https://ishinoame.onrender.com"


from pyodide.http import pyfetch
import asyncio
IS_WEB = True

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, STONE_INTERVAL, START_SCENE, PLAY_SCENE, LEADERBOARD_SCENE, STONE_SPEED, PLAY_SCREEN_COLOR
from stone import Stone
from player import Player
from scenes import draw_start_scene, draw_game_over, draw_leaderboard

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="石の雨")
        pyxel.load("my_resource.pyxres")
        self.current_scene = START_SCENE
        self.score = 0
        self.step_speed = 50
        self.stone_interval = STONE_INTERVAL
        self.leaderboard = []

        try:
            self.username = pyxel.globals.username
        except AttributeError:
            self.username = "Anonymous"

        pyxel.run(self.update, self.draw)

    def reset_play_scene(self):
        self.score = 0
        self.is_colliding = False
        self.game_over_timer = 60
        self.step_speed = 50
        self.stone_speed = STONE_SPEED
        self.stone_interval = STONE_INTERVAL
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
            if IS_WEB:
                async def send_score():
                    try:
                        response = await pyfetch(
                            url=f"{API_URL}/submit-score",
                            method="POST",
                            headers={"Content-Type": "application/json"},
                            body=pyxel.dumps_json({
                                "username": self.username,
                                "score": self.score
                            })
                        )
                        data = await response.json()
                        print("Score envoyé (web):", data)
                    except Exception as e:
                        print("Erreur fetch (web):", e)

                asyncio.ensure_future(send_score())
            else:
                try:
                    response = requests.post(
                        f"{API_URL}/submit-score",
                        json={"username": self.username, "score": self.score},
                        headers={"Content-Type": "application/json"}
                    )
                    print("Score envoyé (local):", response.json())
                except Exception as e:
                    print("Erreur envoi score (local):", e)
            return

        self.score += 1

        if self.score > self.step_speed:
            self.step_speed += 50
            if self.score < 2800:
                self.stone_speed += 0.1
            elif self.stone_interval > 7:
                self.stone_interval -= 1

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
        if not hasattr(self, 'leaderboard_fetched'):
            if IS_WEB:
                async def get_leaderboard():
                    try:
                        response = await pyfetch(f"{API_URL}/top")
                        data = await response.json()
                        self.leaderboard = data if isinstance(data, list) else [("No data", 0)]
                    except Exception as e:
                        print("Erreur GET leaderboard (web):", e)
                        self.leaderboard = [("Erreur", 0)]
                    self.leaderboard_fetched = True
                asyncio.ensure_future(get_leaderboard())
            else:
                try:
                    response = requests.get(f"{API_URL}/top")
                    data = response.json()
                    self.leaderboard = data if isinstance(data, list) else [("No data", 0)]
                except Exception as e:
                    print("Erreur GET leaderboard (local):", e)
                    self.leaderboard = [("Erreur", 0)]
                self.leaderboard_fetched = True

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.current_scene = START_SCENE
            del self.leaderboard_fetched

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if self.current_scene == START_SCENE:
            self.update_start_scene()
        elif self.current_scene == LEADERBOARD_SCENE:
            self.update_leaderboard_scene()
        elif self.current_scene == PLAY_SCENE:
            self.update_play_scene()

    def draw(self):
        if self.current_scene == START_SCENE:
            draw_start_scene()
        elif self.current_scene == PLAY_SCENE:
            if self.score > 3000:
                pyxel.cls(pyxel.COLOR_GRAY)
            else:
                pyxel.cls(eval(PLAY_SCREEN_COLOR))
            pyxel.text(2, 2, f"{self.score}", pyxel.COLOR_RED)
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
            draw_leaderboard(self.leaderboard)
