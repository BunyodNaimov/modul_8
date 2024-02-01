import pygame
import pygame_menu

pygame.init()


class Button:
    def __init__(self, x, y, width, height, b_text, b_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.b_text = b_text
        self.b_color = b_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.b_color, self.rect)
        font = pygame.font.SysFont(None, 36)
        button_text = font.render(self.b_text, True, (0, 0, 0))
        screen.blit(button_text, (
            self.rect.centerx - button_text.get_width() / 2,
            self.rect.centery - button_text.get_height() / 2
        ))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print(f"Button {self.b_text} clicked!")


screen = pygame.display.set_mode((600, 600))

menu = pygame_menu.Menu("Welcome", 300, 300, theme=pygame_menu.themes.THEME_BLUE)
menu.add.text_input("Name: ", default="John Doe")
menu.add.button("Button 1", lambda: print("Button bosildi!"))
menu.add.button("Quit", pygame_menu.events.EXIT)

button = Button(
    100, 100, 200, 50, "Click Me!", "green"
)

button1 = Button(
    100, 200, 200, 50, "Click Me!", "red"
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        button.handle_event(event)
        button1.handle_event(event)
    screen.fill((0, 0, 0))
    button.draw(screen)
    menu.draw(screen)
    button1.draw(screen)
    pygame.display.update()
