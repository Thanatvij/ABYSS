import pygame, sys
from button import Button

#font@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def get_thai_font(size):
    return pygame.font.Font("assets/Kart-Thai-Khon-Demo.ttf", size)
def get_font(size):  
    return pygame.font.Font("assets/Mantinia Regular.otf", size)
#sound sfx@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
pygame.mixer.music.load("assets/Frog Laughing - Sound Effect.mp3")
pygame.mixer.music.play()
#death screen@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def death_screen(screen):
    while True:
        screen.fill("Black")

        font = get_thai_font(size=95)
        DEATH_TEXT = font.render("ไปเกิดใหม่ไป", True, "Red")
        DEATH_RECT = DEATH_TEXT.get_rect(center=(640, 200))
        screen.blit(DEATH_TEXT, DEATH_RECT)

        RESTART_BUTTON = Button(image=None, pos=(640, 400), text_input="RESTART", 
                                font=get_font(size=50), base_color="white", hovering_color="green")
        QUIT_BUTTON = Button(image=None, pos=(640, 500), text_input="QUIT", 
                             font=get_font(size=50), base_color="white", hovering_color="red")
        BACK_BUTTON = Button(image=None, pos=(640, 600), text_input="BACK TO MENU", 
                             font=get_font(size=50), base_color="white", hovering_color="red")

        for button in [RESTART_BUTTON, QUIT_BUTTON, BACK_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESTART_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    from tutorial import start_tutorial
                    start_tutorial()  # Restart the game
                if QUIT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
                if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    from menu import main_menu
                    main_menu()
                     
        pygame.display.update()
pygame.display.update()