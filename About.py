import pygame
import sys

# Initialize pygame
pygame.init()

def get_font(size):
    return pygame.font.Font("jaro/Jaro-Regular-VariableFont_opsz.ttf", size)

def About():
    WIDTH, HEIGHT = 1125, 750
    TEXT_COLOR = (255, 255, 255)  # White text color
    FONT_SIZE = 18
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("About")

    BG = pygame.image.load("bgfinal.png")  # Load the background image

    text_content = [
        "Electrostatics Python Application",
        "",
        "This project introduces a Python-based application focused on electrostatics,",
        "a fundamental concept in electromagnetics dealing with interactions between",
        "stationary electric charges. The application calculates and simulates various",
        "electrostatic scenarios, offering users visualization tools to understand",
        "electric forces, distances, and field patterns. Key features include computing",
        "electric force and field lines, alongside a built-in calculator for specific",
        "electrostatic problems. The project emphasizes accuracy through detailed",
        "explanations of computational methods and validation against established",
        "solutions. The interactive nature of the application encourages hands-on",
        "learning for students and educators. Future enhancements could include support",
        "for more complex charge configurations and expanded simulation capabilities,",
        "enhancing its educational value."
    ]

    font = get_font(FONT_SIZE)
    rendered_text = [font.render(line, True, TEXT_COLOR) for line in text_content]

    text_height = sum(text.get_height() for text in rendered_text)
    start_y = (HEIGHT - text_height) // 2

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

    BACK_BUTTON = Button(image=None, pos=(WIDTH // 2, HEIGHT - 50),
                         text_input="BACK", font=get_font(30), base_color="Gold", hovering_color="Green")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    return  # Exit the About screen and return to the main menu

        SCREEN.blit(BG, (0, 0))  # Blit the background image

        y_offset = start_y
        for text in rendered_text:
            x = 50  # Adjusted to place text on the left side of the screen
            SCREEN.blit(text, (x, y_offset))
            y_offset += text.get_height() + 4

        BACK_BUTTON.changeColor(pygame.mouse.get_pos())
        BACK_BUTTON.update(SCREEN)

        pygame.display.flip()

if __name__ == "__main__":
    About()
