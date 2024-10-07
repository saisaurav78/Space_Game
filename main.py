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
explosion= pygame.image.load("spacegame/assets/images/blast.png")



#creatingPlayer
playerImg=pygame.image.load("spacegame/assets/images/player.png")
playerX=300
playerY=400
playerHealth=50

#creatingEnemy
enemyImg=pygame.image.load("spacegame/assets/images/ufo.png")
enemyX=0
enemyY=0
enemyX_Change=2.8
enemyY_change=2.5
enemyBulletYchange=8


#PlayerBullets
bulletImg=pygame.image.load("spacegame/assets/images/bullet.png")
bulletX=playerX
bulletY=playerY
bulletXchange=0
bulletYchange=8
bulletState="ready"



#EnemyBullets
enemybulletImg=pygame.image.load("spacegame/assets/images/enemybullets.png")
enemybulletX=enemyX
enemybulletY=enemyY

#GameSounds
bulletsound=pygame.mixer.Sound("spacegame/assets/sounds/gunshot.wav")


#DisplayingToScreen

def enemy():
    screen.blit(enemyImg,(enemyX,enemyY))

def player(x,y):
    if(playerHealth>=0 and playerHealth<=50):
        screen.blit(playerImg,(x,y))

def healthbar(x, y, playerHealth):
    if playerHealth <= 50 and playerHealth>=25:
        color = (0, 255, 0)  
    elif playerHealth <=35 and playerHealth>=20:
        color = (255, 255, 0)  
    else:
        color = (255, 0, 0) 
    pygame.draw.rect(screen, color, (x + 7, y + 66, playerHealth, 8))

def fire_bullet(x,y):
   global bulletState
   bulletState="fire"
   screen.blit(bulletImg,(x+16,y+10))

def enemybullet(x,y):
    screen.blit(enemybulletImg,(enemybulletX,enemybulletY))

player_score=0
def display_score(x,y):
    font=pygame.font.Font('freesansbold.ttf',20)
    show_score= font.render(f"score:{player_score}",True,(255,255,255))
    screen.blit(show_score,(x,y))

player_lives=5
def display_player_lives(x,y):
    font=pygame.font.Font('freesansbold.ttf',20)
    show_lives= font.render(f"player-lives:{player_lives}",True,(255,255,255))
    screen.blit(show_lives,(x,y))

#PlayAgainButton
def button():
    btn_rect = pygame.draw.rect(screen, (110, 207, 7), (200, 300, 250, 60))
    font = pygame.font.Font('freesansbold.ttf', 40)
    btn_font = font.render("Play Again", True, (255, 255, 255))
    text_rect = btn_font.get_rect(center=btn_rect.center)
    screen.blit(btn_font, text_rect)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if btn_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, (255, 34, 8), btn_rect)  
        pygame.mouse.set_cursor(pygame.cursors.diamond)
        screen.blit(btn_font, text_rect)
        if pygame.mouse.get_pressed()[0]:  
            return True
    return False

#GameStatus
def gameover(game_status):
    screen.fill((0, 0, 0))
    font=pygame.font.Font(None,50)
    show_status=font.render(game_status,True,(255,255,255))
    screen.blit(show_status,(30,200)) 
    button()
    pygame.display.update()
   
#CollisionDetection
def enemy_collision(enemyX,enemyY,BulletX,BulletY):
    dist=math.sqrt(math.pow((enemyX-BulletX),2)+math.pow((enemyY-BulletY),2))
    if dist<=27:
        return True
    else:
        return False
    
def player_collision(playerX, playerY, enemybulletX, enemybulletY):
    dist = math.sqrt(math.pow((playerX - enemybulletX), 2) + math.pow((playerY - enemybulletY), 2))
    if dist <= 27:
        return True
    else:
        return False
    


gamedone=False

#GameLoop
running=True
while running:

    screen.blit(bg,(0,0))
    enemybulletY+=enemyBulletYchange
    
    if enemybulletY>=450:
        enemybulletX=enemyX
        enemybulletY=enemyY

    if playerX<=0:
        playerX=0
    elif playerX>=540:
        playerX=540
        
    if playerY>=400:
        playerY=400
    elif playerY<=0:
        playerY=0

    enemyX+=enemyX_Change
    if enemyX<=0:
        enemyX_Change=2.5
        enemyY+=enemyY_change
    elif enemyX>=540:
         enemyX_Change=-2.5
         enemyY+=enemyY_change

    enemybullet(enemybulletX,enemybulletY)

    enemycollision= enemy_collision(enemyX,enemyY,bulletX,bulletY)
    if enemycollision:
        screen.blit(explosion,(enemyX,enemyY))
        player_score+=1
        bulletY=playerY
        bulletX=playerX
        bulletState="ready"
        enemyX=randint(0,640)
        enemyY=randint(0,150)
        pygame.display.update()
        # pygame.time.delay(1000)

    playercollision = player_collision(playerX,playerY,enemybulletX,enemybulletY)
    if playercollision:
        screen.blit(explosion, (playerX, playerY)) 
        # player_lives-=1  
        playerHealth-=5
        playerX=randint(0,640)
        PlayerY=randint(300,450)
        enemybulletX = enemyX  
        enemybulletY = enemyY
        pygame.display.update()
        # playerX = 300
        # playerY = 400
        # pygame.time.delay(1000)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bulletsound.play()
                    bulletX = playerX
                    bulletY=playerY
                    fire_bullet(bulletX, bulletY)

    if bulletY<=0:
        bulletY=playerY-20
        bulletX=playerX
        bulletState="ready"

    if bulletState=="fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletYchange
        

  
    keys=pygame.key.get_pressed()
    if (keys[K_d]):
        playerX+=4.5
    if (keys[K_a]):
        playerX-=4.5
    if (keys[K_w]):
        playerY-=4.5
    if (keys[K_s]):
        playerY+=4.5

    if player_score>=10:
        gamedone=True
        gameover("Thank you for playing You Won !!!!")
        if button():
            gamedone=False
            screen.blit(bg,(0,0))
        pygame.display.update()

    elif playerHealth<=0:
        gamedone=True
        gameover("You Lost better luck next time !!!")
        if button():
            gamedone=False
            screen.blit(bg,(0,0))
        pygame.display.update()

    # if player_score >= 5:
    #     gameover_msg = "Thank you for playing You Won !!!"
    # elif player_lives<=0:
    #     gameover_msg = "You Lost better luck next time !!!"
    #     gameover(gameover_msg)
    #     if button():
    #         gamedone = False
    #         pygame.display.update()
    #     else:
    #         gamedone=True


#callingPlayer,Enemy
    if (gamedone!=True):
        player(playerX,playerY)
        healthbar(playerX,playerY,playerHealth)
        enemy()
        display_score(10,10)
        display_player_lives(500,10)
        clock.tick(60)
        pygame.display.update()