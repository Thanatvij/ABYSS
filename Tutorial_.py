import pygame
from enemy import Enemy
from itertools import cycle
import subprocess
import sys
import math

class AttackAnimation(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.frames = [
            pygame.image.load(f"assets/attack/{i}.png") for i in range(1, 6)
        ]
        self.frames = [pygame.transform.scale(frame, (50, 50)) for frame in self.frames]
        self.frame_cycle = cycle(self.frames)
        self.image = next(self.frame_cycle)
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 5
        self.counter = 0
        self.damage = 10

        # Calculate direction to target
        direction_x = target_x - x
        direction_y = target_y - y
        distance = math.hypot(direction_x, direction_y)
        if distance == 0:
            distance = 1
        self.velocity_x = (direction_x / distance) * 10
        self.velocity_y = (direction_y / distance) * 10

    def update(self):
        # Move the attack animation toward the target
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Check if the attack has moved off the screen and remove it
        if not (0 <= self.rect.x <= 1280 and 0 <= self.rect.y <= 720):
            self.kill()

        # Animation logic
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.image = next(self.frame_cycle)
            self.counter = 0

def start_game():
    pygame.init()
    pygame.display.set_caption("Abyss")

    clock = pygame.time.Clock()
    FPS = 60
    speed = 5
    player_max_health = 100  
    player_health = player_max_health

    # Backgrounds
    screen_w = 1280        
    screen_h = 720
    screen = pygame.display.set_mode((screen_w, screen_h))
    screen_rect = screen.get_rect()
    background = pygame.image.load("assets/wallpaper.png")
    background = pygame.transform.scale(background, (1280, 720))

    # Colors
    red = (255, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)

    # Character
    player_image = pygame.image.load("assets/Mainchar.webp")
    player_image = pygame.transform.scale(player_image, (35, 35))
    player_rect = player_image.get_rect(center=(640, 360))

    # Enemies
    enemies = [Enemy(200 + i * 10, 100 + i * 5, 2) for i in range(5)]
    attack_sprites = pygame.sprite.Group()

    # Door and Room state
    door_rect = pygame.Rect(640, 0, 100, 20)
    door_open = False

    # Fire delay
    fire_delay = 10
    fire_spawn_time = 0

    # Game loop
    running = True
    next_game_triggered = False

    while running:
        # Fill the screen with the background
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spawn attack animation based on fire delay
        fire_spawn_time += 1
        if fire_spawn_time >= fire_delay:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            attack = AttackAnimation(player_rect.centerx, player_rect.centery, mouse_x, mouse_y)
            attack_sprites.add(attack)
            fire_spawn_time = 0  # Reset spawn timer

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player_rect.top > 0:
            player_rect.y -= speed
        if keys[pygame.K_s] and player_rect.bottom < screen_h:
            player_rect.y += speed
        if keys[pygame.K_a] and player_rect.left > 0:
            player_rect.x -= speed
        if keys[pygame.K_d] and player_rect.right < screen_w:
            player_rect.x += speed

        # Draw player
        screen.blit(player_image, player_rect)

        # Update and draw all enemies
        for enemy in enemies:
            enemy.update(screen, player_rect)
            
            hits = pygame.sprite.spritecollide(enemy, attack_sprites, True)
            for hit in hits:
                enemy.take_damage(hit.damage)
            
            if enemy.is_near_player(player_rect):
                player_health -= 0.25
                player_health = max(player_health, 0)

        # Check if all enemies are dead, open the door
        if all(not enemy.alive for enemy in enemies):
            door_open = True

        # Draw the door
        if door_open:
            pygame.draw.rect(screen, white, door_rect)

        # Check if the player collides with the door and transition only once
        if door_open and player_rect.colliderect(door_rect) and not next_game_triggered:
            pygame.display.update()
            pygame.time.delay(500)
            pygame.quit()
            next_game_triggered = True
            try:
                subprocess.run([sys.executable, 'attack_water.py'])
            except Exception as e:
                print(f"Failed to start attack_water game: {e}")
            break

        # Check if player health is zero
        if player_health <= 0:
            running = False
            from game_manager import death_screen
            death_screen(screen)

        # Draw the health bar
        health_bar_width = 35
        health_bar_height = 4
        health_ratio = player_health / player_max_health
        current_health_width = health_bar_width * health_ratio
        hp_x = player_rect.centerx - health_bar_width // 2
        hp_y = player_rect.top - health_bar_height - 5 
        pygame.draw.rect(screen, red, (hp_x, hp_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, green, (hp_x, hp_y, current_health_width, health_bar_height))

        # Update and draw attack animations
        attack_sprites.update()
        attack_sprites.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()