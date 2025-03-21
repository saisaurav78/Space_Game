import pygame
from pygame import *
from random import *
import math

# Creating Display
pygame.init()
pygame.display.set_caption("Space World")
screen = pygame.display.set_mode((640, 480))
icon = pygame.image.load("spacegame/assets/images/player.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
bg = pygame.image.load("spacegame/assets/images/bg.jpg")
playerimg = pygame.image.load("spacegame/assets/images/player.png")
enemyimg = pygame.image.load("spacegame/assets/images/ufo.png")
bulletimg = pygame.image.load("spacegame/assets/images/bullet.png")
enemyBulletimg = pygame.image.load("spacegame/assets/images/enemybullets.png")
blastimg =pygame.image.load("spacegame/assets/images/blast.png")


# Load bullet fire sound
bullet_fire_sound = pygame.mixer.Sound("spacegame/assets/sounds/gunshot.wav")  

# Set colors
black = (0, 0, 0)
white = (255, 255, 255)

# Define options and font
options = {1: 'Start Game', 2: 'Quit Game'}
def get_font(size):
    return pygame.font.Font('freesansbold.ttf', size)


class UI:
    def __init__(self,level,score):
        self.font=get_font(20)
        self.level=level
        self.score=score

    def render(self, text, x_pos, y_pos, value):
        rendered_text=self.font.render(f"{text}:{value}", True, white)
        screen.blit(rendered_text, (x_pos,y_pos) )


    class Menu:
        def __init__(self, bg, color, options, x_pos, y_pos):
            self.bg = bg
            self.color = color
            self.font = get_font(50)
            self.options = options
            self.x_pos = x_pos
            self.original_y_pos = y_pos
            self.y_pos = y_pos

        def render_menu(self, event):
            self.y_pos = self.original_y_pos
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for key, option in self.options.items():
                menu_rect = pygame.Rect(self.x_pos, self.y_pos, 280, 50)
                rect_color = (32, 227, 38) if menu_rect.collidepoint(mouse_x, mouse_y) else (27, 123, 196)
                pygame.draw.rect(screen, rect_color, menu_rect)
                text = self.font.render(option, True, self.color)
                text_rect = text.get_rect(center=(self.x_pos + 140, self.y_pos + 25))
                screen.blit(text, text_rect)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and menu_rect.collidepoint(mouse_x, mouse_y):
                    print(f'Option chosen: {option}')

                self.y_pos += 100

# Menu Object


# Ship Object
class Ship:
    class Bullet:
        def __init__(self, BulletImg, BulletX, BulletY):
            self.bulletImg = BulletImg
            self.bulletX = BulletX  
            self.bulletY = BulletY
        
        def move_Y(self):
            self.bulletY -= 10

    def __init__(self, ShipImg, X_pos, Y_pos, Health):
        self.ShipImg = ShipImg
        self.X_pos = X_pos
        self.Y_pos = Y_pos
        self.Health = Health

    def move_X(self, KEY):
        if(KEY[K_LEFT] or KEY[K_a]):
            if self.X_pos <= 5:
                self.X_pos = 5
            self.X_pos -= 5
        elif (KEY[K_RIGHT] or KEY[K_d]):
            if self.X_pos >= 570:
                self.X_pos = 570
            self.X_pos += 5

    def healthbar(self):
        x = self.X_pos
        y = self.Y_pos

        if self.Health >60:
            color = (0, 255, 0)  # Green
        elif self.Health > 20 and self.Health<=60:
            color = (255, 255, 0)  # Yellow
        else:
            color = (255, 0, 0)  # Red
        
        pygame.draw.rect(screen, color, (x-15 , y+69 , self.Health, 8))

    def collision(self, bulletX, bulletY):
        distance = math.sqrt(math.pow((self.X_pos - bulletX), 2) + math.pow((self.Y_pos - bulletY), 2))
        if distance < 27: 
            return True
        return False


# Enemy Object
class Enemy(Ship):
    class EnemyBullet:
        def __init__(self, BulletImg, BulletX, BulletY):
            self.bulletImg = BulletImg
            self.bulletX = BulletX  
            self.bulletY = BulletY
        
        def move_Y(self):
            self.bulletY += 10

    def __init__(self, Img, X_pos, Y_pos, Health, Direction):
        super().__init__(Img, X_pos, Y_pos, Health)
        self.Direction = Direction
        
    def move_X(self):
        if self.X_pos <= 0 or self.X_pos >= 570:
            self.Direction = -self.Direction
        self.X_pos += 2 * self.Direction

# Initialize Player
Player = Ship(playerimg, 300, 400, 100) 

# Enemy management
enemies = []
level = 1
score=0
enemycount = 3

if level == 2:
    enemycount = 5
elif level == 3:
    enemycount = 7

for i in range(enemycount):
    direction = 1 if randint(0, 1) == 0 else -1
    enemy = Enemy(enemyimg, randint(0, 400), randint(0, 150), 100, direction)
    enemies.append(enemy)

# Initialize the PlayerBullet variable to None
PlayerBullet = None  
enemyBullets = []

# Main Loop
running = True
displaying_level=False
ui=UI(level, score)
mainmenu = UI.Menu(None,  white, options, 180, 150)
gameloop = False
starting_game = False  # New variable to track if the game is starting



while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for key, option in options.items():
                menu_rect = pygame.Rect(180, 150 + (key - 1) * 100, 280, 50)
                if menu_rect.collidepoint(mouse_x, mouse_y):
                    if key == 1:  # Start Game
                        gameloop = True
                        starting_game = True
                    elif key == 2:  # Quit Game
                        running = False

    if starting_game:
        screen.fill(black)
        starting_text = get_font(50).render("Starting Game...", True, white)
        text_rect = starting_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(starting_text, text_rect)
        pygame.display.update()
        pygame.time.delay(2000)
        starting_game = False
        continue

    if gameloop:
        screen.blit(bg, (0, 0))
        ui.render('level', 5,10, 0)
        ui.render('score', 550,10, score)
        if Player.Health!=0:
            screen.blit(Player.ShipImg, (Player.X_pos, Player.Y_pos))
            Player.healthbar() 

        # Check if the bullet is active before drawing it
        if PlayerBullet:
            screen.blit(PlayerBullet.bulletImg, (PlayerBullet.bulletX, PlayerBullet.bulletY))
            PlayerBullet.move_Y()
            # Reset the bullet if it goes off-screen
            if PlayerBullet.bulletY < 0:
                PlayerBullet = None  # Reset the bullet if it goes off-screen

        # Fire bullet when space is pressed
        KEY = pygame.key.get_pressed()
        if KEY[K_SPACE] and PlayerBullet is None:
            PlayerBullet = Ship.Bullet(bulletimg, Player.X_pos + 16, Player.Y_pos - 16)  # Create a new bullet
            bullet_fire_sound.play()  # Play bullet fire sound when bullet is created

        for enemy in enemies:
            screen.blit(enemy.ShipImg, (enemy.X_pos, enemy.Y_pos))
            enemy.move_X()      

            if random() < 0.006: #Enemy Bullets frequency
                # Create a new enemy bullet starting from the enemy's position
                new_enemy_bullet = Enemy.EnemyBullet(enemyBulletimg, enemy.X_pos + 16, enemy.Y_pos + 20)  # Adjusted starting position
                enemyBullets.append(new_enemy_bullet)

         
            if PlayerBullet and enemy.collision(PlayerBullet.bulletX, PlayerBullet.bulletY):
                screen.blit(blastimg, (enemy.X_pos, enemy.Y_pos))

                enemy.X_pos = randint(0, 400)
                enemy.Y_pos = randint(0, 150)

                PlayerBullet = None  # Remove bullet on hit
                score+=1     


        for bullet in enemyBullets:
            bullet.move_Y()  # Update bullet position
            screen.blit(bullet.bulletImg, (bullet.bulletX, bullet.bulletY))  # Draw bullet at its own position
            if bullet.bulletY > 480:  # Remove bullet if it goes off screen
                enemyBullets.remove(bullet)

             # Collision Detection for Enemy Bullets
            player_collision = Player.collision(bullet.bulletX, bullet.bulletY)
            if player_collision:
                screen.blit(blastimg, (Player.X_pos, Player.Y_pos))
                Player.Health -= 10
                enemyBullets.remove(bullet)

        Player.move_X(KEY)

    if not gameloop:
        mainmenu.render_menu(event)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
