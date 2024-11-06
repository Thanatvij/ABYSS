import pygame
import math

class Enemy:
    def __init__(self, x, y, speed):
        self.image = pygame.image.load("assets/enemy.png") 
        self.image = pygame.transform.scale(self.image, (30, 30))  # Size in pixels
        self.rect = self.image.get_rect(center=(x, y))  # Boundaries for movement
        self.speed = speed
        
        self.enemy_max_health = 50
        self.enemy_health = self.enemy_max_health
        self.health_bar_width = 35  
        self.health_bar_height = 5
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        
        self.alive = True  # Add the alive attribute

    def move_towards_player(self, player_rect):  # Auto-move towards player
        dx = player_rect.x - self.rect.x
        dy = player_rect.y - self.rect.y
        distance = math.hypot(dx, dy)
        
        if distance > 0:  
            dx /= distance
            dy /= distance
        
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw_health_bar(self, screen):
        health_ratio = self.enemy_health / self.enemy_max_health
        current_health_width = self.health_bar_width * health_ratio
        
        health_bar_rect = pygame.Rect(
            self.rect.x, self.rect.y - 10, self.health_bar_width, self.health_bar_height
        )
        
        pygame.draw.rect(screen, self.red, health_bar_rect)  # Draw the red background for health bar
        pygame.draw.rect(screen, self.green, 
                         (health_bar_rect.x, health_bar_rect.y, current_health_width, self.health_bar_height))  # Health bar (green)

    def update(self, screen, player_rect):
        if self.alive:  # Only update if the enemy is alive
            if self.enemy_health > 0:  
                self.move_towards_player(player_rect)  
                screen.blit(self.image, self.rect) 
                self.draw_health_bar(screen)

    def is_near_player(self, player_rect, attack_radius=10):
        distance = math.hypot(player_rect.x - self.rect.x, player_rect.y - self.rect.y)
        return distance < attack_radius

    def take_damage(self, amount):
        if self.alive:  # Ensure enemy can only take damage if it's alive
            self.enemy_health -= amount
            if self.enemy_health <= 0:
                self.enemy_health = 0
                self.alive = False  # Set alive to False when health is 0 or below