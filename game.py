import sys, pygame
from math import pi, sin, cos


def initTanks():
    global tank1rect, tank2rect, angle

    tank2rect.x = 700
    tank2rect.y = 500
    tank1rect.x = 50
    tank1rect.y = 500
    angle = 45


# Inicializamos pygame
pygame.init()
# Muestro una ventana de 800x600
size = 1000, 600
screen = pygame.display.set_mode(size)

green = (0, 255, 0)
blue = (0, 0, 128)

# Inicializamos variables
width, height = 1000, 600
speed = [1, 1]

background = pygame.image.load("images/background.png")
background = pygame.transform.scale(background, (width, height))

fireBall = pygame.image.load("images/fireBall.png")
fireBall = pygame.transform.scale(fireBall, (20, 20))
fireBallRect = fireBall.get_rect()

explosion = pygame.image.load("images/explosion.png")
explosion = pygame.transform.scale(explosion, (50, 50))
explosionRect = explosion.get_rect()

font = pygame.font.Font('freesansbold.ttf', 32)
textWin = font.render('Tank 1 Wins', True, green, blue)
textWinRect = textWin.get_rect()
textWinRect.center = (width // 2, height // 2)

playAgain = pygame.image.load("images/playAgainButton.png")
playAgain = pygame.transform.scale(playAgain, (110, 70))
playAgainRect = playAgain.get_rect()
playAgainRect.center = (width // 2, height // 2 + 70)

tank1 = pygame.image.load("images/tank1.png")
tank1 = pygame.transform.scale(tank1, (30, 30))
tank1rect = tank1.get_rect()
tank2 = pygame.image.load("images/tank2.png")
tank2 = pygame.transform.scale(tank2, (30, 30))
tank2rect = tank2.get_rect()

initTanks()

fire = False
win = False

run = True

gravityAcceleration = 0.8  # positivo porque el el juego el positivo es hacia abajo
vel = 20

angle = 45

textAngle = font.render(str(angle), True, green, blue)
textAngleRect = textAngle.get_rect()
textAngleRect.center = (30, 30)

while run:
    pygame.time.delay(0)

    for event in pygame.event.get():
        # Si el evento es salir de la ventana, terminamos
        if event.type == pygame.QUIT: run = False

    screen.blit(background, [0, 0])

    screen.blit(tank1, tank1rect)
    screen.blit(tank2, tank2rect)

    textAngle = font.render(str(angle), True, green, blue)
    screen.blit(textAngle, textAngleRect)

    if win:
        screen.blit(textWin, textWinRect)
        screen.blit(explosion, explosionRect)
        screen.blit(playAgain, playAgainRect)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if playAgainRect.left < mouse[0] < playAgainRect.right and playAgainRect.top < mouse[1] < playAgainRect.bottom:
            if click[0]:
                initTanks()
                win = False

        pygame.display.flip()
        continue

    if fire:
        screen.blit(fireBall, fireBallRect)
        fireBallRect = fireBallRect.move(vx, vy)
        vy += gravityAcceleration * 1
        if fireBallRect.colliderect(tank2rect):
            explosionRect.x = tank2rect.x
            explosionRect.y = tank2rect.y
            screen.blit(explosion, explosionRect)
            win = True
            fire = False
        if fireBallRect.bottom > height:
            fire = False
        pygame.display.flip()
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        tank1rect = tank1rect.move(1, 0)
    if keys[pygame.K_a]:
        tank1rect = tank1rect.move(-1, 0)
    if keys[pygame.K_w]:
        angle += 1
    if keys[pygame.K_s]:
        angle -= 1

    if keys[pygame.K_j] and not fire:
        rads = angle * pi / 180
        vx = vel * cos(rads)
        vy = -vel * sin(rads)  # coordenadas en y en el juego van en sentido contrario
        fire = True
        fireBallRect.x = tank1rect.x
        fireBallRect.y = tank1rect.y

    pygame.display.flip()

pygame.quit()
