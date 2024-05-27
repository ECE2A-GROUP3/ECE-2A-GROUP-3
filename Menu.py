import pygame
import sys
from FINAL_SIMULATOR import run_simulation  # Import the run_simulation function from your simulator file
from final_calc_emags import ElectricForceCalculator
from About import About  # Import the About function

pygame.init()  # Initialize Pygame

SCREEN = pygame.display.set_mode((1125, 750))
pygame.display.set_caption("Menu")

BG = pygame.image.load("bgfinal.png")

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("jaro/Jaro-Regular-VariableFont_opsz.ttf", size)

def Calc():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def Sim():
    run_simulation()  # Call the simulation function directly

def open_calculator():
    calculator = ElectricForceCalculator()
    calculator.mainloop()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("ELECTROSTATICS ", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 50))

        CALCULATOR_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(180, 200),
                             text_input="ELECROSTATICS CALCULATOR", font=get_font(25), base_color="#ffffff", hovering_color="#b68f40")
        SIMULATOR_BUTTON = Button(image=pygame.image.load("Options Rect.png"), pos=(190, 350),
                                text_input="ELECROSTATICS SIMULATOR", font=get_font(25), base_color="#FFFFFF", hovering_color="#b68f40")
        ABOUTUS_BUTTON = Button(image=pygame.image.load("Options Rect.png"), pos=(230, 500),
                                  text_input="ABOUT", font=get_font(25), base_color="#FFFFFF",
                                  hovering_color="#b68f40")

        QUIT_BUTTON = Button(image=pygame.image.load("Options Rect.png"), pos=(290, 650),
                             text_input="QUIT", font=get_font(25), base_color="#FFFFFF", hovering_color="#b68f40")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [CALCULATOR_BUTTON, SIMULATOR_BUTTON, ABOUTUS_BUTTON,  QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CALCULATOR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    open_calculator()
                elif SIMULATOR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Sim()
                elif ABOUTUS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    About()
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    main_menu()
