# Import libraries
import pygame
import random
import math
def attack_fire():
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("Abyss")

    # Constants
    fire_speed = 10
    fire_size = 20
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
    red_pink = (255, 32, 111)
    black = (0, 0, 0)
    yellow_fire = (255, 201, 31)
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)

    # Load character and enemy images
    img = pygame.image.load("assets/Mainchar.webp").convert_alpha()
    img = pygame.transform.scale(img, (35, 35))
    img_rect = img.get_rect(center=screen_rect.center)

    enemy_img = pygame.image.load("assets/Enemy.png").convert_alpha()

    # Music
    pygame.mixer.music.load("assets/weird.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

    # Game variables
    player_exp = 0
    exp_needed = 100
    skill_points = 0
    max_hp = 100
    hp = 100
    player_kill_count = 0

    # EXP bar
    exp_bar_width = 1270
    exp_bar_height = 10
    exp_bar_x = 10
    exp_bar_y = 680

    # Health bar
    hp_w = 35
    hp_h = 4

    # Enemy and fire lists
    enemies = []
    exp_items = []
    fires = []
    fires_spawn_timer = 0
    fires_spawn_delay = 10
    spawn=True

    # Skill upgrade message variables
    level_up_message = ""
    level_up_message_duration = 100
    level_up_message_timer = 0

    # Door
    door_rect = pygame.Rect(screen_w // 2-24, (screen_h // 2) - 50, 50, 100)
    door_open = False

    # Functions
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
        else:
            x = screen_w + 50
            y = random.randint(0, screen_h)

        enemy_rect = pygame.Rect(x, y, 40, 40)
        enemy_health = 1  # ตั้งพลังชีวิตของมอนสเตอร์ที่ 1
        enemies.append({"rect": enemy_rect, "health": enemy_health})

    def spawn_exp(x, y):
        exp_rect = pygame.Rect(x, y, 10, 10)
        exp_items.append(exp_rect)

    def upgrade_projectile_size():
        nonlocal fire_size  # เพิ่ม global เพื่อให้เข้าถึงตัวแปร fire_size
        fire_size += 1


    def upgrade_projectile_speed():
        nonlocal fire_speed
        fire_speed += 1

   
    # Main game loop
    running = True
    while running:
        screen.fill(black)
        screen.blit(img, img_rect)

        # Level-up message
        if level_up_message:
            text = font.render(level_up_message, True, yellow_fire)
            screen.blit(text, (screen_w // 2 - text.get_width() // 2, 50))
            level_up_message_timer -= 1
            if level_up_message_timer <= 0:
                level_up_message = ""

        # EXP handling
        for exp_rect in exp_items:
            pygame.draw.rect(screen, green, exp_rect)
            if img_rect.colliderect(exp_rect):
                player_exp += 10
                exp_items.remove(exp_rect)
                if player_exp >= exp_needed:
                    player_exp -= exp_needed
                    skill_points += 1
                    level_up_message = "Level Up! / Press 2 for size / Press 3 for speed /"
                    level_up_message_timer = level_up_message_duration

        # Spawn enemies randomly
        if spawn and random.randint(0, 100) < 4:
            spawn_enemy()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and skill_points > 0:
                if event.key == pygame.K_2:
                    upgrade_projectile_size()
                    skill_points -= 1
                elif event.key == pygame.K_3:
                    upgrade_projectile_speed()
                    skill_points -= 1

        # Movement keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and img_rect.top >= 0:
            img_rect.y -= speed
        if keys[pygame.K_s] and img_rect.bottom <= screen_h:
            img_rect.y += speed
        if keys[pygame.K_a] and img_rect.left >= 0:
            img_rect.x -= speed
        if keys[pygame.K_d] and img_rect.right <= screen_w:
            img_rect.x += speed

        # Projectile creation
        fires_spawn_timer += 1
        if fires_spawn_timer >= fires_spawn_delay:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx, dy = mouse_x - img_rect.centerx, mouse_y - img_rect.centery
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx, dy = dx / distance, dy / distance
                fires.append({"pos": [img_rect.centerx, img_rect.centery], "dir": [dx, dy]})
            fires_spawn_timer = 0

        # Projectile movement and enemy collision
        for fire in fires[:]:
            fire["pos"][0] += fire["dir"][0] * fire_speed
            fire["pos"][1] += fire["dir"][1] * fire_speed
            fire_rect = pygame.Rect(fire["pos"][0], fire["pos"][1], fire_size, fire_size)
            for enemy in enemies[:]:
                if fire_rect.colliderect(enemy["rect"]):
                    enemy["health"] -= 1  # ลดพลังชีวิตของมอนสเตอร์ทีละ 1
                    fires.remove(fire)
                    if enemy["health"] <= 0:
                        spawn_exp(enemy["rect"].centerx, enemy["rect"].centery)
                        enemies.remove(enemy)
                        player_kill_count+=1
                    break

        # Door open after kills
        # After the kill count condition
        if player_kill_count >= 20:
            door_open = True  # Ensure this is set correctly
            spawn=False
            
        # Handle door collision
        if door_open:
            pygame.draw.rect(screen, white, door_rect)
            if img_rect.colliderect(door_rect):
                import bossfire  # Ensure this import is correct and intended
                
                running = False  # Exit the game loop
                
            

        # Enemy movement and collision with player
        for enemy in enemies:
            dx, dy = img_rect.centerx - enemy["rect"].centerx, img_rect.centery - enemy["rect"].centery
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx, dy = dx / distance, dy / distance
                enemy["rect"].x += dx * enemy_speed
                enemy["rect"].y += dy * enemy_speed
            screen.blit(enemy_img, enemy["rect"])
            if enemy["rect"].colliderect(img_rect):
                hp -= 1

        # HP bar
        current_health_width = hp_w * (hp / max_hp)
        hp_x = img_rect.centerx - hp_w // 2
        hp_y = img_rect.top - hp_h - 5
        pygame.draw.rect(screen, red, (hp_x, hp_y, hp_w, hp_h))
        pygame.draw.rect(screen, green, (hp_x, hp_y, current_health_width, hp_h))

        # End game if HP is zero
        if hp <= 0:
            running = False
            from game_manager import death_screen
            death_screen(screen)  # Call death screen

        # Draw projectiles
        for fire in fires:
            pygame.draw.circle(screen, red_pink, (int(fire["pos"][0]), int(fire["pos"][1])), fire_size)

        # Draw EXP bar
        current_exp_width = (player_exp / exp_needed) * exp_bar_width
        pygame.draw.rect(screen, yellow_fire, (exp_bar_x, exp_bar_y, current_exp_width, exp_bar_height))

        # Skill points display
        skill_points_text = font.render(f"Skill Points: {skill_points}", True, white)
        screen.blit(skill_points_text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
