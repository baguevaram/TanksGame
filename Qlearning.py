import numpy as np
#import time

ANGLES_SIZE = 90
VELOCITIES_SIZE = 40 
ACTION_SPACE_SIZE = 5

INITPOS = 50
ENEMYPOS = 900
DISTANCEOPPONENT= abs(ENEMYPOS - INITPOS) #d is the distance between the person who is playing and the opponent A RECTIFIER
#TODO:check Brayan's game to see if the hitbox width is right
HITBOXWIDTH = 30 #the size of the enemy's hit box (region where it is considered a collision if the ball hits)

#movements
ANGLE_UP = 0
ANGLE_DOWN = 1
VELOCITY_UP = 2
VELOCITY_DOWN = 3
FIRE = 4

#parameters of the script
LEARNING_RATE = 0.1
GAMMA = 0.8 #actualisation factor
GOAL_REWARD = 10000000
MISS_PENALITY =  0#penalise the agent if it misses
EXPLORATION_RATE = 0.1
FDPPENALTY = -6000
DELTADECAY = 0.1
ITERATIONS = 1000000


class Agent: #agent that will play the game 

    def __init__(self, Qpath = None):
        #agent's Q table
        if Qpath:
            self.load(Qpath)
        else: 
            self.Q = np.zeros((ANGLES_SIZE, VELOCITIES_SIZE, ACTION_SPACE_SIZE)) 

        #meta parameters of the Q learning algorithm
        self.LearningRate = LEARNING_RATE
        self.gamma = GAMMA
        self.explorationRate = EXPLORATION_RATE
        self.iterations = ITERATIONS

        #initial conditions
        self.initialState = [45,20] #according to the game's initial angle and velocity
        self.maxTurns = 20 #according to the game, the number of turns per player

        #agent's internal states 
        self.state = self.initialState
        self.turnsLeft = self.maxTurns
        self.fired = False

        #mappings from action to index
        self.actionSpace = [self.angleUp, self.angleDown, self.velUp, self.velDown, self.fire]
        
    def action_toString(action):

        match action:
            case 0:
                return "Angle up"
            case 1:
                return "Angle down"
            case 2:
                return "Velocitu up"
            case 3:
                return "Velocity Down"
            case 4:
                return "Fire!"
            
            case _:
                return "wtf"



    #actions of the agent
    def angleUp(self):
        if self.state[0] + 1 < ANGLES_SIZE:
            self.state[0] += 1

    def angleDown(self):            
        if self.state[0] -1 >= 0:
            self.state[0] -= 1

    def velUp(self):
        if self.state[1] + 1 < VELOCITIES_SIZE:
            self.state[1] += 1

    def velDown(self):
        if self.state[1] - 1 >= 0:
            self.state[1] -= 1

    def fire(self): 
        self.fired = True
        self.turnsLeft -= 1

    def reset(self): #resets the game and the state of the agent
        self.fired = False
        self.state = self.initialState
        self.turnsLeft = self.maxTurns


    def calculerCollision(x,v): #to kn  ow where the fireball will hit

        rads = x * np.pi / 180
        d = v**2 * np.sin(2*rads) #according to Brayan's formula
        #return ((2*v*v*np.cos(rads)*np.sin(rads))/9.806)
        return min(abs(d - DISTANCEOPPONENT),abs( d - (DISTANCEOPPONENT + HITBOXWIDTH )))

#je laisse ça ici pour comparer avec la fonction de Brayan hihi
# # fonction pour savoir si le tir touchera la cible
# def calculerCollition():
#     global tank1rect, tank2rect, angle, vel
#     rads = angle * pi / 180
#     d = pow(vel, 2) * sin(2 * rads)

#     tankDistance = tank2rect.left - tank1rect.centerx
#     diff = min(abs(d - (tankDistance)), abs(d - (tankDistance + 30)))

#     return diff

    #sample an action according to the epsilon greedy method
    def sampleAction(self):
        #Explore
        if np.random.rand() < self.explorationRate:
            return np.random.randint(0 , ACTION_SPACE_SIZE)
        
        #Exploit
        return np.argmax(self.Q[self.state[0],self.state[1]]) #return the best action inside the Q_table for that state

    def stepReward(self, x,v,lastState): #reward for a given action
        # if x == lastState[0] and v == lastState[1]: 
        #     return FDPPENALTY 
        delta = Agent.calculerCollision(x,v)
        if self.fired:
            if delta< HITBOXWIDTH:
                #print('HIT!')
                return GOAL_REWARD
            else:
                return MISS_PENALITY
        else:
            return DELTADECAY*-delta

    #openAi-like function for making tehe agent act and then observing the next state after the action,
    #the reward from the action, and wheater the game finished or not
    def step(self, action, lastState):
        #Sample an action according to epsilon-greedy method
        self.actionSpace[action]() #execute the according action
        newState = self.state
        finished = self.turnsLeft <= 0
        reward = self.stepReward(newState[0],newState[1], lastState)
        self.fired = False #in case the tank fired in the last step

        return newState, reward, finished

    def save(self, path): #function for saving the Q table into a file at path 
        np.save(path, self.Q)
    
    def load(self, path): #function for loading a Q table from a file
        self.Q = np.load(path)

    def learn(self): #plays the game in a simulated environment and (hopefully) learns the Q table
        
        logevery = 1000 #number of iterations before printing the number of operations done


        for nb_iteration in range(self.iterations):
            
            if nb_iteration % logevery == 0:
                print(f"Learning... {nb_iteration} out of {self.iterations} iterations")
                logevery *= 2

            state = self.initialState

            lastState = [state[0]-1, state[1]]

            finished = False 
            
            #sample an action from the action space 
            action = self.sampleAction()

            while(not finished): # play the game to the end 

                next_state , reward, finished = self.step(action, lastState)
                                
                if finished:
                    self.Q[state[0], state[1], action] = (1 - self.LearningRate) * self.Q[state[0], state[1], action] + self.LearningRate* reward
                    break
                
                next_action = self.sampleAction()

                #update Q_table with bellman function
                self.Q[state[0], state[1], action] = (1 - self.LearningRate) * self.Q[state[0], state[1], action] + self.LearningRate* (reward + self.gamma * self.Q[next_state[0],next_state[1],next_action] )

                #now the current state is state and the current action is action
                lastState = state
                state = next_state
                action = next_action


            #when we get here the game is finished, so we reset it to play again!
            self.reset()

    def play(self): #Play the game using the Q table 
        
        #choose best action inside the Q table
        action =  np.argmax(self.Q[self.state[0], self.state[1]])
        
        #take that action
        self.actionSpace[action]()  

        self.fired = False

        print("Action values:",self.Q[self.state[0], self.state[1]])
        print(f"Action: {Agent.action_toString(action)}, state: {self.state}")

        return action #I think I will use this to play the game

if __name__ == "__main__":

    bunda = Agent()
    bunda.learn()

    print(bunda.Q)

    bunda.save(".\Q_table")
