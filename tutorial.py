import pygame
from itertools import cycle
import math
from pixel_dimension import start_boss

class AttackAnimation(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, power_type="fire"):
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
        self.power_type = power_type  

        # Calculate direction to target
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

def start_tutorial():
    pygame.init()
    pygame.display.set_caption("Abyss")

    clock = pygame.time.Clock()
    FPS = 60
    speed = 5
    player_max_health = 100  
    player_health = player_max_health

    screen_w = 1280        
    screen_h = 720
    screen = pygame.display.set_mode((screen_w, screen_h))
    background = pygame.image.load("assets/wallpaper.png")
    background = pygame.transform.scale(background, (1280, 720))

    black = (0, 0, 0)
    white = (255, 255, 255)

    def get_thai_font(size):
        return pygame.font.Font("assets/Kart-Thai-Khon-Demo.ttf", size)
    font = get_thai_font(size=50)

    player_image = pygame.image.load("assets/Mainchar.webp")
    player_image = pygame.transform.scale(player_image, (35, 35))
    player_rect = player_image.get_rect(center=(640, 360))

    npc_image = pygame.Surface((50, 50)) 
    npc_image.fill((255, 0, 0))
    npc_rect = npc_image.get_rect(center=(640, 300))  

    message_box = pygame.Rect(100, 550, 1080, 150)
    message_box_color = black
    message_text_color = white
    dialogue = [
        "ว่าไงคนแปลกหน้า",
        "ที่นี่คือ Abyss นะโบร๋ว",
        "มาเล่นเกมนี้ได้แสดงว่าว่างใช่ไหมละ!!",
        "ถ้างั้นมาฆ่าสัตว์ประหลาดให้หน่อยดิ แต้งกิ้ว!!",
        "เลือกพลังที่ด้านหลังของชั้นเลย"
    ]
    current_dialogue_index = 0
    show_message = False  

    power_images = [
        pygame.image.load("assets/fire.png"),
        pygame.image.load("assets/water.png"),
    ]
    power_images = [pygame.transform.scale(img, (60, 60)) for img in power_images]
    selected_power_index = 0  
    show_powers = False  

    door_rect = pygame.Rect(600, 100, 60, 80)  
    door_open = False
    next_game_triggered = False
    power_selected = False  

    # Main game loop
    running = True
    attack_sprites = pygame.sprite.Group()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Press E to interact with NPC
                if event.key == pygame.K_e and player_rect.colliderect(npc_rect):
                    show_message = True
                    current_dialogue_index = 0  
                    show_powers = False  # Reset power selection visibility
                # Advance through the dialogue
                elif event.key == pygame.K_RETURN and show_message:
                    current_dialogue_index += 1
                    if current_dialogue_index >= len(dialogue):
                        show_message = False  
                        show_powers = True  # Show power options after dialogue ends
                # Hide message box with spacebar
                elif event.key == pygame.K_SPACE:
                    show_message = False
                    show_powers = False

                # Power selection controls
                if show_powers:
                    if event.key == pygame.K_LEFT:
                        selected_power_index = (selected_power_index - 1) % len(power_images)
                    elif event.key == pygame.K_RIGHT:
                        selected_power_index = (selected_power_index + 1) % len(power_images)
                    elif event.key == pygame.K_RETURN:
                        chosen_power = power_images[selected_power_index]
                        power_selected = True  
                        print(f"Chosen Power: {chosen_power}")
                        show_powers = False  # Hide power options after selection

        # Set door to open once a power is selected
        if power_selected:
            door_open = True

        # Player movement logic (independent of other game states)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player_rect.top > 0:
            player_rect.y -= speed
        if keys[pygame.K_s] and player_rect.bottom < screen_h:
            player_rect.y += speed
        if keys[pygame.K_a] and player_rect.left > 0:
            player_rect.x -= speed
        if keys[pygame.K_d] and player_rect.right < screen_w:
            player_rect.x += speed

        # Draw background, player, and NPC
        screen.blit(background, (0, 0))
        screen.blit(player_image, player_rect)
        screen.blit(npc_image, npc_rect)

        # Draw message box and current line of dialogue if show_message is True
        if show_message and current_dialogue_index < len(dialogue):
            pygame.draw.rect(screen, message_box_color, message_box)
            pygame.draw.rect(screen, white, message_box, 2)
            text_surface = font.render(dialogue[current_dialogue_index], True, message_text_color)
            screen.blit(text_surface, (message_box.x + 10, message_box.y + 10))

        # Draw power selection options if show_powers is True
        if show_powers:
            power_y = npc_rect.y - 100  # Positioning above NPC
            total_width = len(power_images) * 60 + (len(power_images) - 1) * 10
            start_x = (screen_w - total_width) // 2

            for i, power_img in enumerate(power_images):
                power_x = start_x + i * (60 + 10)
                # Highlight the selected power with a border
                if i == selected_power_index:
                    pygame.draw.rect(screen, (255, 215, 0), (power_x - 5, power_y - 5, 70, 70), 3) 
                screen.blit(power_img, (power_x, power_y))

        # Draw door if it is open
        if door_open:
            pygame.draw.rect(screen, white, door_rect)

        # Transition to the boss if player reaches the door
        if door_open and player_rect.colliderect(door_rect) and not next_game_triggered:
            pygame.display.update()
            pygame.time.delay(500)
            
            pygame.quit()
            next_game_triggered = True  
            start_boss()
            break

        pygame.display.update()
        clock.tick(FPS)
start_tutorial()
