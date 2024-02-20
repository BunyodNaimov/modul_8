import pygame

pygame.init()

screen = pygame.display.set_mode((500, 480))
pygame.display.set_caption("First Game")

BG = pygame.image.load("bg.jpg")
char = pygame.image.load("standing.png")

clock = pygame.time.Clock()

bullet_sound = pygame.mixer.Sound('bullet.mp3')
hit_sound = pygame.mixer.Sound("hit.mp3")

music = pygame.mixer.Sound("music.mp3")
music.play()

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

FPS = 27


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.speed = 5
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 100
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('None', 100)
        text = font1.render('-5', True, (255, 0, 0))
        screen.blit(text, (250 - (text.get_width() / 2), 200))
        pygame.display.update()

        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    quit()


class Enemy(object):
    walk_right_list = ["R1E.png", "R2E.png", "R3E.png", "R4E.png", "R5E.png",
                       "R6E.png", "R7E.png", "R8E.png", "R9E.png", "R10E.png", "R11E.png"]

    walk_left_list = ["L1E.png", "L2E.png", "L3E.png", "L4E.png", "L5E.png",
                      "L6E.png", "L7E.png", "L8E.png", "L9E.png", "L10E.png", "L11E.png"]

    walkRight = [pygame.image.load(image) for image in walk_right_list]
    walkLeft = [pygame.image.load(image) for image in walk_left_list]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.speed = 5
        self.hitbox = [self.x + 17, self.y + 3, 31, 57]
        self.healt = 10
        self.isvisible = True

    def draw(self, screen):
        self.move()

        if self.isvisible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            if self.speed > 0:
                screen.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                screen.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(screen, (0, 128, 0),
                             (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.healt)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    def move(self):
        if self.speed > 0:
            if self.x + self.speed < self.path[1]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walkCount = 0
        else:
            if self.x - self.speed > self.path[0]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walkCount = 0

    def hit(self):
        if self.healt > 0:
            self.healt -= 1
        else:
            self.isvisible = False


class Bullet(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.speed = 8 * facing

    def draw(self, screen):
        pygame.draw.circle(
            screen, self.color, (self.x, self.y), self.radius
        )


def redrawGameWindow():
    screen.blit(BG, (0, 0))
    player.draw(screen)
    enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.update()


player = Player(200, 410, 64, 64)
enemy = Enemy(10, 410, 64, 64, 470)

score = 0

bullets = []
running = True
while running:
    clock.tick(FPS)

    if enemy.isvisible == True:
        if player.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and \
                player.hitbox[1] + player.hitbox[3] > enemy.hitbox[1]:
            if player.hitbox[0] + player.hitbox[2] > enemy.hitbox[0] and \
                    player.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
                player.hit()
                score += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

    for bullet in bullets:
        if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and \
                bullet.y + bullet.radius > enemy.hitbox[1]:
            if bullet.x + bullet.radius > enemy.hitbox[0] and \
                    bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                hit_sound.play()
                enemy.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 600 and bullet.x > 0:
            bullet.x += bullet.speed
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if player.left:
            facing = -1
        else:
            facing = 1
        print(len(bullets))
        if len(bullets) < 5:
            bullets.append(
                Bullet(round(player.x + player.width // 2),
                       round(player.y + player.height // 2),
                       6, (0, 0, 0), facing)
            )

    if keys[pygame.K_LEFT]:
        player.x -= player.speed
        player.left = True
        player.right = False
        player.standing = False

    elif keys[pygame.K_RIGHT]:
        player.x += player.speed
        player.right = True
        player.left = False
        player.standing = False
    else:
        player.standing = True
        player.walkCount = 0

    if not player.isJump:
        if keys[pygame.K_UP]:
            player.isJump = True
            player.right = False
            player.left = False
            player.walkCount = 0
    else:
        if player.jumpCount >= -10:
            neg = 1
            if player.jumpCount < 0:
                neg = -1
            player.y -= (player.jumpCount ** 2) * 0.5 * neg
            player.jumpCount -= 1
        else:
            player.isJump = False
            player.jumpCount = 10

    redrawGameWindow()
