import pygame

pygame.init()

screen = pygame.display.set_mode((600, 480))
pygame.display.set_caption("First Game")

BG = pygame.image.load("bg.jpg")
standing = pygame.image.load("standing.png")

clock = pygame.time.Clock()

walkRight = [
    pygame.image.load("R1.png"),
    pygame.image.load("R2.png"),
    pygame.image.load("R3.png"),
    pygame.image.load("R4.png"),
    pygame.image.load("R5.png"),
    pygame.image.load("R6.png"),
    pygame.image.load("R7.png"),
    pygame.image.load("R8.png"),
    pygame.image.load("R9.png"),
]
walkLeft = [
    pygame.image.load("L1.png"),
    pygame.image.load("L2.png"),
    pygame.image.load("L3.png"),
    pygame.image.load("L4.png"),
    pygame.image.load("L5.png"),
    pygame.image.load("L6.png"),
    pygame.image.load("L7.png"),
    pygame.image.load("L8.png"),
    pygame.image.load("L9.png"),
]

x = 50
y = 400
width = 64
height = 64
isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0
FPS = 27


def redrawGameWindow():
    global walkCount
    screen.blit(BG, (0, 0))

    if walkCount + 1 >= FPS:
        walkCount = 0

    if left:
        screen.blit(walkLeft[walkCount // 3], (x, y))
        walkCount += 1
    elif right:
        screen.blit(walkRight[walkCount // 3], (x, y))
        walkCount += 1
    else:
        screen.blit(standing, (x, y))
    pygame.display.update()


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        left = True
        right = False
    elif keys[pygame.K_RIGHT]:
        right = True
        left = False
    else:
        right = False
        left = False
        walkCount = 0

    if not isJump:
        if keys[pygame.K_SPACE]:
            isJump = True
            right = False
            left = False
            walkCount = 0
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    redrawGameWindow()
