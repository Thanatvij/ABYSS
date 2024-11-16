import pygame
from itertools import cycle
import math
import random

def start_boss():
    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load("assets/Mainchar.webp"), (35, 35))
            self.rect = self.image.get_rect(center=(x, 680))
            self.health = 100  # player health

        def update(self, keys, speed, screen_w, screen_h):
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
            self.frames = [pygame.image.load(f"assets/Fire1.png")]
            self.frames = [pygame.transform.scale(frame, (50, 50)) for frame in self.frames]
            self.frame_cycle = cycle(self.frames)
            self.image = next(self.frame_cycle)
            self.rect = self.image.get_rect(center=(x, y))
            self.animation_speed = 5
            self.counter = 0
            self.damage = 2

            direction_x = target_x - x
            direction_y = target_y - y
            distance = math.hypot(direction_x, direction_y)
            if distance == 0: 
                distance = 1
            self.velocity_x = (direction_x / distance) * 10
            self.velocity_y = (direction_y / distance) * 10

        def update(self):
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y
            self.counter += 1
            if self.counter >= self.animation_speed:
                self.image = next(self.frame_cycle)
                self.counter = 0

    class Projectile(pygame.sprite.Sprite):
        def __init__(self, x, y, velocity_x, velocity_y):
            super().__init__()
            self.image = pygame.Surface((20, 20), pygame.SRCALPHA)  # Use SRCALPHA for transparency
            pygame.draw.circle(self.image, (255, 0, 0), (10, 10), 10)  # Draw a red circle
            self.rect = self.image.get_rect(center=(x, y))
            self.velocity_x = velocity_x
            self.velocity_y = velocity_y
            self.damage = 20  # Damage value

        def update(self):
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y
            if not (0 <= self.rect.x <= 1280 and 0 <= self.rect.y <= 720):
                self.kill()

    class Boss(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load("assets/boss.PNG"), (350,200))
            self.rect = self.image.get_rect(center=(x, y))
            self.health = 1000
            self.max_health = 1000 
            self.last_shot_time = 0
            self.shot_interval = 1000  # Shoot every second

        def shoot(self):
            # Fire projectiles in a pattern (e.g., random angle)
            for _ in range(20):  # Adjust the number of projectiles fired
                angle = random.uniform(0, 2 * math.pi)  # Random angle
                velocity_x = math.cos(angle) * 5
                velocity_y = math.sin(angle) * 5
                projectile = Projectile(self.rect.centerx, self.rect.centery, velocity_x, velocity_y)
                projectile_group.add(projectile)

        def take_damage(self, amount):
            self.health -= amount
            if self.health <= 0:
                self.kill()

        def update(self, current_time, player_rect):
            if current_time - self.last_shot_time > self.shot_interval:
                self.shoot()
                self.last_shot_time = current_time

        def draw_health_bar(self, screen):
            health_bar_width = 200
            health_bar_height = 20
            health_ratio = self.health / self.max_health
            current_health_width = health_bar_width * health_ratio
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.centerx - health_bar_width // 2, self.rect.top - 30, health_bar_width, health_bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.centerx - health_bar_width // 2, self.rect.top - 30, current_health_width, health_bar_height))

    # Pygame initialization
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

    fires_spawn_timer = 0
    fires_spawn_delay = 10
    running = True

    while running:
        current_time = pygame.time.get_ticks()
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # Handle attack animations
        fires_spawn_timer += 1
        if fires_spawn_timer >= fires_spawn_delay:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            attack = AttackAnimation(player.rect.centerx, player.rect.centery, mouse_x, mouse_y)
            attack_sprites.add(attack)
            fires_spawn_timer = 0

        # Update player movement
        keys = pygame.key.get_pressed()
        player.update(keys, speed, screen_w, screen_h)

        # Update boss and projectiles
        boss_group.update(current_time, player.rect)
        projectile_group.update()

        # Draw everything
        player_group.draw(screen)
        boss_group.draw(screen)
        boss.draw_health_bar(screen)

        # Handle collisions
        hits = pygame.sprite.spritecollide(boss, attack_sprites, True)
        for hit in hits:
            boss.take_damage(hit.damage)

        player_hits = pygame.sprite.spritecollide(player, projectile_group, True)
        for hit in player_hits:
            player.health -= hit.damage  

        # Draw player health bar
        health_bar_width = 35
        health_bar_height = 4
        health_ratio = player.health / player_max_health
        current_health_width = health_bar_width * health_ratio
        hp_x = player.rect.centerx - health_bar_width // 2
        hp_y = player.rect.top - health_bar_height - 5
        pygame.draw.rect(screen, (255, 0, 0), (hp_x, hp_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (hp_x, hp_y, current_health_width, health_bar_height))

        # Draw attack animations and projectiles
        attack_sprites.update()
        attack_sprites.draw(screen)
        projectile_group.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

        if player.health <= 0:
            running = False
            from game_manager import death_screen
            death_screen(screen)  # Call death screen

    pygame.quit()
        
start_boss()
