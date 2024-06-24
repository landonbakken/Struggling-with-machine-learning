import numpy as np
import random
import matplotlib.pyplot as plt
import time
from Game_Library import TicTacToe as Environment
import math

episodes = 1000000
graphStep = 10000

#agent settings
#exploration
targetEndExploration = 0.001
startExploration = 0.9 #because if it's higher, it doesnt really learn anything, and just wastes time

#rewards
rewards_draw = 0
rewards_win = 1
rewards_lose = -1

usePlotter = True

class RealTimePlotter:
    def __init__(self, title="Change Over Time", xlabel="Time", ylabel="Value"):
        self.fig, self.ax = plt.subplots()
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.values = []
        self.line, = self.ax.plot([], [], marker='o', linestyle='-', color='b')
        
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.grid(True)
        plt.ion()  # Turn on interactive mode
        
    def add_value(self, value):
        self.values.append(value)
        self.update()

    def update(self):
        self.line.set_data(range(len(self.values)), self.values)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def show(self):
        plt.show()

# Define the Q-learning agent
class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.9999):
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay

    def get_q_values(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(9)
        return self.q_table[state]

    def choose_action(self, state, available_moves):
        if random.random() < self.exploration_rate:
            return random.choice(available_moves)
        q_values = self.get_q_values(state)
        return available_moves[np.argmax([q_values[i*3 + j] for i, j in available_moves])]

    def update_q_table(self, state, action, reward, next_state):
        q_values = self.get_q_values(state)
        max_future_q = max(self.get_q_values(next_state))
        q_values[action[0]*3 + action[1]] += self.learning_rate * (reward + self.discount_factor * max_future_q - q_values[action[0]*3 + action[1]])

    def decay_exploration(self):
        self.exploration_rate *= self.exploration_decay
        #print(self.exploration_rate)

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

    winCounter = 0
    for episode in range(episodes):
        if episode%graphStep == 0 and episode != 0:
            #plot win percent
            winPercent = winCounter/graphStep * 100#test_agent(agent, graphStep, game)
            winCounter = 0
            if usePlotter:
                plotter.add_value(winPercent)
                plotter.update()
            else:
                print(f"Win percent: {winPercent}")
            print(f"Exploration rate: {agent.exploration_rate}")
        
        #start game
        game.reset()
        
        state = game.get_state()
        
        rewarded_player = random.randint(1, 2)
        while True:
            # choose move
            available_moves = game.available_moves()
            if game.current_player == rewarded_player:
                action = agent.choose_action(state, available_moves)
            else:
                action = random.choice(available_moves)
            
            #make move
            game.make_move(*action)
            
            #update state
            next_state = game.get_state()

            #checks if there is a win
            winner = game.check_winner()
            if winner is not None:
                if winner == rewarded_player: #win
                    reward = rewards_win
                    winCounter += 1
                    agent.update_q_table(state, action, reward, next_state)
                elif winner == 3 - rewarded_player: #loss
                    reward = rewards_lose
                else: #draw
                    reward = rewards_draw
                #reward agent and end game
                break
            
            #log actionn if rewarded player did it
            if game.current_player != rewarded_player:
                agent.update_q_table(state, action, -.1, next_state)
            #update state
            state = next_state
        #make it explore less
        agent.decay_exploration()
    #return trained agent
    return agent

# Main script
startTime = time.time()
trained_agent = train_agent(episodes, graphStep, Environment())
#winrate = test_agent(trained_agent, 100, Environment())
print(f"{round(time.time() - startTime)} seconds for {episodes} episodes")# with {winrate} winrate")

#let human play:
game = Environment()
game.human_game(trained_agent)