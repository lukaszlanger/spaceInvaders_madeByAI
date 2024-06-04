import pygame
import random
import math

# Initialize the pygame
pygame.init()

# Create the screen with larger dimensions
screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the clock for controlling FPS
clock = pygame.time.Clock()

# Load and scale the images
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (200, 200))  # Scale background to a smaller logo

playerImg = pygame.image.load('player.png')
playerImg = pygame.transform.scale(playerImg, (50, 50))
playerX = (screen_width // 2) - 25
playerY = screen_height - 100
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    img = pygame.image.load('enemy.png')
    img = pygame.transform.scale(img, (50, 50))
    enemyImg.append(img)
    enemyX.append(random.randint(0, screen_width - 50))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)  # Reduce speed
    enemyY_change.append(20)

bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (10, 30))
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 7  # Reduce speed
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (screen_width // 2 - 200, screen_height // 2 - 32))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 20, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    return distance < 27


running = True
while running:
    # Limit the frame rate to 60 FPS
    clock.tick(60)

    screen.fill((0, 0, 0))
    # Draw the smaller background logo at the center of the screen
    screen.blit(background, ((screen_width - 200) // 2, (screen_height - 200) // 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= screen_width - 50:
        playerX = screen_width - 50

    for i in range(num_of_enemies):
        if enemyY[i] > screen_height - 100:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2  # Reduce speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= screen_width - 50:
            enemyX_change[i] = -2  # Reduce speed
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, screen_width - 50)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
