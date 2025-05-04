import asyncio
import pygame
from pygame import *
from random import *
import math

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 2

# GameState
class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    VICTORY = 3
    QUITTING = 4

# Asset loading functions
def load_image(path, scale=None):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, scale) if scale else img
    except pygame.error as e:
        print(f"Error loading {path}: {e}")
        surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        surface.fill((255, 0, 255))
        return surface

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        print(f"Error loading sound: {path}")
        return None

# Initialize pygame
pygame.init()
pygame.display.set_caption("Space World")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load assets
def load_assets():
    assets = {
        'icon': load_image("assets/images/player.png"),
        'bg': load_image("assets/images/bg.jpg", (SCREEN_WIDTH, SCREEN_HEIGHT)),
        'player': load_image("assets/images/player.png", scale=(62, 62)),
        'enemy': load_image("assets/images/ufo.png", scale=(60, 60)),
        'bullet': load_image("assets/images/bullet.png"),
        'enemy_bullet': load_image("assets/images/enemybullets.png"),
        'blast': load_image("assets/images/blast.png"),
        'bullet_sound': load_sound("assets/sounds/bullet.ogg"),
        'menu_select_sound': load_sound("assets/sounds/menu_select.ogg"),
        'explosion_sound': load_sound("assets/sounds/explosion.ogg"),
    }
    pygame.display.set_icon(assets['icon'])
    return assets

assets = load_assets()

# Explosion tracking
explosions = []

# Class for UI 
class Menu:
    def __init__(self, options, x_pos, y_pos):
        self.options = options
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = pygame.font.Font('freesansbold.ttf', 50)
        self.hovered_last_frame = {key: False for key in options}
    
    def render(self, screen):
        title_font = pygame.font.Font('freesansbold.ttf', 50)
        title_text = title_font.render("Welcome to Space World", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title_text, title_rect)
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (key, option) in enumerate(self.options.items()):
            rect = pygame.Rect(self.x_pos, self.y_pos + i*100, 280, 50)
            if rect.collidepoint(mouse_pos):
                color = (32, 227, 38)
                if not self.hovered_last_frame[key]:
                    self.hovered_last_frame[key] = True
                    if assets['menu_select_sound']:
                        assets['menu_select_sound'].play()
            else:
                self.hovered_last_frame[key] = False
                color = (27, 123, 196)
            
            pygame.draw.rect(screen, color, rect)
            text = self.font.render(option, True, WHITE)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
    
    def handle_click(self, pos):
        for i, (key, option) in enumerate(self.options.items()):
            rect = pygame.Rect(self.x_pos, self.y_pos + i*100, 280, 50)
            if rect.collidepoint(pos):
                return key
        return None

# Class for Bullets
class Bullet:
    def __init__(self, image, x, y, speed, is_enemy=False):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed
        self.is_enemy = is_enemy
        self.active = True
    
    def update(self):
        self.y += self.speed * (1 if self.is_enemy else -1)
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            self.active = False
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Ship Class   
class Ship:
    def __init__(self, image, x, y, health):
        self.image = image
        self.x = x
        self.y = y
        self.health = health
        self.width = image.get_width()
        self.height = image.get_height()
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.draw_healthbar(screen)
    
    def draw_healthbar(self, screen):
        if self.health > 60:
            color = (0, 255, 0)
        elif self.health > 30:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        bar_width = max(0, min(self.health, 100))
        pygame.draw.rect(screen, color, (self.x-15, self.y + self.height + 8, bar_width, 6))

