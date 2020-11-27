import sys, pygame
from math import pi, sin, cos

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

tank1 = pygame.image.load("images/tank1.png")
tank1 = pygame.transform.scale(tank1, (30, 30))
tank1rect = tank1.get_rect()
tank2 = pygame.image.load("images/tank2.png")
tank2 = pygame.transform.scale(tank2, (30, 30))
tank2rect = tank2.get_rect()

tank2rect.move_ip(700, 500)
tank1rect.move_ip(50, 500)

fireBall = pygame.image.load("images/fireBall.png")
fireBall = pygame.transform.scale(fireBall, (20, 20))
fireBallRect = fireBall.get_rect()

explosion = pygame.image.load("images/explosion.png")
explosion = pygame.transform.scale(explosion, (50, 50))
explosionRect = explosion.get_rect()

font = pygame.font.Font('freesansbold.ttf', 32)

textWin = font.render('Tank 1 Wins', True, green, blue)

# create a rectangular object for the
# text surface object
textWinRect = textWin.get_rect()

# set the center of the rectangular object.
textWinRect.center = (width // 2, height // 2)

fire = False
win = False

run = True

gravityAcceleration = 0.8  # positivo porque el el juego el positivo es hacia abajo
vel = 20

while run:
    pygame.time.delay(0)

    for event in pygame.event.get():
        # Si el evento es salir de la ventana, terminamos
        if event.type == pygame.QUIT: run = False

    screen.blit(background, [0, 0])

    screen.blit(tank1, tank1rect)
    screen.blit(tank2, tank2rect)

    if win:
        screen.blit(textWin, textWinRect)
        screen.blit(explosion, explosionRect)
        pygame.display.flip()
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        tank1rect = tank1rect.move(1, 0)
    if keys[pygame.K_a]:
        tank1rect = tank1rect.move(-1, 0)

    if keys[pygame.K_j] and not fire:
        angle = 45 * pi / 180
        vx = vel * cos(angle)
        vy = -vel * sin(angle)  # coordenadas en y en el juego van en sentido contrario
        fire = True
        fireBallRect.x = tank1rect.x
        fireBallRect.y = tank1rect.y

    if fire:
        screen.blit(fireBall, fireBallRect)
        fireBallRect = fireBallRect.move(vx, vy)
        vy += gravityAcceleration * 1
        if fireBallRect.colliderect(tank2rect):
            explosionRect.x = tank2rect.x
            explosionRect.y = tank2rect.y
            screen.blit(explosion, explosionRect)

            print("tank1 WINS")
            win = True
            fire = False

    if fireBallRect.bottom > height:
        fire = False

    pygame.display.flip()

pygame.quit()
