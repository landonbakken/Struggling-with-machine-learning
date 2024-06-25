import numpy as np
import random
import matplotlib.pyplot as plt
import time
from Game_Library import TicTacToe as Environment
import math

episodes = 100000
graphStep =100

#agent settings
#exploration
targetEndExploration = 0.001
startExploration = 1

#rewards
rewards_draw = -.5
rewards_win = 1#1
rewards_lose = -1

usePlotter = True

class RealTimePlotter:
    def __init__(self, title, xlabel, ylabel):
        self.fig, self.ax = plt.subplots()
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        
        self.lines = []
        self.labels = []
        
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        
        plt.grid(True)
        plt.ion()  # Turn on interactive mode
        
    def add_line(self, label, color, y=[]):
        line, = self.ax.plot(range(len(y)), y, color=color, label=label)
        self.lines.append(line)
        self.labels.append(label)
        
    def add_value(self, value, label):
        index = self.labels.index(label)
        line = self.lines[index]
        
        y_data = list(line.get_ydata())
        
        y_data.append(value)
        
        line.set_xdata(range(len(y_data)))
        line.set_ydata(y_data)
        
        self.update()

    def update(self):
        self.ax.legend()
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def show(self):
        plt.show()

# Define the Q-learning agent
class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.9999, noise = 0.1):
        self.q_table = {} #Q values for every state-action pair (?)
        self.learning_rate = learning_rate #how fast new information overrides old info (?)
        self.discount_factor = discount_factor #Determines the importance of future rewards (?)
        self.exploration_rate = exploration_rate #how random it is when choosing a move
        self.exploration_decay = exploration_decay #how fast the exploration decays over time to hone in 
        self.noise = noise

    def get_q_values(self, state):
        #add a Q value if not in dictionary
        if state not in self.q_table:
            self.q_table[state] = np.random.randn(9) * self.noise #for tic tac toe
            #self.q_table[state] = np.random.randn(7) * self.noise #for connect 4
        
        #return the Q value that matches the state
        return self.q_table[state]

    def choose_action(self, state, available_moves):
        #add randomness so it can improve
        if random.random() < self.exploration_rate:
            return random.choice(available_moves)
        
        #gets Q values for the current state
        q_values = self.get_q_values(state)
        
        #returns move with highest Q value
        #max(available_moves, key=lambda col: q_values[col]) #for connect 4
        return available_moves[np.argmax([q_values[i*3 + j] for i, j in available_moves])] #for tictactoe

    def update_q_table(self, state, action, reward, next_state):
        #get the Q values for the current state 
        q_values = self.get_q_values(state)
        
        #get maximum q value for the next state
        max_future_q = max(self.get_q_values(next_state))
        
        '''
        Q-learning forumla: 
        
        Mathmatically:
        s = State
        s' = Next state
        A = Action
        A' = Next action
        a = Learning rate (normally alpha)
        r = Reward
        y = Discount factor
        
        Q(s, a) = Q(s, a) + a * (r + y * max(Q(s', a')) - Q(s, a))
        
        Programmatically:
        q_values[action] += self.learning_rate * (reward + self.discount_factor * max_future_q - q_values[action])
        '''
        
        #q_values[action] += self.learning_rate * (reward + self.discount_factor * max_future_q - q_values[action]) #for connect four
        q_values[action[0]*3 + action[1]] += self.learning_rate * (reward + self.discount_factor * max_future_q - q_values[action[0]*3 + action[1]]) #for tic tac toe

    def decay_exploration(self):
        #reduces exploration rate over time so it won't make as many random moves
        self.exploration_rate *= self.exploration_decay


# Train the agent
def train_agent(episodes, graphStep, game):
    #figure out decay: startExploration * exploration_decay ^ ticks = targetEndExploration
    decay = math.e ** (math.log(targetEndExploration/startExploration)/episodes)
    
    #create agent
    agent = QLearningAgent(exploration_decay=decay, exploration_rate=startExploration)
    
    #initialize plot
    if usePlotter:
        plotter = RealTimePlotter(title="Winrate vs Games played", xlabel=f"Games played (x{graphStep})", ylabel="Winrate (%)")
        plotter.show()

    plotter.add_line("Wins", 'g')
    plotter.add_line("Losses", 'r')
    plotter.add_line("Draws", 'b')
    plotter.add_line("Training Balance", 'k')
    
    balanceCounter = graphStep/2
    
    for episode in range(episodes):
        if episode%graphStep == 0:
            #plot win percent
            winPercent, lossPercent, drawPercent = game.test_agent(agent, 100)
            
            balance = balanceCounter / graphStep * 100
            balanceCounter = 0
            
            if usePlotter:
                plotter.add_value(winPercent, "Wins")
                plotter.add_value(lossPercent, "Losses")
                plotter.add_value(drawPercent, "Draws")
                plotter.add_value(balance, "Training Balance")
        
        #start game
        game.reset()
        
        action = None
        state = None
        while True:
            #get possible moves
            available_moves = game.available_moves()
            
            #store info
            past_action = action
            past_state = state
            
            #choose move
            action = agent.choose_action(state, available_moves)
            
            #make move
            winner = game.make_move(*action)
            
            #update state
            next_state = game.get_state()

            #checks if there is a win
            if winner is not None:
                if winner == 3: #draw
                    agent.update_q_table(past_state, past_action, rewards_draw, state)
                    agent.update_q_table(state, action, rewards_draw, next_state)
                else:
                    agent.update_q_table(state, action, rewards_win, next_state)
                    agent.update_q_table(past_state, past_action, rewards_lose, state)
                    
                    if winner == 1:
                        balanceCounter += 1
                break
            
            #update state
            state = next_state
            
            #log past action
            if past_state != None and past_action != None:
                agent.update_q_table(past_state, past_action, 0, state)
            
        #make it explore less
        agent.decay_exploration()
        
    #return trained agent
    return agent


startTime = time.time()
trained_agent = train_agent(episodes, graphStep, Environment())
print(f"{round(time.time() - startTime)} seconds for {episodes} episodes")

#let human play:
game = Environment()
game.human_game(trained_agent)