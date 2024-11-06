import pygame
from itertools import cycle
import subprocess
import sys
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/Mainchar.webp"), (35, 35))
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 100  # Initial health for the player

    def update(self, keys, speed, screen_w, screen_h):
        # Player movement
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= speed
        if keys[pygame.K_s] and self.rect.bottom < screen_h:
            self.rect.y += speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= speed
        if keys[pygame.K_d] and self.rect.right < screen_w:
            self.rect.x += speed

class AttackAnimation(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.frames = [pygame.image.load(f"assets/attack/{i}.png") for i in range(1, 6)]
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
        if distance == 0:  # Avoid division by zero
            distance = 1
        self.velocity_x = (direction_x / distance) * 10
        self.velocity_y = (direction_y / distance) * 10

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Check if the attack has moved off the screen and deactivate it
        if not (0 <= self.rect.x <= 1280 and 0 <= self.rect.y <= 720):
            self.kill()

        # Animation logic
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.image = next(self.frame_cycle)
            self.counter = 0
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__()
        self.image = pygame.Surface((10, 100))  # Create a 10x10 surface for the projectile
        self.image.fill((255, 0, 0))  # Fill it with red color
        self.rect = self.image.get_rect(center=(x, y))  # Set its position
        self.velocity_x = velocity_x  # Horizontal velocity
        self.velocity_y = velocity_y  # Vertical velocity
        self.damage = 500  # Projectile damage

    def update(self):
        # Move the projectile according to its velocity
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Remove the projectile if it moves off-screen
        if not (0 <= self.rect.x <= 1280 and 0 <= self.rect.y <= 720):
            self.kill()
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/enemy.png"), (300, 300))
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 1000
        self.max_health = 1000  # Add max health for the boss
        self.last_shot_time = 0
        self.shot_interval = 500  # Reduced shot interval to make the boss shoot faster (500ms)

    def shoot(self, player_rect):
        direction_x = player_rect.centerx - self.rect.centerx
        direction_y = player_rect.centery - self.rect.centery
        distance = math.hypot(direction_x, direction_y)
        if distance == 0:  # Avoid division by zero
            distance = 1
        velocity_x = (direction_x / distance) * 5
        velocity_y = (direction_y / distance) * 5
        return Projectile(self.rect.centerx, self.rect.centery, velocity_x, velocity_y)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def update(self, current_time, player_rect, projectile_group):
        # Shoot at intervals (adjusted to shoot faster)
        if current_time - self.last_shot_time > self.shot_interval:
            projectile = self.shoot(player_rect)
            projectile_group.add(projectile)
            self.last_shot_time = current_time

    def draw_health_bar(self, screen):
        # Draw the health bar for the boss
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = self.health / self.max_health
        current_health_width = health_bar_width * health_ratio

        # Draw the background (red) of the health bar
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.centerx - health_bar_width // 2, self.rect.top - 30, health_bar_width, health_bar_height))
        # Draw the current health (green)
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.centerx - health_bar_width // 2, self.rect.top - 30, current_health_width, health_bar_height))


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__()
        self.image = pygame.Surface((10, 100))  # Create a 10x100 surface for the laser beam
        self.image.fill((255, 0, 0))  # Fill it with red color (could change to match laser color)
        self.rect = self.image.get_rect(center=(x, y))  # Set its position
        self.velocity_x = velocity_x  # Horizontal velocity
        self.velocity_y = velocity_y  # Vertical velocity
        self.damage = 20  # Increased damage for the laser beam

    def update(self):
        # Move the projectile according to its velocity
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Remove the projectile if it moves off-screen
        if not (0 <= self.rect.x <= 1280 and 0 <= self.rect.y <= 720):
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/Mainchar.webp"), (35, 35))
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 100  # Initial health for the player

    def update(self, keys, speed, screen_w, screen_h):
        # Player movement
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= speed
        if keys[pygame.K_s] and self.rect.bottom < screen_h:
            self.rect.y += speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= speed
        if keys[pygame.K_d] and self.rect.right < screen_w:
            self.rect.x += speed

def start_game():
    pygame.init()
    pygame.display.set_caption("Abyss")

    clock = pygame.time.Clock()
    FPS = 60
    speed = 5
    player_max_health = 100

    screen_w = 1280
    screen_h = 720
    screen = pygame.display.set_mode((screen_w, screen_h))
    
    player = Player(640, 360)
    player_group = pygame.sprite.GroupSingle(player)

    boss = Boss(screen_w // 2, screen_h // 2)
    boss_group = pygame.sprite.GroupSingle(boss)
    attack_sprites = pygame.sprite.Group()
    projectile_group = pygame.sprite.Group()

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    attack = AttackAnimation(player.rect.centerx, player.rect.centery, mouse_x, mouse_y)
                    attack_sprites.add(attack)

        keys = pygame.key.get_pressed()
        player.update(keys, speed, screen_w, screen_h)

        player_group.draw(screen)

        boss_group.update(current_time, player.rect, projectile_group)
        boss_group.draw(screen)

        # Draw the boss's health bar
        boss.draw_health_bar(screen)

        # Check for collision between boss and attack
        hits = pygame.sprite.spritecollide(boss, attack_sprites, True)
        for hit in hits:
            boss.take_damage(hit.damage)

        # Check for collision between player and projectiles
        player_hits = pygame.sprite.spritecollide(player, projectile_group, True)
        for hit in player_hits:
            player.health -= hit.damage  # Apply projectile damage to the player

        # Draw the player's health bar
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = player.health / player_max_health
        current_health_width = health_bar_width * health_ratio
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (10, 10, current_health_width, health_bar_height))

        attack_sprites.update()
        attack_sprites.draw(screen)

        projectile_group.update()
        projectile_group.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

        if player.health <= 0:
            running = False

    pygame.quit()

start_game()