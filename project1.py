import math
import time

import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("background.png")
background_sound = pygame.mixer.Sound("background.wav")

playerIMG = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

enemyIMG = []
enemyX = []
enemyY = []

enemyX_change = []
enemyY_change = []

number_of_enemies = 5
for i in range(number_of_enemies):
    enemyIMG.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 750))
    enemyY.append(random.randint(20, 70))
    enemyX_change.append(4)
    enemyY_change.append(10)

bulletIMG = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_status = "ready"

FPS = 60
clock = pygame.time.Clock()


def player(x, y):
    screen.blit(playerIMG, (x, y))


def enemy(x, y, i):
    screen.blit(enemyIMG[i], (x, y))


def fire_bullet(x, y):
    global bullet_status
    bullet_status = "fire"
    screen.blit(bulletIMG, (x, y))


def isCollision(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt(math.pow
                         (enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2))
                         )
    if distance < 27:
        return True
    else:
        return False


running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX += 10
            if event.key == pygame.K_LEFT:
                playerX -= 10
            if event.key == pygame.K_SPACE:
                if bullet_status == "ready":
                    bulletSound = pygame.mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

    if bulletY <= 0:
        bulletY = 480
        bullet_status = "ready"
    if bullet_status == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Dushmanlarni harakatlantirish
    for i in range(number_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = isCollision(bulletX, bulletY, enemyX[i], enemyY[i])

        if collision:
            collisionSound = pygame.mixer.Sound("explosion.wav")
            collisionSound.play()
            bulletY = 480
            bullet_status = "ready"
            enemyX[i] = random.randint(0, 750)
            enemyY[i] = random.randint(20, 150)

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)

    pygame.display.update()
