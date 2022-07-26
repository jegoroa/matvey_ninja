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
        if keys[K_SPACE]: self.jump()

    def update(self):
        self.gravity()
        self.ground_check()
        self.control()
        self.draw()
        self.rect.x += self.speed_x

        

    def ground_check(self):
        for  wall in walls:
            if wall.rect.colliderect(self.rect):

                if self.rect.top > wall.rect.bottom:
                    self.rect.top = wall.rect.bottom + 3

                if self.rect.left < wall.rect.left:
                    self.speed_x = 0

                if self.rect.right > wall.rect.right:
                    self.speed_x = 0

                if self.rect.top < wall.rect.bottom:
                    self.speed_y = 0
                    return  0
        if self.jumped <=0 :self.speed_y = 5
        


Ronin = Hero(300,100,100,150,"samurai.png")
Ronin.jumped = 0
walls= sprite. Group()
def load_level(n):
    pass

def save_level(n):
    levels[n] = []
    for wall in walls:
        levels[n].append([wall.rect.x,wall.rect.y,
                        wall.rect.w,wall.rect.h])

    with  open("levels.json","w",encoding="utf-8")as file:
        json.dump(levels,file)
      

levels ={}
wall = Wall(x=0,h=50,w=1650,y=765, filename="стена.jpg")
wall = Wall(x=800,h=50,w=200,y=500, filename="стена.jpg")
wall = Wall(x=0,h=50,w=200,y=600, filename="стена.jpg")

spawn_w = 100
spawn_h = 50

while True:


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

            if sobitye.key == K_c:
                keys = key.get_pressed()
                for n in [K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]:
                    if keys[n]:
                        save_level(n-48)


        if sobitye.type == MOUSEBUTTONDOWN:
            x,y = sobitye.pos
            Wall(x-spawn_w//2,y-spawn_h//2,
                spawn_w,spawn_h,"стена.jpg")
            
    
    
    win.blit(background,(0,0))
    Ronin.update()
    walls.update()
    display.update()