import pygame
from math import pi, sin, cos


def changeTurn():
    global turn, angle, vel, vel1, vel2, angle1, angle2, movLimit
    turn = not turn
    movLimit = 50

    if turn:
        vel2, vel = vel, vel1
        angle2, angle = angle, angle1
    else:
        vel1, vel = vel, vel2
        angle1, angle = angle, angle2


def initTanks():
    global tank1rect, tank2rect, angle, vel, vel1, vel2, angle1, angle2, turn, movLimit

    tank2rect.x = 900
    tank2rect.y = 542
    tank1rect.x = 50
    tank1rect.y = 542
    vel1 = 20
    vel2 = 20
    vel = vel1
    angle1 = 45
    angle2 = 135
    angle = angle1
    turn = True
    movLimit = 50


# Inicializamos pygame
pygame.init()
# Muestro una ventana de 800x600
size = 1000, 600
screen = pygame.display.set_mode(size)

green = (0, 255, 0)
blue = (0, 0, 128)

# Inicializamos variables
width, height = 1000, 600

background = pygame.image.load("images/background.png")
background = pygame.transform.scale(background, (width, height))

fireBall = pygame.image.load("images/fireBall.png")
fireBall = pygame.transform.scale(fireBall, (20, 20))
fireBallRect = fireBall.get_rect()

sight = pygame.image.load("images/sight.png")
sight = pygame.transform.scale(sight, (20, 20))
sightRect = sight.get_rect()

explosion = pygame.image.load("images/explosion.png")
explosion = pygame.transform.scale(explosion, (50, 50))
explosionRect = explosion.get_rect()

font = pygame.font.Font('freesansbold.ttf', 32)
textWin1 = font.render('Tank 1 Wins', True, green, blue)
textWin1Rect = textWin1.get_rect()
textWin1Rect.center = (width // 2, height // 2 - 35)

textWin2 = font.render('Tank 2 Wins', True, green, blue)
textWin2Rect = textWin2.get_rect()
textWin2Rect.center = (width // 2, height // 2 - 35)

playAgain = pygame.image.load("images/playAgainButton.png")
playAgain = pygame.transform.scale(playAgain, (140, 70))
playAgainRect = playAgain.get_rect()
playAgainRect.center = (width // 2, height // 2 + 35)

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

gravityAcceleration = 9.8  # positivo porque el el juego el positivo es hacia abajo
vel1 = 20
vel2 = 20
vel = vel1

angle1 = 45
angle2 = 135
angle = angle1

textAngle = font.render(str(angle), True, green, blue)
textAngleRect = textAngle.get_rect()
textAngleRect.center = (30, 30)

textVel = font.render(str(vel * 100 // 40), True, green, blue)
textVelRect = textVel.get_rect()
textVelRect.center = (950, 30)

turn = True  # True tank1, False tank2
movLimit = 50

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

    textVel = font.render(str(vel * 100 // 40), True, green, blue)
    screen.blit(textVel, textVelRect)

    if win:
        if turn:
            screen.blit(textWin1, textWin1Rect)
        else:
            screen.blit(textWin2, textWin2Rect)

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

    rads = angle * pi / 180

    if turn:
        sightRect.x = tank1rect.x + vel * 3 * cos(rads)
        sightRect.y = tank1rect.y - vel * 3 * sin(rads)
        screen.blit(sight, sightRect)
    else:
        sightRect.x = tank2rect.x + vel * 3 * cos(rads)
        sightRect.y = tank2rect.y - vel * 3 * sin(rads)
        screen.blit(sight, sightRect)

    if fire:
        screen.blit(fireBall, fireBallRect)
        fireBallRect = fireBallRect.move(vx, vy)
        vy += gravityAcceleration * 0.1
        adver = tank2rect if turn else tank1rect
        if fireBallRect.colliderect(adver):
            explosionRect.x = adver.x
            explosionRect.y = adver.y
            screen.blit(explosion, explosionRect)
            win = True
            fire = False
            # changeTurn()

        if fireBallRect.bottom > 580 or fireBallRect.left < 0 or fireBallRect.right > width:
            fire = False
            changeTurn()
        pygame.display.flip()
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] and movLimit:
        if turn:
            tank1rect = tank1rect.move(1, 0)
        else:
            tank2rect = tank2rect.move(1, 0)
        movLimit -= 1
    if keys[pygame.K_a] and movLimit:
        if turn:
            tank1rect = tank1rect.move(-1, 0)
        else:
            tank2rect = tank2rect.move(-1, 0)
        movLimit -= 1
    if keys[pygame.K_q]:
        angle = (angle + 1) % 360
    if keys[pygame.K_e]:
        angle = (angle - 1) % 360
    if keys[pygame.K_w] and vel < 40:
        vel += 1
    if keys[pygame.K_s] and vel > 0:
        vel -= 1

    if keys[pygame.K_j] and not fire:
        vx = vel * cos(rads)
        vy = -vel * sin(rads)  # coordenadas en y en el juego van en sentido contrario
        fire = True

        fireBallRect.x = tank1rect.x if turn else tank2rect.x
        fireBallRect.y = tank1rect.y if turn else tank2rect.y

    pygame.display.flip()

pygame.quit()
