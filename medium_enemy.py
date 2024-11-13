import pygame
import math

class Enemy:
    def __init__(self, x, y, speed):
        self.image = pygame.image.load("assets/enemy.png") 
        self.image = pygame.transform.scale(self.image, (30, 30)) #ขนาดเป็น pixel
        self.speed = speed
        self.rect = self.image.get_rect(center=(x, y)) #ขอบเขตการเดิน
        self.image = pygame.transform.scale(self.image, (30, 30))  # Set size of the enemy image
        self.rect = self.image.get_rect(center=(x, y))  # Set the position of the enemy
        self.speed = speed

        # Health variables
        self.enemy_max_health = 50
        self.enemy_health = self.enemy_max_health
        self.health_bar_width = 35  
        self.health_bar_height = 5
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)

    def move_towards_player(self, player_rect): #เดินออโต้
        
        dx = player_rect.x - self.rect.x
        dy = player_rect.y - self.rect.y
        distance = math.hypot(dx, dy)
        
        if distance > 0:  
            dx /= distance
            dy /= distance

        
        # Color for health bar
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)

        # Initialize alive attribute to track if the enemy is alive
        self.alive = True

    def move_towards_player(self, player_rect):  # Automatically move towards the player
        dx = player_rect.x - self.rect.x
        dy = player_rect.y - self.rect.y
        distance = math.hypot(dx, dy)

        if distance > 0:  # Prevent division by zero if distance is 0
            dx /= distance
            dy /= distance

        # Move the enemy
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw_health_bar(self, screen):
        health_ratio = self.enemy_health / self.enemy_max_health
        current_health_width = self.health_bar_width * health_ratio
       
        health_bar_rect = pygame.Rect(
            self.rect.x, self.rect.y - 10, self.health_bar_width, self.health_bar_height)
        pygame.draw.rect(screen, self.red, health_bar_rect) 
        pygame.draw.rect(screen, self.green, 
                         (health_bar_rect.x, health_bar_rect.y, current_health_width, self.health_bar_height))  # Health bar (green)

    def update(self, screen, player_rect):
        if self.enemy_health > 0:  
            self.move_towards_player(player_rect)  
            screen.blit(self.image, self.rect) 
            self.draw_health_bar(screen)

    def update(self, screen, player_rect):
        if self.enemy_health > 0:  # If enemy is alive, update movement and health bar
            self.move_towards_player(player_rect)  
            screen.blit(self.image, self.rect)  # Draw the enemy
            self.draw_health_bar(screen)

        else:
            self.alive = False  # If health is zero, set the enemy as dead

    def is_near_player(self, player_rect, attack_radius=10):
        distance = math.hypot(player_rect.x - self.rect.x, player_rect.y - self.rect.y)
        return distance < attack_radius

    def take_damage(self, amount):
        self.enemy_health -= amount
        if self.enemy_health < 0:
            self.enemy_health = 0
        if self.enemy_health <= 0:
            self.enemy_health = 0
            self.alive = False  # Set enemy as dead when health reaches 0
