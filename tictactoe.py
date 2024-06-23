#this was generated with chatgpt, I am just using it for learning (I will be modifying it)
import numpy as np
import random
import matplotlib.pyplot as plt
import time

episodes = 10000
graphStep = 100

rewards_draw = -1
rewards_win = 1
rewards_lose = -1

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


# Define the Tic-Tac-Toe board
class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1

    def reset(self):
        self.board.fill(0)
        self.current_player = 1

    def available_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def make_move(self, row, col):
        if self.board[row, col] == 0:
            self.board[row, col] = self.current_player
            self.current_player = 3 - self.current_player
            return True
        return False

    def check_winner(self):
        for i in range(3):
            if np.all(self.board[i, :] == self.board[i, 0]) and self.board[i, 0] != 0:
                return self.board[i, 0]
            if np.all(self.board[:, i] == self.board[0, i]) and self.board[0, i] != 0:
                return self.board[0, i]
        if self.board[0, 0] == self.board[1, 1] == self.board[2, 2] != 0:
            return self.board[0, 0]
        if self.board[0, 2] == self.board[1, 1] == self.board[2, 0] != 0:
            return self.board[0, 2]
        if not self.available_moves():
            return 0
        return None

# Define the Q-learning agent
class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995):
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay

    def get_state(self, board):
        return str(board.reshape(9))

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

# Train the agent
def train_agent(episodes, graphStep, game, randOpponentChance):
    agent = QLearningAgent()
    
    #initialize counters
    winsCount = 0
    
    #initialize plot
    plotter = RealTimePlotter(title="Winrate vs Games played", xlabel=f"Games played (x{graphStep})", ylabel="Winrate (%)")
    plotter.show()

    for episode in range(episodes):
        if episode%graphStep == 0 and episode != 0:
            #plot win percent
            plotter.add_value(winsCount/graphStep * 100)
            plotter.update()
            
            #reset counters
            winsCount = 0
        
        game.reset()
        state = agent.get_state(game.board)
        randomOpponent = random.random() < randOpponentChance
        while True:
            available_moves = game.available_moves()

            # Agent's turn
            action = agent.choose_action(state, available_moves)
            game.make_move(*action)
            next_state = agent.get_state(game.board)
            winner = game.check_winner()

            if winner is not None:
                if winner == 1:
                    winsCount += 1
                    reward = rewards_win
                elif winner == 2:
                    reward = rewards_lose
                else:
                    reward = rewards_draw
                agent.update_q_table(state, action, reward, next_state)
                break
            else:
                agent.update_q_table(state, action, 0, next_state)
                state = next_state

            if randomOpponent:
                # Random opponent's turn
                available_moves = game.available_moves()
                action = random.choice(available_moves)
                game.make_move(*action)
                next_state = agent.get_state(game.board)
                winner = game.check_winner()

                if winner is not None:
                    if winner == 1:
                        reward = rewards_lose  # Opposite reward for the agent
                    elif winner == 2:
                        winsCount += 1
                        reward = rewards_win    # Opposite reward for the agent
                    else:
                        reward = rewards_draw
                    agent.update_q_table(state, action, reward, next_state)
                    break
                else:
                    agent.update_q_table(state, action, 0, next_state)
                    state = next_state

        agent.decay_exploration()
    return agent

# Play a game against the trained agent
def play_game(agent):
    game = TicTacToe()
    game.reset()
    state = agent.get_state(game.board)
    while True:
        available_moves = game.available_moves()
        if game.current_player == 1: #q-learning
            action = agent.choose_action(state, available_moves)
        else:
            action = random.choice(available_moves)
        game.make_move(*action)
        state = agent.get_state(game.board)
        winner = game.check_winner()
        if winner is not None:
            return winner

# Main script
if __name__ == "__main__":
    startTime = time.time()
    trained_agent = train_agent(episodes, graphStep, TicTacToe(), .8)
    print(f"{round(time.time() - startTime)} seconds for {episodes} episodes")
    results = {"Agent": 0, "Random": 0, "Draw": 0}
    for _ in range(100):
        result = play_game(trained_agent)
        if result == 1:
            results["Agent"] += 1
        elif result == 2:
            results["Random"] += 1
        else:
            results["Draw"] += 1
    print(results)
