import pygame
from tutorial2 import start_game2
from tutorial3 import start_game3

def start_tutorial():
    pygame.init()
    pygame.display.set_caption("Abyss")

    clock = pygame.time.Clock()
    FPS = 60
    speed = 5

    screen_w = 1280        
    screen_h = 720
    screen = pygame.display.set_mode((screen_w, screen_h))
    background = pygame.image.load("assets/wallpaper.png")
    background = pygame.transform.scale(background, (1280, 720))

    # Colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (124, 252, 0)

    # Fonts
    def get_thai_font(size):
        return pygame.font.Font("assets/Kart-Thai-Khon-Demo.ttf", size)
    font = get_thai_font(size=50)
    interaction_font = get_thai_font(size=30)
    interaction_text_color = white
    text_alpha = 255    #For text animation
    fade_direction = -5

    # Character setup
    player_image = pygame.image.load("assets/Mainchar.webp")
    player_image = pygame.transform.scale(player_image, (35, 35))
    player_rect = player_image.get_rect(center=(640, 360))

    # NPC setup
    npc_image = pygame.image.load("assets/Wizard.png")
    npc_image = pygame.transform.scale(npc_image, (100, 100))
    npc_rect = npc_image.get_rect(center=(640, 300))  

    # Dialogue setup
    dialogue = [
        "ว่าไงคนแปลกหน้า",
        "ที่นี่คือ Abyss นะโบร๋ว",
        "มาเล่นเกมนี้ได้แสดงว่าว่างใช่ไหมละ!!",
        "ถ้างั้นมาฆ่าสัตว์ประหลาดให้หน่อยดิ แต้งกิ้ว!!",
        "พลังอยู่ข้างหลังเรา ไปเลือกที่ชอบนะจ้ะ"
    ]
    current_dialogue_index = 0
    show_message = False  

    # Message box setup
    message_box = pygame.Rect(100, 550, 1080, 150)
    message_box_color = black
    message_text_color = white
    border_color = white  # Color of the border
    border_thickness = 4  # Thickness of the border

    # Power options
    power_images = [
        pygame.image.load("assets/fire.png"),
        pygame.image.load("assets/water.png"),
    ]
    power_images = [pygame.transform.scale(img, (60, 60)) for img in power_images]
    selected_power_index = 0  
    show_powers = False  
    chosen_power = None  # Track the selected power

    door_width = 85
    door_height = 190
    door_rect = pygame.Rect((screen_w - door_width) // 2, 50, door_width, door_height) 
    door_image = pygame.image.load("assets/Door.png").convert_alpha()
    door_image = pygame.transform.scale(door_image, (door_width, door_height))
    door_open = False
    

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and player_rect.colliderect(npc_rect):
                    show_message = True
                    current_dialogue_index = 0  
                    show_powers = False  
                elif event.key == pygame.K_RETURN and show_message:
                    current_dialogue_index += 1
                    if current_dialogue_index >= len(dialogue):
                        show_message = False  
                        show_powers = True  
                elif event.key == pygame.K_SPACE:
                    show_message = False
                    show_powers = False

                # Power selection
                elif show_powers:
                    if event.key == pygame.K_LEFT:
                        selected_power_index = (selected_power_index - 1) % len(power_images)
                    elif event.key == pygame.K_RIGHT:
                        selected_power_index = (selected_power_index + 1) % len(power_images)
                    elif event.key == pygame.K_RETURN:
                        chosen_power = "fire" if selected_power_index == 0 else "water"  
                        show_powers = False  
                        door_open = True  

        # Movement controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player_rect.top > 0:
            player_rect.y -= speed
        if keys[pygame.K_s] and player_rect.bottom < screen_h:
            player_rect.y += speed
        if keys[pygame.K_a] and player_rect.left > 0:
            player_rect.x -= speed
        if keys[pygame.K_d] and player_rect.right < screen_w:
            player_rect.x += speed

        proximity_threshold = 100
        is_near_npc = player_rect.colliderect(npc_rect.inflate(proximity_threshold, proximity_threshold))

        # Draw elements
        screen.blit(background, (0, 0))
        screen.blit(player_image, player_rect)
        screen.blit(npc_image, npc_rect)

        #Display text when close to the npc
        if is_near_npc and not show_message:
            interaction_text_surface = interaction_font.render("Press 'E' to talk", True, interaction_text_color)
            interaction_text_rect = interaction_text_surface.get_rect(center=(npc_rect.centerx, npc_rect.top - 10))
            screen.blit(interaction_text_surface, interaction_text_rect)

        if show_message and current_dialogue_index < len(dialogue):
            # Draw the border around the message box
            pygame.draw.rect(screen, border_color, 
                             (message_box.x - border_thickness, message_box.y - border_thickness, 
                              message_box.width + 2 * border_thickness, message_box.height + 2 * border_thickness))
            
            # Draw the inner message box
            pygame.draw.rect(screen, message_box_color, message_box)

            # Render the text and display it
            text_surface = font.render(dialogue[current_dialogue_index], True, message_text_color)
            screen.blit(text_surface, (message_box.x + 10, message_box.y + 10))

            text_alpha += fade_direction
            if text_alpha <= 50 or text_alpha >= 255:  # Reverse direction at min/max alpha
                fade_direction *= -1
                text_alpha = max(50, min(255, text_alpha))

            instruction_font = get_thai_font(size=30)  # Smaller font for instructions
            instruction_surface = instruction_font.render("Enter to continue", True, message_text_color)
            instruction_surface.set_alpha(text_alpha)
            
            margin_x =20    #จัดให้ไม่เลยขอบ
            margin_y =15
            instruction_rect = instruction_surface.get_rect(
                bottomright=(message_box.right - margin_x, message_box.bottom - margin_y)
            )
            screen.blit(instruction_surface, instruction_rect)

        # Power selection display
        if show_powers:
            power_y = npc_rect.y - 100  
            total_width = len(power_images) * 60 + (len(power_images) - 1) * 10 
            start_x = (screen_w - total_width) // 2  
            
            for i, power_img in enumerate(power_images):
                power_x = start_x + i * (60 + 10)
                if i == selected_power_index:
                    pygame.draw.rect(screen, (255, 215, 0), (power_x - 5, power_y - 5, 70, 70), 3) 
                screen.blit(power_img, (power_x, power_y))

        if door_open:
            screen.blit(door_image, door_rect)

        # Door interaction to start the chosen game
        if door_open and player_rect.colliderect(door_rect) :
            pygame.time.delay(500)  
            if chosen_power == "fire":
                start_game2()
            elif chosen_power == "water":
                
                start_game3()
                break


        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()