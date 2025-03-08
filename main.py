import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
STONE_INTERVAL = 5
START_SCENE = "start"
PLAY_SCENE = "play"

class Stone:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def update(self):
        self.y+=1

    def draw(self):
        # 石
        pyxel.blt(self.x,self.y,0,8,0,8,8,pyxel.COLOR_BLACK)


class App:

    def __init__(self):
        pyxel.init(SCREEN_WIDTH,SCREEN_HEIGHT,title="石の雨")
        pyxel.load("my_resource.pyxres")
        
        self.current_scene = START_SCENE
        

        pyxel.run(self.update,self.draw)

    def reset_play_scene(self):
        self.is_colliding = False
        self.score = 0
        self.game_over_timer = 60

        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT*4//5
        
        self.stones=[]
        self.current_scene = PLAY_SCENE

    def update_start_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.reset_play_scene()

    def update_play_scene(self):
        # Game over ?
        if self.is_colliding:
            return
        # score
        self.score+=1

        # x
        if pyxel.btn(pyxel.KEY_LEFT) and self.player_x > - 4 :
            self.player_x -=1
        elif pyxel.btn(pyxel.KEY_RIGHT) and self.player_x<SCREEN_WIDTH-12 :
            self.player_x +=1

        # y
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y -=1
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.player_y +=1
        

        if pyxel.frame_count%STONE_INTERVAL==0:
            self.stones.append(Stone(pyxel.rndi(0,SCREEN_WIDTH-6),0))

        for stone in self.stones.copy():
            stone.update()

            # colliding stone/player ?
            if (self.player_x <= stone.x <= self.player_x+8) and (self.player_y <= stone.y <= self.player_y+8):
                self.is_colliding=True
            
            if stone.y>=SCREEN_HEIGHT:
                self.stones.remove(stone)

    def update(self):

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        
        if self.current_scene==START_SCENE:
            self.update_start_scene()

        elif self.current_scene==PLAY_SCENE:
            self.update_play_scene()


    def draw_start_scene(self):
        pyxel.blt(0,0,0,32,0,160,120)
        pyxel.text(SCREEN_WIDTH//10,SCREEN_HEIGHT//10,"Click to Start",pyxel.COLOR_RED)
        self.update_start_scene()


    def draw_play_scene(self):
        pyxel.blt(0,0,1,0,0,160,120)
        pyxel.text(2,2,f"{self.score}",pyxel.COLOR_GREEN)
        # game over
        if self.is_colliding:
            self.game_over_timer-=1
            pyxel.text(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,"GAME OVER",pyxel.COLOR_RED)
            if self.game_over_timer<30:
                self.draw_start_scene()
                return
        # stones
        for stone in self.stones:
            stone.draw()

        # player
        pyxel.blt(self.player_x,self.player_y,0,16,0,16,16,pyxel.COLOR_BLACK)


    def draw(self):
        if self.current_scene==START_SCENE:
            self.draw_start_scene()
        elif self.current_scene==PLAY_SCENE:
            self.draw_play_scene()

App()