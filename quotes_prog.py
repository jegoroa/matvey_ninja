from pygame import*
from ctypes import*
import json
W=windll.user32.GetSystemMetrics(0)
H=windll.user32.GetSystemMetrics(1)
win = display.set_mode((W,H),flags=FULLSCREEN)
background = image.load("ronin.jpg")
background = transform.scale(background,(W,H))


class MegaClass(sprite.Sprite):

    def __init__(self,x,y,w,h,filename):
        super().__init__()
        self.rect = Rect(x,y,w,h)
        self.image = image.load(filename)
        self.image = transform.scale(self.image,(w,h))
        self.speed_x = 0
        self.speed_y = 0
        self.right = self. image
        self.left = transform.flip(self.image,True,False)
    def draw(self):
        win.blit(self.image,(self.rect.x,self.rect.y))

class Wall(MegaClass):


    def __init__(self,x,y,w,h,filename):
        super().__init__(x,y,w,h,filename)
        walls.add(self)
    def update(self):
        self.draw()

class Hero(MegaClass):


    def gravity(self):

        if self.jumped >= 0: 
            self.jumped -=1
        else:
            self.speed_y = 10

        self.rect.y += self.speed_y

    def jump(self):
        if self.speed_y == 0:
            self.speed_y  = -10
            self.jumped = 20

    def control(self):
        keys = key.get_pressed()
        if keys[K_d]: 
            self.image = self.right    
            self.speed_x = 5

        elif keys[K_a]: 
            self.image = self.left
            self.speed_x = -5

        else:  
            self.speed_x = 0

        self.rect.x += self.speed_x

        if keys[K_SPACE]: self.jump()

    def update(self):
        self.gravity()
        self.verticle_ground_check()
        self.horizontal_ground_check()
        self.control()
        self.draw()
        
    def verticle_ground_check(self):
        for wall in walls:
            if wall.rect.colliderect(self.rect):
                if self.speed_y > 0:
                    self.rect.bottom = wall.rect.top
                    self.speed_y = 0

                elif self.speed_y < 0 and self.rect.top > wall.rect.bottom:
                    self.rect.top = wall.rect.bottom
                
    def horizontal_ground_check(self):
        for wall in walls:
            if wall.rect.colliderect(self.rect):
                #if self.rect.bottom < wall.rect.top:
                    if self.speed_x > 0:
                        self.rect.right = wall.rect.left
                    elif self.speed_x < 0:
                        self.rect.left = wall.rect.right
                    
ronin = Hero(300,100,100,150,"samurai.png")
ronin.jumped = 0
ronin.speed_y = 10

walls= sprite.Group()

def clear():
    global walls
    walls = sprite.Group()

def load_levelS():
    global levels
    with open("levels.json","r",encoding="utf-8") as file:
        levels = json.load(file)

def bild_level(n):
    global levels
    if n in levels:
        for wall in levels[n]:
            Wall(wall[0],wall[1],wall[2],wall[3],
                    "стена.jpg")
    else:
        print("уровни кончились!")

load_levelS()
bild_level("1")

def save_level(n):
    global levels
    levels[n] = []
    for wall in walls:
        levels[n].append([wall.rect.x,wall.rect.y,
                        wall.rect.w,wall.rect.h])

    with open("levels.json","w",encoding="utf-8")as file:
        json.dump(levels,file)

spawn_w = 100
spawn_h = 50

#timer = time.Clock()
gamemode = 1
while True:
    #timer.tick(60)

    for sobitye in event.get():
        if sobitye.type == KEYDOWN:
            if sobitye.key == K_ESCAPE:
                exit()

            if sobitye.key == K_p:
                spawn_w, spawn_h = spawn_h,spawn_w
            if sobitye.key == K_UP: spawn_h +=30
            if sobitye.key == K_DOWN: spawn_h -=30
            if sobitye.key == K_LEFT: spawn_w -=30
            if sobitye.key == K_RIGHT: spawn_w +=30

            if gamemode == 1:
                if sobitye.key == K_c:
                    keys = key.get_pressed()
                    for n in [K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]:
                        if keys[n]:
                            save_level(n-48)

                if sobitye.key == K_BACKSPACE:
                    clear()

        if sobitye.type == MOUSEBUTTONDOWN:
            x,y = sobitye.pos
            Wall(x-spawn_w//2,y-spawn_h//2,
                spawn_w,spawn_h,"стена.jpg")
            
    
    
    win.blit(background,(0,0))
    ronin.update()
    walls.update()
    display.update()
