# app.py
import pyxel

from database import create_table, insert_player, update_score, get_top_players, player_exists
from settings import STONE_INTERVAL, SCREEN_WIDTH, SCREEN_HEIGHT, START_SCENE, NAME_SCENE, PLAY_SCENE, LEADERBOARD_SCENE, STONE_SPEED, PLAY_SCREEN_COLOR,IS_WEB
from stone import Stone
from player import Player
from scenes import draw_username_scene, draw_start_scene, draw_game_over, draw_leaderboard

if IS_WEB:
    import json
    from pyodide.http import pyfetch

# ⚡ Crée la table locale si besoin
if not IS_WEB:
    create_table()

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="石の雨")
        pyxel.load("my_resource.pyxres")
        self.current_scene = NAME_SCENE
        self.score = 0
        self.step_speed = 50
        self.stone_interval = STONE_INTERVAL
        self.leaderboard = []
        self.username = ""
        self.username_available = True  # Par défaut accepté en local
        pyxel.run(self.update, self.draw)

    def update_username_scene(self):
        for attr in dir(pyxel):
            if attr.startswith("KEY_") and attr not in ("KEY_BACKSPACE", "KEY_RETURN"):
                keycode = getattr(pyxel, attr)
                if pyxel.btnp(keycode) and len(self.username) < 20:
                    try:
                        self.username += chr(keycode)
                    except ValueError:
                        print("Key code invalide")

        if pyxel.btnp(pyxel.KEY_BACKSPACE) and self.username:
            self.username = self.username[:-1]

        if pyxel.btnp(pyxel.KEY_RETURN) and self.username:
            if IS_WEB:
                # (optionnel : vérifier username sur serveur)
                self.current_scene = START_SCENE
            else:
                if not player_exists(self.username):
                    insert_player(self.username)
                self.current_scene = START_SCENE

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
                        await pyfetch(
                            url="https://ishinoame.onrender.com/submit-score",
                            method="POST",
                            headers={"Content-Type": "application/json"},
                            body=json.dumps({
                                "username": self.username,
                                "score": self.score
                            })
                        )
                        print("Score envoyé au serveur")
                    except Exception as e:
                        print("Erreur d'envoi:", e)
                import asyncio
                asyncio.ensure_future(send_score())
            else:
                update_score(self.username, self.score)
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
                        response = await pyfetch("https://ishinoame.onrender.com/top")
                        data = await response.json()
                        self.leaderboard = [(entry["username"], entry["score"]) for entry in data]
                        self.leaderboard_fetched = True
                    except Exception as e:
                        print("Erreur récupération leaderboard:", e)

                import asyncio
                asyncio.ensure_future(get_leaderboard())
            else:
                top_players = get_top_players()
                self.leaderboard = [(row[0], row[1]) for row in top_players]
                self.leaderboard_fetched = True

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.current_scene = START_SCENE
            if hasattr(self, 'leaderboard_fetched'):
                del self.leaderboard_fetched

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if self.current_scene == NAME_SCENE:
            self.update_username_scene()
        elif self.current_scene == START_SCENE:
            self.update_start_scene()
        elif self.current_scene == LEADERBOARD_SCENE:
            self.update_leaderboard_scene()
        elif self.current_scene == PLAY_SCENE:
            self.update_play_scene()

    def draw(self):
        if self.current_scene == NAME_SCENE:
            draw_username_scene(self.username, self.username_available)
        elif self.current_scene == START_SCENE:
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
