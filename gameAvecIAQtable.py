#we import the necessary libraries
from datetime import datetime
from pathlib import Path

import numpy as np
import pygame  #library for managing the game
from math import pi, sin, cos  # Functions and constant necessary for the calculation of speeds in x and y
from random import randint  # Function to randomize the terrain generation

#import torch

#import IA
from Qlearning import Agent

def groundGen():  # Function to generate the terrain randomly
    global field  # It is used because the global variable field is going to be modified

         # The field vector will contain the height of the terrain, each position of the vector
        # contains the height of 3 contiguous pixels

        # The first height will be an integer between 100 and height (the height of the window) - 100
        # so that it is not too low or too high
    field[0] = randint(100, height - 100)

      # The terrain is divided into 4 parts and each one will have a random positive or negative slope
     # The slopes are random but the range of randomness is -2 to 5 for a positive slope
     # since most numbers will be positive and -5 to 2 for a negative slope
     # The upDown variable will store the ranges for the terrain randomness
     # The first slope is determined by the first height
    upDown = [(-2, 5)] if field[0] < height // 2 else [(-5, 2)]

    # Randomly attach the ranks of the other 3 parts of the terrain
    for i in range(3):
        up = randint(0, 1)
        if up:
            upDown.append((-2, 5))
        else:
            upDown.append((-5, 2))

    # Randomly fill terrain heights, terrain is formed by adding a random number to
    # the immediately preceding height
    for i in range(1, len(field)):
        limits = upDown[(i * 3) // (width // 4)]
        r = randint(limits[0], limits[1])
        field[i] = max(0, field[i - 1] + r)


def changeTurn():  # Function to change shifts when one of the tanks fires
    global turn, angle, vel, vel1, vel2, angle1, angle2, movLimit
    turn = not turn   # When the variable turn is True, it is tank 1's turn and False is tank 2's turn.
    movLimit = 50  

     # The variable movLimit is the limit of pixels that each tank can move per turn

     # The vel and angle variables store the data to be displayed on the screen
     # The variables vel1 and angle1 store the last speed and angle with which tank 1 fired
     # The variables vel2 and angle2 store the last speed and angle with which tank 2 fired
    if turn:
        vel2, vel = vel, vel1
        angle2, angle = angle, angle1
    else:
        vel1, vel = vel, vel2
        angle1, angle = angle, angle2


def initTanks():  #fonction pour creer un nouveau jeu
    global tank1rect, tank2rect, angle, vel, vel1, vel2, angle1, angle2, turn, movLimit, field, score1, score2, turnsLimit, fire



    #we initialize global variables
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


# we initiate the game
pygame.init()
# # The 1000x600 window is displayed
size = 1000, 600
screen = pygame.display.set_mode(size)

# The colors to be used for the letters of the game are defined
black = (0, 0, 0)
gray = (180, 180, 180)

# We initialize width and height variables because they are going to be used a lot
width, height = 1000, 600

# The images to be used in the game are loaded and scaled to the appropriate size
# also the necessary objects are found the rectangle that contains the images to reposition the images
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

# The global variable field will contain the heights of the terrain in every 3 pixels
# size is width/3 because each field position represents 3 pixels
field = [100] * (width // 3)

# Create the global variables to be used
run = True # Variable to always be running until closed

# Control variables used in game logic
fire = False
win = False

gravityAcceleration = 9.8  # positive because in the game the positive is down

# Initial velocities and angles
vel1 = 20
vel2 = 20
vel = vel1
angle1 = 45
angle2 = 135
angle = angle1

# starting score
score1 = 0
score2 = 0

# Number of turns in 1 round
turnsLimit = 20

turn = True  # True tank1, False tank2
movLimit = 50
# Start a new game
initTanks()

# The texts that are going to be used in the game are created and the rectangle that contains them is also found

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
    tankDistance = (tank2rect.left - tank1rect.centerx) if turn else (tank2rect.centerx - tank1rect.right)
    diff = min(abs(d - (tankDistance)), abs(d - (tankDistance + 30)))

    return diff


# Fonction pour faire des actions
def updateGame(action):
    # action:
    # (pas une action ici) Droite      A
    # (pas une action ici) Gauche      D
    # 0 ->   +Angle      Q
    # 1 ->   -Angle      E
    # 2 ->   +Puissance  W
    # 3 ->   -Puissance  S
    # 4  ->   Tirer       J

    global tank1rect, tank2rect, angle, vel, vel1, vel2, angle1, angle2, turn, movLimit, field, score1, score2, turnsLimit, fire, vx, vy

    #reward = -1000000

    keys = pygame.key.get_pressed()  # Se guarda un arreglo donde las teclas presionadas estan en True y las dem√°s en False

    state = None
           # If the D or A key is pressed then the tank on turn moves one pixel to the
        # right or left as appropriate and the movement limit is decreased by 1
    if (keys[pygame.K_d]) and movLimit:
        if turn and tank1rect.right < width:
            tank1rect = tank1rect.move(1, 0)
        elif not turn and tank2rect.right < width:
            tank2rect = tank2rect.move(1, 0)
        movLimit -= 1

        dis = calculerCollition()
        state = np.array(
            [tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis]).astype(
            np.float32)
        #reward = -dis / 10

    if (keys[pygame.K_a]) and movLimit:
        if turn and tank1rect.left > 0:
            tank1rect = tank1rect.move(-1, 0)
        elif not turn and tank2rect.left > 0:
            tank2rect = tank2rect.move(-1, 0)
        movLimit -= 1

        # dis = calculerCollition()
        # state = np.array([tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis]).astype(np.float32)
        # reward = -dis / 10

     # If the key pressed is Q or E, 1 is added or subtracted to the angle as appropriate
     # The angle always has modulo 360 so that it is between 0 and 359
    if keys[pygame.K_q] or action == 0:
        angle = (angle + 1) % 360

        # dis = calculerCollition()
        # state = np.array([tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis]).astype(np.float32)
        # reward = -dis / 10

    if keys[pygame.K_e] or action == 1:
        angle = (angle - 1) % 360

        # dis = calculerCollition()
        # state = np.array([tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis]).astype(np.float32)
        # reward = -dis / 10

        # If the pressed key is W or S, 1 is added or subtracted from the initial speed as appropriate
        # The initial speed can be minimum 0 and maximum 40
    if (keys[pygame.K_w] or action == 2) and vel < 40:
        vel += 1

        # dis = calculerCollition()
        # state = np.array([tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis]).astype(np.float32)
        # reward = -dis / 10

    if (keys[pygame.K_s] or action == 3) and vel > 0:
        vel -= 1

        # dis = calculerCollition()
        # state = np.array([tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis]).astype(np.float32)
        # reward = -dis / 10


  # If the key pressed is J, the initial speed in X and Y is calculated and the control variable fire is set to True    if keys[pygame.K_j] or action == 4:
        vx = vel * cos(rads)
        vy = -vel * sin(rads)  # coordinates in Y in the game go in the opposite direction (negative )
        fire = True

        turnsLimit -= 1   # When triggered, decrease the number of turns remaining by 1

        #  The initial position of the fireball depends on the tank that is in turn
        fireBallRect.x = tank1rect.x if turn else tank2rect.x
        fireBallRect.y = tank1rect.y if turn else tank2rect.y

        # dis = calculerCollition()
        # state = np.array([tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis]).astype(np.float32)
        # reward = 10000 if dis < 30 else -dis

    # dis = calculerCollition()
    return #state , reward, win


# use_cuda = torch.cuda.is_available()
# print(f"Using CUDA: {use_cuda}")
# print()

# save_dir1 = Path("checkpoints1") / datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
# save_dir1.mkdir(parents=True)
# save_dir2 = Path("checkpoints2") / datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
# save_dir2.mkdir(parents=True)

# tank1IA = IA.Tank(state_dim=7, action_dim=7, save_dir=save_dir1)
# tank1IA.net.load_state_dict(torch.load("net_IA1.chkpt")["model"])
# tank1IA.exploration_rate = 0

# tank2IA = IA.Tank(state_dim=7, action_dim=7, save_dir=save_dir2)
# tank2IA.net.load_state_dict(torch.load("net_IA2.chkpt")["model"])
# tank2IA.exploration_rate = 0

# logger1 = IA.MetricLogger(save_dir1)
# logger2 = IA.MetricLogger(save_dir2)

tank1IA = Agent(".\Q_table.npy")
print("Loaded Q table:")
print(tank1IA.Q)

episodes = 100000
for e in range(episodes):
    initTanks()
    win = False
    dis = calculerCollition()
    state = np.array([tank1rect.centerx, tank1rect.centerx, tank2rect.centerx, tank2rect.centerx, angle, vel, dis])
    # reward = 1000 if dis < 30 else -dis

    if not run: break

    # Le cycle qui maintiendra le jeu actif est crÈÈ
    while not win:

        if not run: break

        for event in pygame.event.get():  # Les ÈvÈnements qui se produisent dans le jeu sont passÈs en revue
             # Si l'ÈvÈnement est de quitter la fenÍtre, la boucle est rompue
            if event.type == pygame.QUIT:
                print("Quit")
                run = False

         # The background image is rendered in the window
        screen.blit(background, [0, 0])

        # # In the mouse variable the mouse position is saved and in the click variable it is saved if the click is pressed
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #If the button is clicked, the game is restarted with the initTanks() function
        if resetRect.left < mouse[0] < resetRect.right and resetRect.top < mouse[1] < resetRect.bottom:
            if click[0]:
                win = False
                initTanks()

        # Tanks are placed at ground level and rendered
        tank2rect.bottom = height - field[tank2rect.centerx // 3]
        tank1rect.bottom = height - field[tank1rect.centerx // 3]
        screen.blit(tank1, tank1rect)
        screen.blit(tank2, tank2rect)

        # For each height stored in the field variable, the part of the terrain is scaled and rendered
        for pix, h in enumerate(field):
            groundPix = pygame.transform.scale(ground, (3, h))
            groundRect = groundPix.get_rect()
            groundRect.bottom = height
            groundRect.x = pix * 3
            screen.blit(groundPix, groundRect)

        # Render the reset button
        screen.blit(reset, resetRect)

        # Render angle, power, remaining turns and scores
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
        # If the control variable win is True, the text of the tank that won is displayed
        # also a play again button is shown and if clicked the game is restarted with the initTanks() function

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

            pygame.display.flip() ## This function updates what is in the window
            continue  # Go to the next cycle without looking at the bottom because it is no longer necessary

        # passer du deg au rad
        rads = angle * pi / 180

    # The distance in X and Y at which the sight will be located, which will allow easier aiming, is calculated.
        sightDistX = vel * 3 * cos(rads)
        sightDistY = vel * 3 * sin(rads)

    # The sight is rendered at the place of the tank that has the turn
        if turn:
            sightRect.x = tank1rect.x + sightDistX
            sightRect.y = tank1rect.y - sightDistY
            screen.blit(sight, sightRect)
        else:
            sightRect.x = tank2rect.x + sightDistX
            sightRect.y = tank2rect.y - sightDistY
            screen.blit(sight, sightRect)

    # If the control variable fire is True, all fire logic is handled and everything else is stopped
       

        if fire:
        # Render the shot
            screen.blit(fireBall, fireBallRect)
        # The fireball moves according to the calculated speed in x and y
            fireBallRect = fireBallRect.move(vx, vy)
        # # The speed is updated according to the gravitational acceleration
            vy += gravityAcceleration * 0.1
        # In the adver variable the rectangle containing the opponent's tank is saved
            adver = tank2rect if turn else tank1rect

        # If there is a collision between the fireball and the opponent, an explosion is rendered on the opponent's tank
         # Depending on whose turn it was, 1 is added to their score and the fire variable becomes False
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

        # # If the fireball leaves the window from the sides, it changes turns
            if fireBallRect.left < 0 or fireBallRect.right > width:
                changeTurn()
                fire = False

        # condition to know if the fireball hits the ground
            elif fireBallRect.bottom > height - field[fireBallRect.centerx // 3]:
                impact = fireBallRect.centerx

                ref = field[impact // 3]

            # An explosion is rendered at the impact site
                explosionRect.centerx = fireBallRect.centerx
                explosionRect.centery = fireBallRect.centery
                screen.blit(explosion, explosionRect)

            # Height is subtracted from the terrain to simulate a 20px radius explosion on the terrain
             # for pf in range(20):
             # res = int(pow(pow(20, 2) - pow(pf, 2), 0.5))
             # if (impact - pf) // 3 > 0:
             # field[(impact - pf) // 3] = max(0, max(field[(impact - pf) // 3] - res,
             # min(field[(impact - pf) // 3], ref - res)))
             # if (impact + pf) // 3 < len(field):
             # field[(impact + pf) // 3] = max(0, max(field[(impact + pf) // 3] - res,
             # min(field[(impact + pf) // 3], ref - res)))

             # After the exposure, change shifts
                changeTurn()
                fire = False

            pygame.display.flip()  # This function updates what is in the window
            continue  # Skip to the next loop without looking at the bottom because it's no longer needed

    # If turns remaining is 0 then set the control variable win to True to end the game
        if not turnsLimit:
            win = True

        if turn:
            # Run agent on the state
            #action = tank1IA.act(state)
            action = tank1IA.play()
        else:
            #action = tank2IA.act(state)
            action = -1
            

        #next_state, reward, done = updateGame(action)

        updateGame(action)

        # # if next_state is not None:
        # #     # if turn:
        # #     #     # Remember
        # #     #     tank1IA.cache(state, next_state, action, reward, done)
        # #     #     # Learn
        # #     #     q, loss = tank1IA.learn()
        # #     #     logger1.log_step(reward, loss, q)
        # #     # else:
        # #     #     tank2IA.cache(state, next_state, action, reward, done)
        # #     #     # print(f"TANK2 next_State: {next_state},\t reward :{reward},\t done :{done}")
        # #     #     # Learn
        # #     #     q, loss = tank2IA.learn()
        # #     #     logger2.log_step(reward, loss, q)

        # #     # Update state
        # #     state = next_state

        pygame.display.flip()  # This function updates what is in the window

    # logger1.log_episode()
    # logger2.log_episode()

    # if e % 1 == 0:
    #     logger1.record(episode=e, epsilon=tank1IA.exploration_rate, step=tank1IA.curr_step)
    #     logger2.record(episode=e, epsilon=tank2IA.exploration_rate, step=tank2IA.curr_step)

pygame.quit()  # When the cycle ends, the window closes
