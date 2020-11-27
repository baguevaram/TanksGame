import sys, pygame

# Inicializamos pygame
pygame.init()
# Muestro una ventana de 800x600
size = 800, 600
screen = pygame.display.set_mode(size)
# Inicializamos variables
width, height = 800, 600
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


fire = False

run = True
while run:
    pygame.time.delay(0)

    for event in pygame.event.get():
        # Si el evento es salir de la ventana, terminamos
        if event.type == pygame.QUIT: run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        tank1rect = tank1rect.move(1, 0)
    if keys[pygame.K_a]:
        tank1rect = tank1rect.move(-1, 0)
    if keys[pygame.K_j] and not fire:

        fire = True
        fireBallRect.x=150
        fireBallRect.y=150

    if fire:
        screen.blit(fireBall, fireBallRect)
        fireBallRect = fireBallRect.move(1, 1.8)

    if fireBallRect.bottom > height:
        fire = False



    screen.blit(background, [0, 0])
    # screen.blit(fireBall, fireBallRect)

    screen.blit(tank1, tank1rect)
    screen.blit(tank2, tank2rect)
    pygame.display.flip()
    # Salgo de pygame
pygame.quit()
