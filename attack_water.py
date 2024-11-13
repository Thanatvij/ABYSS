# เริ่มต้น pygame และกำหนดค่าคงที่ต่างๆ
import pygame
import random
import math
import enemy

# function 
def start_water():
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
        global water_size
        water_size += 10  # เพิ่มขนาด projectile

    def upgrade_projectile_speed():
        global water_speed
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
    green = (0, 255, 0)

    # Music
    pygame.mixer.music.load("assets/weird.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

    # Character setup
    img = pygame.image.load("assets/Mainchar.webp").convert_alpha()
    img = pygame.transform.scale(img, (35, 35))
    img_rect = img.get_rect()
    img_rect.center = screen_rect.center
    player_exp = 0
    exp_needed = 100
    skill_points = 0

    # EXP bar size and position
    exp_bar_width = 1270
    exp_bar_height = 10
    exp_bar_x = 10
    exp_bar_y = 680

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

        if len(enemies) < 50 and random.randint(0, 100) < 4:
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
            '''
            if (water["pos"][0] < 0 or water["pos"][0] > screen_w or
                water["pos"][1] < 0 or water["pos"][1] > screen_h):
                waters.remove(water)
                continue
            '''
            water_rect = pygame.Rect(water["pos"][0], water["pos"][1], water_size, water_size)
            for enemy_rect in enemies[:]:
                if water_rect.colliderect(enemy_rect):
                    spawn_exp(enemy_rect.centerx, enemy_rect.centery)
                    enemies.remove(enemy_rect)
                    break

        for enemy_rect in enemies:
            dx, dy = img_rect.centerx - enemy_rect.centerx, img_rect.centery - enemy_rect.centery
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx, dy = dx / distance, dy / distance
                enemy_rect.x += dx * enemy_speed
                enemy_rect.y += dy * enemy_speed
                
            screen.blit(enemy_img, enemy_rect)

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