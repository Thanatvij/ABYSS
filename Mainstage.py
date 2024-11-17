# เริ่มต้น pygame และกำหนดค่าคงที่ต่างๆ
import pygame
import random
import math
import enemy

# function
def attack_water():
    def spawn_enemy():
        side = random.choice(["top", "bottom", "left", "right"])
        
        if side == "top":
            x = random.randint(0, screen_w)
            y = -50
        elif side == "bottom":
            x = random.randint(0, screen_w)
            y = screen_h + 50
        elif side == "left":
            x = -50
            y = random.randint(0, screen_h)
        else:  # "right"
            x = screen_w + 50
            y = random.randint(0, screen_h)
        
        enemy_rect = pygame.Rect((x, y), (40, 40))  # กำหนดขนาด enemy ให้ถูกต้อง
        enemies.append(enemy_rect)

    def spawn_exp(x, y):
        exp_rect = pygame.Rect(x, y, 10, 10)  # exp item size
        exp_items.append(exp_rect)
    # Skill upgrade functions
    def upgrade_projectile_size():
        nonlocal water_size
        water_size += 10  # เพิ่มขนาด projectile

    def upgrade_projectile_speed():
        nonlocal water_speed
        water_speed += 1  # เพิ่มความเร็ว projectile
    #start
    pygame.init()
    pygame.display.set_caption("Abyss")

    # Constants
    water_speed = 7
    water_size = 150  # ขนาดของ projectile เริ่มต้น
    speed = 5
    FPS = 60
    clock = pygame.time.Clock()
    screen_w = 1280
    screen_h = 720
    screen = pygame.display.set_mode((screen_w, screen_h))
    screen_rect = screen.get_rect()
    enemy_speed = 3
    font = pygame.font.Font(None, 36)

    # Colors
    red_pink = (255, 32, 111, 255)
    black = (0, 0, 0)
    blue_boy = (78, 237, 238, 255)
    yellow_fire = (255, 201, 31, 255)
    hell_frame = (255, 201, 31, 255)
    white = (255, 255, 255)
    WHITE = (255, 255, 255)
    green = (0, 255, 0)

    # Music
    pygame.mixer.music.load("assets/weird.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1)

    # Character setup
    img = pygame.image.load("assets/Mainchar.webp").convert_alpha()
    img = pygame.transform.scale(img, (35, 35))
    img_rect = img.get_rect()
    img_rect.center = screen_rect.center
    player_exp = 0
    exp_needed = 100
    skill_points = 0
    max_hp = 100
    hp=100
    player_kill_count = 0

    # EXP bar size and position
    exp_bar_width = 1270
    exp_bar_height = 10
    exp_bar_x = 10
    exp_bar_y = 680

    #Health bar
    hp_w=35
    hp_h=4

    # Enemy setup
    enemy_img = pygame.image.load("assets/Enemy.png").convert_alpha()

    # Game variables
    enemies = []
    exp_items = []
    waters = []
    waters_spawn_timer = 0
    waters_spawn_delay = 100  # ตัวแปรควบคุมความถี่การ spawn projectile

    # Skill upgrade message variables
    level_up_message = ""
    level_up_message_duration = 100
    level_up_message_timer = 0

    #Font
    def get_thai_font(size):
        return pygame.font.Font("assets/Kart-Thai-Khon-Demo.ttf", size)
    font = get_thai_font(size=30)

    messages = ["ถ้านายผ่านประตูนั้นไปค่า status ของนายจะถูกรีเซททั้งหมด", "ถ้านายผ่านประตูนั้นไปค่า status ของนายจะถูกรีเซททั้งหมด"]
    current_messages_index = 0
    start_time = pygame.time.get_ticks()
    display_duration = 6000

    #Door
    door_width = 85
    door_height = 190
    door_rect = pygame.Rect((screen_w - door_width) // 2, 50, door_width, door_height) 
    door_image = pygame.image.load("assets/Door.png").convert_alpha()
    door_image = pygame.transform.scale(door_image, (door_width, door_height))
    door_open = False

    #swich
    spawn=True

    # Main game loop
    running = True
    while running:
        screen.fill(black)
        screen.blit(img, img_rect)

        # แสดงข้อความเลเวลอัปเมื่อผู้เล่นมีแต้มสกิล
        if level_up_message:
            text = font.render(level_up_message, True, yellow_fire)
            screen.blit(text, (screen_w // 2 - text.get_width() // 2, 50))
            level_up_message_timer -= 1
            if level_up_message_timer <= 0:
                level_up_message = ""

        # จัดการกับ EXP ที่เก็บได้และเลเวลอัป
        for exp_rect in exp_items:
            pygame.draw.rect(screen, green, (exp_rect.x, exp_rect.y, 10, 10))
            if img_rect.colliderect(exp_rect):
                player_exp += 10
                exp_items.remove(exp_rect)

                if player_exp >= exp_needed:
                    player_exp -= exp_needed
                    skill_points += 1
                    level_up_message = "Level Up! / Press 2 for size / Press 3 for speed /"
                    level_up_message_timer = level_up_message_duration

        if spawn and random.randint(0, 100) < 4:
            spawn_enemy()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and skill_points > 0:
                if event.key == pygame.K_1:
                    pass
                elif event.key == pygame.K_2:
                    upgrade_projectile_size()
                    skill_points -= 1
                elif event.key == pygame.K_3:
                    upgrade_projectile_speed()
                    skill_points -= 1

        # Movement keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and img_rect.top>=0:
            img_rect.y -= speed
        if keys[pygame.K_s] and img_rect.bottom<=screen_h:
            img_rect.y += speed
        if keys[pygame.K_a] and img_rect.left>=0:
            img_rect.x -= speed
        if keys[pygame.K_d] and img_rect.right<=screen_w:
            img_rect.x += speed

        # Water skill projectiles
        waters_spawn_timer += 1
        if waters_spawn_timer >= waters_spawn_delay:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx, dy = mouse_x - img_rect.centerx, mouse_y - img_rect.centery
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx, dy = dx / distance, dy / distance
                waters.append({
                    "pos": [img_rect.centerx, img_rect.centery],
                    "dir": [dx, dy]
                })
            waters_spawn_timer = 0

        for water in waters[:]:
            
            
            water["pos"][0] += water["dir"][0] * water_speed
            water["pos"][1] += water["dir"][1] * water_speed
            
            water_rect = pygame.Rect(water["pos"][0], water["pos"][1], water_size, water_size)
            for enemy_rect in enemies[:]:
                if water_rect.colliderect(enemy_rect):
                    spawn_exp(enemy_rect.centerx, enemy_rect.centery)
                    enemies.remove(enemy_rect)
                    player_kill_count+=1
                    break
        
        # After the kill count condition
        if player_kill_count >= 20:
            door_open = True  # Ensure this is set correctly
            spawn=False

        if door_open:
            screen.blit(door_image, door_rect)
            elapsed_time = pygame.time.get_ticks() - start_time
            # Handle message timing
            if elapsed_time > display_duration:
                current_messages_index += 1  # Move to the next message
                start_time = pygame.time.get_ticks()
            # Display messages
            if current_messages_index < len(messages):
                # Render and display the current message
                text_surface = font.render(messages[current_messages_index], True, WHITE)
                text_rect = text_surface.get_rect(center=(screen_w // 2, 50))
                screen.blit(text_surface, text_rect)
            else:
                fallback_message = "เพราะฉะนั้นเตรียมตัวไว้ด้วยล่ะ!!!"
                text_surface = font.render(fallback_message, True, WHITE)
                text_rect = text_surface.get_rect(center=(screen_w // 2, 50))
                screen.blit(text_surface, text_rect)
                
            if img_rect.colliderect(door_rect):
                from bosswater import start_boss  # Ensure this import is correct and intended
                start_boss()
                running = False  # Exit the game loop
            
            
        for enemy_rect in enemies:
            dx, dy = img_rect.centerx - enemy_rect.centerx, img_rect.centery - enemy_rect.centery
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx, dy = dx / distance, dy / distance
                enemy_rect.x += dx * enemy_speed
                enemy_rect.y += dy * enemy_speed

            screen.blit(enemy_img, enemy_rect)
            if enemy_rect.colliderect(img_rect):
                hp-=1

        ratio_hp = hp / max_hp
        current_health_width= hp_w*ratio_hp
        hp_x = img_rect.centerx - hp_w // 2
        hp_y = img_rect.top - hp_h - 5 
        
        #hp_bar
        pygame.draw.rect(screen, (255, 0, 0), (hp_x, hp_y, hp_w, hp_h))  
        pygame.draw.rect(screen, (0, 255, 0), (hp_x, hp_y, current_health_width, hp_h))  
        
        if hp   <= 0:
            running = False
            from game_manager import death_screen
            death_screen(screen)  # Call death screen
                
        # Draw projectiles
        for water in waters:
            pygame.draw.rect(screen, blue_boy, (*water["pos"], water_size, water_size))

        # Draw EXP bar
        current_exp_width = (player_exp / exp_needed) * exp_bar_width
        pygame.draw.rect(screen, yellow_fire, (exp_bar_x, exp_bar_y, current_exp_width, exp_bar_height))
        
        # แสดงจำนวน skill points ที่มุมบนซ้ายของหน้าจอ
        skill_points_text = font.render(f"Skill Points: {skill_points}", True, white)
        screen.blit(skill_points_text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)

pygame.quit()