from ABYSS import start_game  
import pygame, sys
from button import Button   

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/background.png")
pygame.mixer.music.load("assets/ELDEN RING Menu Theme.mp3")
pygame.mixer.music.play(loops=-1)

def get_font(size):  
    return pygame.font.Font("assets/Mantinia Regular.otf", size)

def get_thai_font(size):
    return pygame.font.Font("assets/Kart Nuea Duang DEMO.ttf", size)

def create_button(image, pos, text_input, font, base_color, hovering_color):
    button = Button(image=image, pos=pos, 
                    text_input=text_input, font=font, 
                    base_color=base_color, hovering_color=hovering_color)
    return button

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = create_button(image=pygame.image.load("assets/Play Rect.png"), 
                                    pos=(640, 300), text_input="PLAY", 
                                    font=get_font(75), base_color="white", hovering_color="#B80F0A")
        OPTIONS_BUTTON = create_button(image=pygame.image.load("assets/Options Rect.png"), 
                                       pos=(640, 450), text_input="OPTIONS", 
                                       font=get_font(75), base_color="white", hovering_color="#B80F0A")
        QUIT_BUTTON = create_button(image=pygame.image.load("assets/Quit Rect.png"), 
                                    pos=(640, 600), text_input="QUIT", 
                                    font=get_font(75), base_color="white", hovering_color="#B80F0A")
        

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.music.stop()
                    start_game()  
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("Black")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 70))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = create_button(image=None, pos=(640, 460), 
                                     text_input="BACK", font=get_font(75), base_color="White", hovering_color="Red")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

def death_screen():
    while True:
        SCREEN.fill("Black")

        font = get_font(0, 75)
        DEATH_TEXT = font.render("lol u dead ash", True, "Red")
        DEATH_RECT = DEATH_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(DEATH_TEXT, DEATH_RECT)

        RESTART_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), 
                                pos=(640, 400), text_input="RESTART", 
                                font=pygame.font.Font("assets/Mantinia Regular.otf", 75), 
                                base_color="white", hovering_color="#B80F0A")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), 
                             pos=(640, 550), text_input="QUIT", 
                             font=pygame.font.Font("assets/Mantinia Regular.otf", 75), 
                             base_color="white", hovering_color="#B80F0A")

        for button in [RESTART_BUTTON, QUIT_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESTART_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    start_game()  # Restart the game
                if QUIT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

pygame.display.update()
main_menu()
