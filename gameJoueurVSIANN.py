# Se importan las librerías necesarias y funciones necesarias
from datetime import datetime
from pathlib import Path

import numpy as np
import pygame  # Librería para el manejo del Juego
from math import pi, sin, cos  # Funciones y constante necesarias para el calculo de velocidades en x e y
from random import randint  # Funcion para aleatorizar la generación del terreno

import torch

import IA


def groundGen():  # Función para generar el terreno aleatoriamente
    global field  # Se utiliza porque se va a modificar la variable global field

    # El vector field va a contener la altura del terreno, cada posición del vector
    # contiene la altura de 3 píxeles contiguos

    # La primera altura será un número entero entre 100 y height (la altura de la ventana) - 100
    # para que no quede tan abajo ni tan arriba
    field[0] = randint(100, height - 100)

    # El terreno esta dividido en 4 partes y cada una tendrá una pendiente positiva o negativa aleatoriamente
    # La pendientes son aleatorias pero el rango de aleatoriedad es de -2 a 5 para una pendiente positiva
    # ya que la mayoría de numeros seran positivos y de -5 a 2 para una pendiente negativa
    # La variable upDown guardará los rangos para la aleatoriedad del terreno
    # La primera pendiente esta determinada por la primer altura
    upDown = [(-2, 5)] if field[0] < height // 2 else [(-5, 2)]

    # Adjuntar aleatoriamente los rangos de las otras 3 partes del terreo
    for i in range(3):
        up = randint(0, 1)
        if up:
            upDown.append((-2, 5))
        else:
            upDown.append((-5, 2))

    # Llenar aleatoriamente las alturas del terreno, el terreno se forma sumando un número aleatorio a
    # la altura inmediatamente anterior
    for i in range(1, len(field)):
        limits = upDown[(i * 3) // (width // 4)]
        r = randint(limits[0], limits[1])
        field[i] = max(0, field[i - 1] + r)


def changeTurn():  # Función para cambiar de turno cuando uno de los tanques dispara
    global turn, angle, vel, vel1, vel2, angle1, angle2, movLimit
    turn = not turn  # Cuando la variable turn es True, es el turno del tanque 1 y False es el turno del tanque 2
    movLimit = 50  # La variable movLimit es el limite de pixeles que se puede mover cada tanque por turno

    # Las variable vel y angle guardan los datos que se van a mostrar en pantalla
    # Las variables vel1 y angle1 guarda la última velocidad y angulo con las que disparo el tanque 1
    # Las variables vel2 y angle2 guarda la última velocidad y angulo con las que disparo el tanque 2
    if turn:
        vel2, vel = vel, vel1
        angle2, angle = angle, angle1
    else:
        vel1, vel = vel, vel2
        angle1, angle = angle, angle2


def initTanks():  # Funcion para crear un juego nuevo
    global tank1rect, tank2rect, angle, vel, vel1, vel2, angle1, angle2, turn, movLimit, field, score1, score2, turnsLimit, fire

    # se genera un nuevo terreno
    # groundGen()

    # se ponen todas las variables globales en sus valores iniciales
    tank2rect.x = 900
    tank2rect.bottom = height - field[900 // 3]
    tank1rect.x = 50
    tank1rect.bottom = height - field[50 // 3]
    vel1 = 20
    vel2 = 20
    vel = vel1
    angle1 = 45
    angle2 = 135
    angle = angle1
    turn = True
    fire = False
    movLimit = 50
    score1 = 0
    score2 = 0
    turnsLimit = 20


# Se inicia pygame
pygame.init()
# Se muestra la ventana de 1000x600
size = 1000, 600
screen = pygame.display.set_mode(size)

# Se definen los colores que se van a utilizar para las las letras del juego
black = (0, 0, 0)
gray = (180, 180, 180)

# Inicializamos variables de ancho y alto porque se van a utilizar bastante
width, height = 1000, 600

# Se cargan las imágenes que se van a utilizar en el juego y se escalan al tamaño adecuado
# tambien a los objetos necesarios se le halla el rectangulo que contiene las imagenes para reposicionar las imágenes
background = pygame.image.load("images/background.png")
background = pygame.transform.scale(background, (width, height))

fireBall = pygame.image.load("images/fireBall.png")
fireBall = pygame.transform.scale(fireBall, (15, 15))
fireBallRect = fireBall.get_rect()

sight = pygame.image.load("images/sight.png")
sight = pygame.transform.scale(sight, (20, 20))
sightRect = sight.get_rect()

explosion = pygame.image.load("images/explosion.png")
explosion = pygame.transform.scale(explosion, (50, 50))
explosionRect = explosion.get_rect()

playAgain = pygame.image.load("images/playAgainButton.png")
playAgain = pygame.transform.scale(playAgain, (140, 70))
playAgainRect = playAgain.get_rect()
playAgainRect.center = (width // 2, height // 2 + 35)

reset = pygame.image.load("images/resetButton.png")
reset = pygame.transform.scale(reset, (30, 30))
resetRect = reset.get_rect()
resetRect.center = (width // 2, height - 20)

tank1 = pygame.image.load("images/tank1.png")
tank1 = pygame.transform.scale(tank1, (30, 30))
tank1rect = tank1.get_rect()
tank2 = pygame.image.load("images/tank2.png")
tank2 = pygame.transform.scale(tank2, (30, 30))
tank2rect = tank2.get_rect()

ground = pygame.image.load("images/ground.png")

# La variable global field va a contener las alturas del terreno en cada 3 píxeles
# el tamaño es width/3 porque cada posición de field representa 3 píxeles
field = [100] * (width // 3)

# Se crean las variables globales que se va a utilizar
run = True  # Variable para que siempre esté corriendo hasta que lo cierren

# Variables de control usadas en la lógica del juego
fire = False
win = False

gravityAcceleration = 9.8  # positivo porque el el juego el positivo es hacia abajo

# Velocidades y angulos iniciales
vel1 = 20
vel2 = 20
vel = vel1
angle1 = 45
angle2 = 135
angle = angle1

# Puntaje inicial
score1 = 0
score2 = 0

# Cantidad de turnos en 1 ronda
turnsLimit = 20

turn = True  # True tank1, False tank2
movLimit = 50

# Se incia un nuevo juego
initTanks()

# Se crean los textos que se van a utilizar en el juego y tambien se halla el rectangulo que los contienen
font = pygame.font.Font('freesansbold.ttf', 32)
textWin1 = font.render('Tank 1 Wins', True, black, gray)
textWin1Rect = textWin1.get_rect()
textWin1Rect.center = (width // 2, height // 2 - 35)

textWin2 = font.render('Tank 2 Wins', True, black, gray)
textWin2Rect = textWin2.get_rect()
textWin2Rect.center = (width // 2, height // 2 - 35)

textDraw = font.render('Draw', True, black, gray)
textDrawRect = textDraw.get_rect()
textDrawRect.center = (width // 2, height // 2 - 35)

textTurn = font.render('Turns', True, black, gray)
textTurnRect = textTurn.get_rect()
textTurnRect.center = (width // 2, 30)

numberTurn = font.render(str(turnsLimit), True, black, gray)
numberTurnRect = numberTurn.get_rect()
numberTurnRect.center = (width // 2, 70)

textAngleLetters = font.render("Angle", True, black, gray)
textAngleLettersRect = textAngleLetters.get_rect()
textAngleLettersRect.center = (width // 2 - 100, height - 20)

textAngle = font.render(str(angle), True, black, gray)
textAngleRect = textAngle.get_rect()
textAngleRect.center = (width // 2 - 100, height - 60)

textPowerLetters = font.render("Power", True, black, gray)
textPowerLettersRect = textPowerLetters.get_rect()
textPowerLettersRect.center = (width // 2 + 100, height - 20)

textVel = font.render(str(vel * 100 // 40), True, black, gray)
textVelRect = textVel.get_rect()
textVelRect.center = (width // 2 + 100, height - 60)

textTank1 = font.render("Tank1", True, black, gray)
textTank1Rect = textTank1.get_rect()
textTank1Rect.left = 10
textTank1Rect.centery = 30

numberTank1 = font.render(str(score1), True, black, gray)
numberTank1Rect = numberTank1.get_rect()
numberTank1Rect.center = (30, 70)

textTank2 = font.render("Tank2", True, black, gray)
textTank2Rect = textTank2.get_rect()
textTank2Rect.right = 990
textTank2Rect.centery = 30

numberTank2 = font.render(str(score2), True, black, gray)
numberTank2Rect = numberTank2.get_rect()
numberTank2Rect.center = (950, 70)


# fonction pour savoir si le tir touchera la cible
def calculerCollition():
    global tank1rect, tank2rect, angle, vel, turn
    rads = angle * pi / 180
    d = pow(vel, 2) * sin(2 * rads)
    d = d if turn else -d
    tankDistance = tank2rect.x - tank1rect.x
    diff = abs(d - tankDistance)
    if (tankDistance+10) > d > (tankDistance-5):
        diff=0
    return diff


# Fonction pour faire des actions
def updateGame(action):
    # action:
    # 0 ->   Droite      A
    # 1 ->   Gauche      D
    # 2 ->   +Angle      Q
    # 3 ->   -Angle      E
    # 4 ->   +Puissance  W
    # 5 ->   -Puissance  S
    # 6 ->   Tirer       J

    global tank1rect, tank2rect, angle, vel, vel1, vel2, angle1, angle2, turn, movLimit, field, score1, score2, turnsLimit, fire, vx, vy

    reward = -1000000

    keys = pygame.key.get_pressed()  # Se guarda un arreglo donde las teclas presionadas estan en True y las demás en False

    state = None
    # Si la tecla D o A están presionadas entonces el tanque que está de turno se mueve un píxel a la
    # derecha o a la izquierda según corresponda y se disminuye en 1 el limite de movimiento
    if (keys[pygame.K_d] or action == 0) and movLimit:
        if turn and tank1rect.right < width:
            tank1rect = tank1rect.move(1, 0)
        elif not turn and tank2rect.right < width:
            tank2rect = tank2rect.move(1, 0)
        movLimit -= 1

        dis = calculerCollition()
        state = np.array(
            [tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis]).astype(
            np.float32)
        reward = -dis / 10

    if (keys[pygame.K_a] or action == 1) and movLimit:
        if turn and tank1rect.left > 0:
            tank1rect = tank1rect.move(-1, 0)
        elif not turn and tank2rect.left > 0:
            tank2rect = tank2rect.move(-1, 0)
        movLimit -= 1

        dis = calculerCollition()
        state = np.array([tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis]).astype(np.float32)
        reward = -dis / 10

    # Si la tecla presionadas es Q o E, se le suma o se le resta 1 al angulo según corresponda
    # El ángulo siempre tiene modulo 360 para que esté entre 0 y 359
    if keys[pygame.K_q] or action == 2:
        angle = (angle + 1) % 360

        dis = calculerCollition()
        state = np.array([tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis]).astype(np.float32)
        reward = -dis / 10

    if keys[pygame.K_e] or action == 3:
        angle = (angle - 1) % 360

        dis = calculerCollition()
        state = np.array([tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis]).astype(np.float32)
        reward = -dis / 10

    # Si la tecla presionadas es W o S, se le suma o se le resta 1 a la velocidad inicial según corresponda
    # La velocidad inicial puede ser mínimo 0 y máximo 40
    if (keys[pygame.K_w] or action == 4) and vel < 40:
        vel += 1

        dis = calculerCollition()
        state = np.array([tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis]).astype(np.float32)
        reward = -dis / 10

    if (keys[pygame.K_s] or action == 5) and vel > 0:
        vel -= 1

        dis = calculerCollition()
        state = np.array([tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis]).astype(np.float32)
        reward = -dis / 10

    # Si la tecla presionada es J, se calcula la velocidad inicial en X y en Y y la variable de control fire se pone en True
    if keys[pygame.K_j] or action == 6:
        vx = vel * cos(rads)
        vy = -vel * sin(rads)  # coordenadas en Y en el juego van en sentido contrario (negativo arriba)
        fire = True

        turnsLimit -= 1  # Cuando se dispara se disminuye en 1 la cantidad de turnos restantes

        # La posición inicial de la bola de fuego depende del tanque que este de turno
        fireBallRect.x = tank1rect.x if turn else tank2rect.x
        fireBallRect.y = tank1rect.y if turn else tank2rect.y

        dis = calculerCollition()
        state = np.array([tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis]).astype(np.float32)
        reward = 10000 if not dis else -dis

    # dis = calculerCollition()
    return state, reward, win


use_cuda = torch.cuda.is_available()
print(f"Using CUDA: {use_cuda}")
print()

save_dir1 = Path("checkpoints1") / datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
save_dir1.mkdir(parents=True)
save_dir2 = Path("checkpoints2") / datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
save_dir2.mkdir(parents=True)

tank1IA = IA.Tank(state_dim=7, action_dim=7, save_dir=save_dir1)
# tank1IA.net.load_state_dict(torch.load("net_IA1.chkpt")["model"])
tank1IA.net.load_state_dict(torch.load("2tank1.chkpt")["model"])
tank1IA.exploration_rate = 0

tank2IA = IA.Tank(state_dim=7, action_dim=7, save_dir=save_dir2)
# tank2IA.net.load_state_dict(torch.load("net_IA2.chkpt")["model"])
tank2IA.net.load_state_dict(torch.load("2tank2.chkpt")["model"])
tank2IA.exploration_rate = 0

logger1 = IA.MetricLogger(save_dir1)
logger2 = IA.MetricLogger(save_dir2)

initTanks()
win = False
dis = calculerCollition()
state = np.array([tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis])

# Se crea el ciclo que mantendrá activo el juego
while True:

    for event in pygame.event.get():  # Se revisan los evento que suceden en el juego
        # Si el evento es salir de la ventana, se rompe el ciclo
        if event.type == pygame.QUIT:
            run = False

    # Se renderiza en la ventana la imágen del fondo
    screen.blit(background, [0, 0])

    # En la variable mouse se guarda la posición del mouse y en la variable click se guarda si el click está presionado
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Si se da click en el botón, se vuelve a iniciar el juego con la función initTanks()
    if resetRect.left < mouse[0] < resetRect.right and resetRect.top < mouse[1] < resetRect.bottom:
        if click[0]:
            win = False
            initTanks()

    # Se sitúan los tanques a la altura del terreno y se renderizan
    tank2rect.bottom = height - field[tank2rect.centerx // 3]
    tank1rect.bottom = height - field[tank1rect.centerx // 3]
    screen.blit(tank1, tank1rect)
    screen.blit(tank2, tank2rect)

    # Por cada altura guardada en la variable field se escala la parte del terreno y se renderiza
    for pix, h in enumerate(field):
        groundPix = pygame.transform.scale(ground, (3, h))
        groundRect = groundPix.get_rect()
        groundRect.bottom = height
        groundRect.x = pix * 3
        screen.blit(groundPix, groundRect)

    # Se renderiza el botón de reset
    screen.blit(reset, resetRect)

    # Se renderiza el angulo, el poder, los turnos restantes y los puntajes
    screen.blit(textAngleLetters, textAngleLettersRect)
    textAngle = font.render(str(angle), True, black, gray)
    screen.blit(textAngle, textAngleRect)
    screen.blit(textPowerLetters, textPowerLettersRect)
    textVel = font.render(str(vel * 100 // 40), True, black, gray)
    screen.blit(textVel, textVelRect)
    screen.blit(textTurn, textTurnRect)
    numberTurn = font.render(str(turnsLimit), True, black, gray)
    screen.blit(numberTurn, numberTurnRect)
    screen.blit(textTank1, textTank1Rect)
    numberTank1 = font.render(str(score1), True, black, gray)
    screen.blit(numberTank1, numberTank1Rect)
    screen.blit(textTank2, textTank2Rect)
    numberTank2 = font.render(str(score2), True, black, gray)
    screen.blit(numberTank2, numberTank2Rect)

    # Si la variable de control win está en True se muestra el texto del tanque que ganó
    # además se muestra un botón de volver a jugar y si se da click se reinicia el juego con la funcion initTanks()
    if win:
        if score1 > score2:
            screen.blit(textWin1, textWin1Rect)
        elif score2 > score1:
            screen.blit(textWin2, textWin2Rect)
        else:
            screen.blit(textDraw, textDrawRect)

        screen.blit(explosion, explosionRect)
        screen.blit(playAgain, playAgainRect)

        if playAgainRect.left < mouse[0] < playAgainRect.right and playAgainRect.top < mouse[
            1] < playAgainRect.bottom:
            if click[0]:
                initTanks()
                win = False

        pygame.display.flip()  # Esta función actualiza lo que hay en la ventana
        continue  # Pasa al siguiente ciclo sin mirar lo de abajo porque ya no es necesario

    # Se pasa el angulo a radianes
    rads = angle * pi / 180

    # Se calculan la distancia en X y en Y a la cual va a estar ubicada la mira que permitira apuntar más fácilmente
    sightDistX = vel * 3 * cos(rads)
    sightDistY = vel * 3 * sin(rads)

    # La mira se renderiza en el lugar del tanque que tiene el turno
    if turn:
        sightRect.x = tank1rect.x + sightDistX
        sightRect.y = tank1rect.y - sightDistY
        screen.blit(sight, sightRect)
    else:
        sightRect.x = tank2rect.x + sightDistX
        sightRect.y = tank2rect.y - sightDistY
        screen.blit(sight, sightRect)

    # Si la variable de control fire está en True, se maneja toda la lógica del disparo y lo demás se detiene
    if fire:
        # Se renderiza el disparo
        screen.blit(fireBall, fireBallRect)
        # La bola de fuego se mueve según la velocidad calculada en x y en y
        fireBallRect = fireBallRect.move(vx, vy)
        # Se actualiza la velocidad de acuerdo a la aceleración gravitacional
        vy += gravityAcceleration * 0.1
        # En la variable adver se guarda el rectangulo que contiene el tanque adversario
        adver = tank2rect if turn else tank1rect

        # Si hay colisión entre la bola de fuego y el adversario, se renderiza una explosión sobre el tanque adversario
        # Dependiendo de quien era el turno se le suma 1 a su puntaje y la variable fire se vuelve False
        if fireBallRect.colliderect(adver):
            explosionRect.x = adver.x
            explosionRect.y = adver.y
            screen.blit(explosion, explosionRect)

            if turn:
                score1 += 1
            else:
                score2 += 1

            changeTurn()
            fire = False

        # Si la bola de fuego sale de la ventana por los lados, se cambia de turno
        if fireBallRect.left < 0 or fireBallRect.right > width:
            changeTurn()
            fire = False

        # Condición para saber si la bola de fuego toca el piso
        elif fireBallRect.bottom > height - field[fireBallRect.centerx // 3]:
            impact = fireBallRect.centerx

            ref = field[impact // 3]

            # Se renderiza una explosión en el lugar del impacto
            explosionRect.centerx = fireBallRect.centerx
            explosionRect.centery = fireBallRect.centery
            screen.blit(explosion, explosionRect)

            # Se resta altura al terreno para simular una explosiónde radio de 20 píxeles en el terreno
            # for pf in range(20):
            #     res = int(pow(pow(20, 2) - pow(pf, 2), 0.5))
            #     if (impact - pf) // 3 > 0:
            #         field[(impact - pf) // 3] = max(0, max(field[(impact - pf) // 3] - res,
            #                                                min(field[(impact - pf) // 3], ref - res)))
            #     if (impact + pf) // 3 < len(field):
            #         field[(impact + pf) // 3] = max(0, max(field[(impact + pf) // 3] - res,
            #                                                min(field[(impact + pf) // 3], ref - res)))

            # Luego de la exposión se cambia de turno
            changeTurn()
            fire = False

        pygame.display.flip()  # Esta función actualiza lo que hay en la ventana
        continue  # Pasa al siguiente ciclo sin mirar lo de abajo porque ya no es necesario

    # Si turnos restantes es 0 entonces se pone la variable de control win en True para acabar el juego
    if not turnsLimit:
        win = True

    action = -1
    if turn:
        # Run agent on the state
        action = tank1IA.act(state)
    # else:
    #     action = tank2IA.act(state)

    next_state, reward, done = updateGame(action)

    if next_state is not None:
        # print(reward)
        # if turn:
        #     # Remember
        #     tank1IA.cache(state, next_state, action, reward, done)
        #     # Learn
        #     q, loss = tank1IA.learn()
        #     logger1.log_step(reward, loss, q)
        # else:
        #     tank2IA.cache(state, next_state, action, reward, done)
        #     # print(f"TANK2 next_State: {next_state},\t reward :{reward},\t done :{done}")
        #     # Learn
        #     q, loss = tank2IA.learn()
        #     logger2.log_step(reward, loss, q)

        # Update state
        state = next_state

    pygame.display.flip()  # Esta función actualiza lo que hay en la ventana

logger1.log_episode()
logger2.log_episode()

# if e % 1 == 0:
#     logger1.record(episode=e, epsilon=tank1IA.exploration_rate, step=tank1IA.curr_step)
#     logger2.record(episode=e, epsilon=tank2IA.exploration_rate, step=tank2IA.curr_step)

pygame.quit()  # Cual el ciclo se termina, se cierra la ventana
