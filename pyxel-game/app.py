# app.py
import pyxel

from database import create_table, update_score, get_top_players, player_exists
from settings import STONE_INTERVAL, SCREEN_WIDTH, SCREEN_HEIGHT, START_SCENE, NAME_SCENE, PLAY_SCENE, LEADERBOARD_SCENE, STONE_SPEED, PLAY_SCREEN_COLOR,IS_WEB
from stone import Stone,Item
from player import Player
from scenes import draw_username_scene, draw_start_scene, draw_game_over, draw_leaderboard

if IS_WEB:
    import json
    from pyodide.http import pyfetch
# Create table if necessary
else:
    create_table()

API_URL = "https://ishinoame.onrender.com"


class App:
    def __init__(self,auto_run=True):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="石の雨")
        pyxel.load("my_resource.pyxres")
        self.current_scene = NAME_SCENE
        self.score = 0
        self.step_speed = 60
        self.stone_interval = STONE_INTERVAL
        self.leaderboard = []

        self.username = ""
        self.password = ""
        self.active_field = "username"  # "username" or "password"
        self.auth_mode = "login"        # "login" or "register"
        self.auth_message = ""          # feedback shown to the player
        self.auth_pending = False       # true while a request is in flight
        self.token = None                # JWT once authenticated

        if auto_run:
            pyxel.run(self.update, self.draw)

    def _type_into(self, buffer_name, max_len=20):
        buffer = getattr(self, buffer_name)
        for attr in dir(pyxel):
            if attr.startswith("KEY_") and attr not in ("KEY_BACKSPACE", "KEY_RETURN", "KEY_TAB"):
                keycode = getattr(pyxel, attr)
                if pyxel.btnp(keycode) and len(buffer) < max_len:
                    try:
                        buffer += chr(keycode)
                    except ValueError:
                        pass
        setattr(self, buffer_name, buffer)

    def update_username_scene(self):
        if self.auth_pending:
            return  # ignore input while a request is running

        if pyxel.btnp(pyxel.KEY_TAB):
            self.active_field = "password" if self.active_field == "username" else "username"
            return

        if self.active_field == "username":
            self._type_into("username")
            if pyxel.btnp(pyxel.KEY_BACKSPACE) and self.username:
                self.username = self.username[:-1]
        else:
            self._type_into("password")
            if pyxel.btnp(pyxel.KEY_BACKSPACE) and self.password:
                self.password = self.password[:-1]

        if pyxel.btnp(pyxel.KEY_L):
            # toggle between login and register mode
            self.auth_mode = "register" if self.auth_mode == "login" else "login"
            self.auth_message = ""

        if pyxel.btnp(pyxel.KEY_RETURN) and self.username and self.password:
            if IS_WEB:
                self.auth_pending = True
                self.auth_message = "logging in..." if self.auth_mode == "login" else "creating..."

                async def do_auth():
                    endpoint = "/login" if self.auth_mode == "login" else "/register"
                    try:
                        response = await pyfetch(
                            f"{API_URL}{endpoint}",
                            method="POST",
                            headers={"Content-Type": "application/json"},
                            body=json.dumps({
                                "username": self.username,
                                "password": self.password
                            })
                        )
                        data = await response.json()
                        if response.status in (200, 201) and "token" in data:
                            self.token = data["token"]
                            self.current_scene = START_SCENE
                            self.auth_message = ""
                        else:
                            self.auth_message = data.get("error", "Unknown error")
                    except Exception as e:
                        self.auth_message = f"Error: {e}"
                    finally:
                        self.auth_pending = False

                import asyncio
                asyncio.ensure_future(do_auth())
            else:
                # local/desktop mode: mirror the same login/register flow
                from database import create_player, verify_password

                if self.auth_mode == "register":
                    if player_exists(self.username):
                        self.auth_message = "Username already taken"
                    else:
                        create_player(self.username, self.password)
                        self.current_scene = START_SCENE
                        self.auth_message = ""
                else:  # login
                    if verify_password(self.username, self.password):
                        self.current_scene = START_SCENE
                        self.auth_message = ""
                    else:
                        self.auth_message = "Invalid username or password"

    def reset_play_scene(self):
        self.score = 0
        self.is_colliding = False
        self.score_submitted = False 

        self.game_over_timer = 60
        self.step_speed = 50
        self.stone_speed = STONE_SPEED
        self.stone_interval = STONE_INTERVAL
        
        self.player = Player()
        
        self.stones = []
        self.items = []
        
        self.current_scene = PLAY_SCENE

    def update_start_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.reset_play_scene()
        elif pyxel.btnp(pyxel.KEY_L):
            self.current_scene = LEADERBOARD_SCENE

    def update_difficulty(self):
        # stone speed: starts low, increases smoothly, caps out
        base_speed = 1.0
        max_speed = 7.0
        speed_ramp_score = 3000  # score at which speed reaches its cap

        speed_progress = min(self.score / speed_ramp_score, 1.0)
        self.stone_speed = base_speed + (max_speed - base_speed) * speed_progress

        # stone interval: starts higher (slower spawns), decreases smoothly, floors out
        base_interval = 7
        min_interval = 7
        interval_ramp_score = 4000  # score at which interval reaches its floor

        interval_progress = min(self.score / interval_ramp_score, 1.0)
        self.stone_interval = round(base_interval - (base_interval - min_interval) * interval_progress)

    def spawn_item_safely(self):
        min_gap = 20  # minimum horizontal distance from any current stone

        candidate_x = pyxel.rndi(0, SCREEN_WIDTH - 6)

        for stone in self.stones:
            # only worry about stones still near the top (recently spawned, not yet passed)
            if stone.y < 20 and abs(stone.x - candidate_x) < min_gap:
                return  # too close to a stone, skip this spawn attempt

        self.items.append(Item(candidate_x, 0, self.stone_speed))

    def update_play_scene(self):
        if self.is_colliding:
            if not self.score_submitted:
                self.score_submitted = True
                if IS_WEB:
                    async def send_score():
                        try:
                            await pyfetch(
                                f"{API_URL}/submit-score",
                                method="POST",
                                headers={
                                    "Content-Type": "application/json",
                                    "Authorization": f"Bearer {self.token}"
                                },
                                body=json.dumps({
                                    "score": self.score
                                })
                            )
                            print("Score sent to the server")
                        except Exception as e:
                            print("Error when sending:", e)
                    import asyncio
                    asyncio.ensure_future(send_score())
                else:
                    update_score(self.username, self.score)
            return

        self.score += 1
        self.update_difficulty()

        self.player.move()

        if pyxel.frame_count % self.stone_interval == 0:
            self.stones.append(Stone(pyxel.rndi(0, SCREEN_WIDTH - 6), 0, self.stone_speed))
        elif pyxel.frame_count % 500 == 0:
            self.spawn_item_safely()

        for stone in self.stones.copy():
            stone.update()

            if (self.player.x <= stone.x <= self.player.x + 8) and (self.player.y <= stone.y <= self.player.y + 8):
                self.is_colliding = True

            if stone.y >= SCREEN_HEIGHT:
                self.stones.remove(stone)

        for item in self.items.copy():
            item.update()
            
            if (self.player.x <= item.x <= self.player.x + 8) and (self.player.y <= item.y <= self.player.y + 8):
                print("ok")
            if item.y >= SCREEN_HEIGHT:
                print(self.items)
                self.items.remove(item)

    def update_leaderboard_scene(self):
        if not hasattr(self, 'leaderboard_fetched'):
            self.leaderboard_fetched = True
            if IS_WEB:
                async def get_leaderboard():
                    try:
                        response = await pyfetch(f"{API_URL}/top")
                        data = await response.json()
                        self.leaderboard = [(entry[0], entry[1]) for entry in data]
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
            draw_username_scene(
                self.username,
                self.password,
                self.active_field,
                self.auth_mode,
                self.auth_message
            )
        elif self.current_scene == START_SCENE:
            draw_start_scene()
        elif self.current_scene == PLAY_SCENE:
            if self.score > 3000:
                pyxel.cls(0)
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
            
            for item in self.items:
                item.draw()
            self.player.draw()
        elif self.current_scene == LEADERBOARD_SCENE:
            draw_leaderboard(self.leaderboard)
