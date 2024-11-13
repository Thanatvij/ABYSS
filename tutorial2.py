import pygame
from enemy import Enemy
from itertools import cycle
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
        self.active = True
        self.damage = 10

        direction_x = target_x - x
        direction_y = target_y - y
        distance = math.hypot(direction_x, direction_y)
        if distance == 0:
            distance = 1
        self.velocity_x = (direction_x / distance) * 10
        self.velocity_y = (direction_y / distance) * 10

    def update(self):
        if self.active:
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y

            if not (0 <= self.rect.x <= 1280 and 0 <= self.rect.y <= 720):
                self.kill()

            self.counter += 1
            if self.counter >= self.animation_speed:
                self.image = next(self.frame_cycle)
                self.counter = 0

def start_game2():
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
    background = pygame.image.load("assets/wallpaper.png")
    background = pygame.transform.scale(background, (1280, 720))

    # Colors
    black = (0, 0, 0)
    red = (255, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)

    # Character
    player_image = pygame.image.load("assets/Mainchar.webp")
    player_image = pygame.transform.scale(player_image, (35, 35))
    player_rect = player_image.get_rect(center=(640, 360))

    # Fonts
    def get_thai_font(size):
        return pygame.font.Font("assets/Kart-Thai-Khon-Demo.ttf", size)
    font = get_thai_font(size=50)
    text = font.render('SPACEBAR FOR ATTACK', True, (255, 255, 255))
    text_rect = text.get_rect(center=(640, 50))
    dialogue_done = False
    
    # Dialogue setup
    dialogue = [
        "โย่วนี่คือ tutorial นะ",
        "ไหนลองเทสสกิลให้ดูหน่อยซิ",
    ]
    current_dialogue_index = 0
    show_message = True  # Start by showing the message
    message_shown = False
    message_duration = 2000  # Display  message for 2 seconds

    # Message box setup
    message_box = pygame.Rect(100, 550, 1080, 150)
    message_box_color = black
    message_text_color = white
    border_color = white
    border_thickness = 4 

    # Enemies
    enemies = []
    attack_sprites = pygame.sprite.Group()

    # Door and Room state
    door_rect = pygame.Rect(640, 0, 100, 20)  # Door position
    door_open = False  # Track if the door is open

    running = True
    next_game_triggered = False
    message_after_kill = False  # Flag for displaying the message after killing all enemies
    message_time_start = 0  # Time when the message_after_kill started
    message_delay_duration = 2000  # Delay for 2 seconds before closing the message

    while running:
        screen.blit(background, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not message_shown:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    attack = AttackAnimation(player_rect.centerx, player_rect.centery, mouse_x, mouse_y)
                    attack_sprites.add(attack)

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

        # Message display
        if show_message and current_dialogue_index < len(dialogue):
            # Display message box with text
            pygame.draw.rect(screen, border_color, 
                             (message_box.x - border_thickness, message_box.y - border_thickness, 
                              message_box.width + 2 * border_thickness, message_box.height + 2 * border_thickness))
            pygame.draw.rect(screen, message_box_color, message_box)
            text_surface = font.render(dialogue[current_dialogue_index], True, message_text_color)
            screen.blit(text_surface, (message_box.x + 10, message_box.y + 10))
        
            # Track time for message display
            if not message_shown:
                message_start_time = pygame.time.get_ticks()
                message_shown = True

            if pygame.time.get_ticks() - message_start_time > message_duration:
                message_shown = False
                current_dialogue_index += 1
                if current_dialogue_index >= len(dialogue):
                    dialogue_done = True
                    show_message = False
                    enemies = [Enemy(200 + i * 10, 100 + i * 5, 2) for i in range(5)]  # 5 enemies

        if dialogue_done:
            screen.blit(text, text_rect)  # Display "SPACEBAR FOR ATTACK" message

        # Enemy updates
        if not show_message:
            for enemy in enemies:
                enemy.update(screen, player_rect)
                hits = pygame.sprite.spritecollide(enemy, attack_sprites, True)
                for hit in hits:
                    enemy.take_damage(hit.damage)
                if enemy.is_near_player(player_rect):
                    player_health -= 0.25
                    player_health = max(player_health, 0)

            # Check if all enemies are dead
            if all(not enemy.alive for enemy in enemies) and not message_after_kill:
                message_after_kill = True  # Trigger message to appear after all enemies are defeated
                message_time_start = pygame.time.get_ticks()  # Start the 2-second delay

        # Show the "Message after kill" if all enemies are dead
        if message_after_kill:
            dialogue2 = [
                "สุดยอดไปเลยนี่นา!!!"
                "ฉันว่านายพร้อมกับสนามจริงแล้วละ >_<"
            ]
            current_dialogue_index2 = 0

            if pygame.time.get_ticks() - message_time_start < message_delay_duration:
                pygame.draw.rect(screen, border_color, 
                         (message_box.x - border_thickness, message_box.y - border_thickness, 
                          message_box.width + 2 * border_thickness, message_box.height + 2 * border_thickness))
                pygame.draw.rect(screen, message_box_color, message_box)
                text_surface = font.render(dialogue2[current_dialogue_index2], True, message_text_color)
                screen.blit(text_surface, (message_box.x + 10, message_box.y + 10))
            else:
                show_message = False 
                door_open = True  

        # Open the door if all enemies are defeated
        if door_open:
            pygame.draw.rect(screen, white, door_rect)

        # Check if player enters the door
        if door_open and player_rect.colliderect(door_rect) and not next_game_triggered:
            pygame.display.update()
            pygame.time.delay(300)  # Small delay before quitting
            pygame.quit()
            next_game_triggered = True
            from Mainstage import attack_water  # Transition to the next game
            attack_water()
            break

        # Player health check
        if player_health <= 0:
            running = False
            from game_manager import death_screen
            death_screen(screen)

        # Draw health bar
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = player_health / player_max_health
        current_health_width = health_bar_width * health_ratio
        pygame.draw.rect(screen, red, (10, 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, green, (10, 10, current_health_width, health_bar_height))

        # Update and draw attack animations
        attack_sprites.update()
        attack_sprites.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

