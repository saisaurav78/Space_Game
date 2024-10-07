import pygame
from pygame import *
from random import *
import math

#CreatingDisplay
pygame.init()
pygame.display.set_caption("space world")
screen=pygame.display.set_mode((640,480))
icon= pygame.image.load("spacegame/assets/images/player.png")
pygame.display.set_icon(icon) 
clock=pygame.time.Clock()
bg=pygame.image.load("spacegame/assets/images/bg.jpg")
playerimg= pygame.image.load("spacegame/assets/images/player.png")
enemyimg= pygame.image.load("spacegame/assets/images/ufo.png")
bulletimg = pygame.image.load("spacegame/assets/images/bullet.png")


#Player Object
class Ship:
    class Bullet:
        def __init__(self,BulletImg,BulletX,BulletY):
            self.bulletImg=BulletImg
            self.bulletX=BulletX  
            self.bulletY=BulletY
        def move_Y(self,key):
            if KEY[K_SPACE]:
                if self.bulletY<=0:
                    self.bulletY=Player.Y_pos-5
                    self.bulletX=Player.X_pos+16
                self.bulletY-=10

    def __init__(self,ShipImg,X_pos,Y_pos,Health):
        self.ShipImg=ShipImg
        self.X_pos=X_pos
        self.Y_pos=Y_pos
        self.Health=Health
    
    def move_X(self,KEY):
        if(KEY[K_LEFT] or KEY[K_a]):
            if self.X_pos<=5:
                self.X_pos=5
            self.X_pos-=5
            print("x:",self.X_pos,"y:",self.Y_pos)
        elif (KEY[K_RIGHT] or KEY[K_d]):
            if self.X_pos>=570:
                self.X_pos=570
            self.X_pos+=5
            print("x:",self.X_pos,"y:",self.Y_pos)
            
    def move_Y(self,KEY):
        if(KEY[K_UP] or KEY[K_w]):
            if self.Y_pos<=5:
                self.Y_pos=5
            self.Y_pos-=5
            print("x:",self.X_pos,"y:",self.Y_pos)
        elif(KEY[K_DOWN] or KEY[K_s]):
            if self.Y_pos>=405:
                self.Y_pos=405
            self.Y_pos+=5
            print("x:",self.X_pos,"y:",self.Y_pos)


#Enemy Object
class Enemy(Ship):
    def __init__(self, Img, X_pos, Y_pos, Health, Direction):
        super().__init__(Img, X_pos, Y_pos, Health)
        self.Direction = Direction
    def move_X(self):
        if self.X_pos <= 0 or self.X_pos >= 570:
            self.Direction = -self.Direction
        self.X_pos += 2 * self.Direction



Player= Ship(playerimg,300,400,50) 
enemy=Enemy(enemyimg,10,0,100,1)


PlayerBullet= Ship.Bullet(bulletimg,Player.X_pos+16,Player.Y_pos-5)


# PlayerBullet= Player.fire(bulletimg,316,416)




enemies=[]
for i in range(5):
    direction = 1 if randint(0, 1) == 0 else -1
    enemy=Enemy(enemyimg,randint(0,500),randint(0,100),100,direction)
    enemies.append(enemy)




#MainLoop
run=True
while(run):
    screen.blit(bg,(0,0))
    screen.blit(Player.ShipImg,(Player.X_pos,Player.Y_pos))
    screen.blit(PlayerBullet.bulletImg,(PlayerBullet.bulletX,PlayerBullet.bulletY))
    for enemy in enemies:
        screen.blit(enemy.ShipImg,(enemy.X_pos,enemy.Y_pos))
        enemy.move_X()

    KEY=pygame.key.get_pressed()
    key=pygame.KEYDOWN
    Player.move_X(KEY)
    Player.move_Y(KEY)
    PlayerBullet.move_Y(key)
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    pygame.display.update()
    clock.tick(60)
pygame.quit()



