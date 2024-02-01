import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("background.png")
background_sound = pygame.mixer.Sound("background.wav")

player = pygame.image.load("player.png")
playerX = 370
playerY = 480

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                playerX += 10
            if event.key == pygame.K_LEFT:
                playerX -= 10
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(player, (playerX, playerY))
    pygame.display.update()
