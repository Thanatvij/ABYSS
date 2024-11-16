import pygame

def game_over_screen(screen, victory=True):
    # Set up fonts
    pygame.font.init()
    font = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Choose message based on victory or defeat
    if victory:
        message = "คุณชนะ!"
        instructions = "กด R เพื่อเล่นใหม่ หรือ Q เพื่อออก"
    else:
        message = "เกมจบ!"
        instructions = "กด R เพื่อเล่นใหม่ หรือ Q เพื่อออก"

    # Render the text
    message_surface = font.render(message, True, white)
    instructions_surface = font_small.render(instructions, True, white)

    # Game loop for game over screen
    running = True
    while running:
        screen.fill(black)
        screen.blit(message_surface, (screen.get_width() // 2 - message_surface.get_width() // 2, screen.get_height() // 2 - 50))
        screen.blit(instructions_surface, (screen.get_width() // 2 - instructions_surface.get_width() // 2, screen.get_height() // 2 + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    running = False  # Exit to main loop
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    exit()

        pygame.display.flip()

def start_boss():
    # (Your existing boss battle code here)
    
    # Check if boss is defeated
    if boss.health <= 0:
        game_over_screen(screen, victory=True)  # Call game over screen on victory

# Ensure to call start_boss() within your main loop to initiate the game
