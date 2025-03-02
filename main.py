import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH,SCREEN_HEIGHT,title="石の雨")
        pyxel.mouse(True)
        pyxel.load("my_resource.pyxres")

        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT*4//5
        self.stone_x = SCREEN_WIDTH//2
        self.stone_y = 0
        self.is_colliding = False

        pyxel.run(self.update,self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
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
            
        print("stone_x:",self.stone_x)
        print("player_x:",self.player_x)
        print("stone_y:",self.stone_y)
        print("player_y:",self.player_y)

        # colliding stone/player ?
        if (self.player_x-4 <= self.stone_x <= self.player_x+4) and (self.player_y-4 <= self.stone_y <= self.player_y-4):
            self.is_colliding=True
        # stone
        self.stone_y+=1

    def draw(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)
        # 石
        pyxel.blt(self.stone_x,self.stone_y,0,8,0,8,8,pyxel.COLOR_BLACK)
        # player
        pyxel.blt(self.player_x,self.player_y,0,16,0,16,16,pyxel.COLOR_BLACK)
        # game over
        if self.is_colliding==True:
            pyxel.text(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,"GAME OVER",pyxel.COLOR_RED)

App()