# Player Class
class Player(Ship):
    def __init__(self, image, x, y):
        super().__init__(image, x, y, 100)
        self.bullet_cooldown = 0
    
    def update(self, keys):
        if self.health <= 0:
            return
        if keys[K_LEFT] or keys[K_a]:
            self.x = max(0, self.x - PLAYER_SPEED)
        if keys[K_RIGHT] or keys[K_d]:
            self.x = min(SCREEN_WIDTH - self.width, self.x + PLAYER_SPEED)
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1
    
    def shoot(self):
        if self.bullet_cooldown == 0 and self.health > 0:
            self.bullet_cooldown = 15
            if assets['bullet_sound']:
                assets['bullet_sound'].play()
            return Bullet(assets['bullet'], self.x + self.width//2 - 8, self.y, BULLET_SPEED)
        return None

# Enemy Class
class Enemy(Ship):
    def __init__(self, image, x, y, direction):
        super().__init__(image, x, y, 100)
        self.direction = direction
        self.shoot_timer = randint(30, 150)
    
    def update(self):
        self.x += ENEMY_SPEED * self.direction
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.direction *= -1
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_timer = randint(30, 180)
            return Bullet(assets['enemy_bullet'], 
                         self.x + self.width//2 - 8, 
                         self.y + self.height, 
                         BULLET_SPEED//2, True)
        return None

# Explosion management
def create_explosion(x, y):
    """Start an explosion at (x, y)"""
    explosions.append({
        'x': x,
        'y': y,
        'start_time': pygame.time.get_ticks()
    })
    if assets['explosion_sound']:
        assets['explosion_sound'].play()

# Enemy spawning function
def spawn_enemies(count):
    return [Enemy(assets['enemy'], randint(50, SCREEN_WIDTH-100), randint(50, 150), 1 if randint(0, 1) else -1) for _ in range(count)]

# Reset game function
def reset_game():
    global player, enemies, player_bullets, enemy_bullets, score, level, game_state
    player = Player(assets['player'], SCREEN_WIDTH//2, SCREEN_HEIGHT-100)
    enemies = spawn_enemies(3 + (level-1)*2)
    player_bullets = []
    enemy_bullets = []
    game_state = GameState.PLAYING

# Game initialization
player = Player(assets['player'], SCREEN_WIDTH//2, SCREEN_HEIGHT-100)
enemies = []
player_bullets = []
enemy_bullets = []
score = 0
level = 1
game_state = GameState.MENU
menu = Menu({1: 'Start Game', 2: 'Quit Game'}, 180, 150)

#Async function to run the game loop
async def main():
    global running, game_state, player, enemies, player_bullets, enemy_bullets, score, level
  
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_state == GameState.MENU and event.type == pygame.MOUSEBUTTONDOWN:
                choice = menu.handle_click(event.pos)
                if choice == 1:  # Start Game
                    reset_game()
                elif choice == 2:  # Quit Game
                    game_state = GameState.QUITTING  # Transition to quitting state
        
        # Get keyboard state
        keys = pygame.key.get_pressed()
        
        # Handle input for game over/victory screens
        if game_state in (GameState.GAME_OVER, GameState.VICTORY):
            if keys[K_r]:
                level = 1
                score = 0
                reset_game()
            elif keys[K_ESCAPE]:
                game_state = GameState.MENU
        
        # Game state updates
        if game_state == GameState.PLAYING:
            player.update(keys)
            if keys[K_SPACE]:
                new_bullet = player.shoot()
                if new_bullet:
                    player_bullets.append(new_bullet)
            
            # Update bullets
            for bullet in player_bullets[:]:
                bullet.update()
                if not bullet.active:
                    player_bullets.remove(bullet)
            
            for bullet in enemy_bullets[:]:
                bullet.update()
                if not bullet.active:
                    enemy_bullets.remove(bullet)
            
            # Update enemies and their shooting
            for enemy in enemies[:]:
                new_bullet = enemy.update()
                if new_bullet:
                    enemy_bullets.append(new_bullet)
                
                # Check collision with player bullets
                for bullet in player_bullets[:]:
                    if math.sqrt((enemy.x - bullet.x)**2 + (enemy.y - bullet.y)**2) < 30:
                        player_bullets.remove(bullet)
                        enemy.health -= 25
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                            score += 10
                            create_explosion(enemy.x + enemy.width//2, enemy.y + enemy.height//2)
                        break
            
            # Check collision with enemy bullets
            for bullet in enemy_bullets[:]:
                if (player.health > 0 and math.sqrt((player.x - bullet.x)**2 + (player.y - bullet.y)**2) < 30):
                    enemy_bullets.remove(bullet)
                    player.health -= 10
                    if player.health <= 0:
                        create_explosion(player.x + player.width//2, player.y + player.height//2)
                        game_state = GameState.GAME_OVER
                    break
            
            # Level progression
            if not enemies:
                level += 1
                if level > 5:  # Win condition
                    game_state = GameState.VICTORY
                else:
                    enemies = spawn_enemies(3 + (level-1)*2)
        
        # Rendering
        if game_state == GameState.MENU:
            screen.blit(assets['bg'], (0, 0))
            menu.render(screen)
        
        elif game_state == GameState.PLAYING:
            screen.blit(assets['bg'], (0, 0))
            player.draw(screen)
            
            # Draw bullets
            for bullet in player_bullets + enemy_bullets:
                bullet.draw(screen)
            
            # Draw enemies
            for enemy in enemies:
                enemy.draw(screen)
            
            # Draw explosions
            current_time = pygame.time.get_ticks()
            for explosion in explosions[:]:
                elapsed = current_time - explosion['start_time']
                if elapsed < 190:  # Duration in ms
                    progress = elapsed / 190
                    scale = int(30 + 50 * progress)
                    scaled_blast = pygame.transform.scale(assets['blast'], (scale, scale))
                    rect = scaled_blast.get_rect(center=(explosion['x'], explosion['y']))
                    screen.blit(scaled_blast, rect)
                else:
                    explosions.remove(explosion)
            
            # Draw UI
            font = pygame.font.Font('freesansbold.ttf', 18)
            level_text = font.render(f"Level: {level}", True, WHITE)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(level_text, (10, 10))
            screen.blit(score_text, (SCREEN_WIDTH-110, 10))
        
        # Game Over Screen
        elif game_state == GameState.GAME_OVER:
            screen.fill(BLACK)
            game_over_font = pygame.font.Font('freesansbold.ttf', 50)
            game_over_text = game_over_font.render("Game Over", True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80))
            screen.blit(game_over_text, text_rect) 
            score_font = pygame.font.Font('freesansbold.ttf', 30)
            score_text = score_font.render(f"Final Score: {score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 5))
            screen.blit(score_text, score_rect)    
            restart_text = font.render("Press R to restart or ESC for menu", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
            screen.blit(restart_text, restart_rect)
        
        # Game Victory Screen
        elif game_state == GameState.VICTORY:
            screen.fill(BLACK)
            victory_font = pygame.font.Font('freesansbold.ttf', 50)
            victory_text = victory_font.render("You Win!", True, WHITE)
            text_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80))
            screen.blit(victory_text, text_rect)
            score_font = pygame.font.Font('freesansbold.ttf', 30)
            score_text = score_font.render(f"Final Score: {score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 5))
            screen.blit(score_text, score_rect)  
            restart_text = font.render("Press R to restart or ESC for menu", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
            screen.blit(restart_text, restart_rect)

         # Quitting Screen
        elif game_state == GameState.QUITTING:
            screen.fill(BLACK)
            font = pygame.font.Font('freesansbold.ttf', 30)
            text = font.render("Quitting game...", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(text, text_rect)
            pygame.display.update()
            await asyncio.sleep(1)  # Wait 1 second
            running = False  # Exit the loop
        
        pygame.display.update()
        clock.tick(FPS)
        await asyncio.sleep(0)  # Required for browser compatibility

# Main entry point
running = True
asyncio.run(main())
pygame.quit()