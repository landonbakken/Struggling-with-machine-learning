import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim

import random
from collections import deque

class TicTacToe:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.done = False
        self.winner = None
        self.current_player = 1
        return self.board.flatten()

    def step(self, action):
        row, col = divmod(action, 3)
        if self.board[row, col] != 0 or self.done:
            return self.board.flatten(), -10, self.done, {}
        
        self.board[row, col] = self.current_player
        reward, self.done, self.winner = self._check_winner()
        self.current_player = 3 - self.current_player  # Switch player
        return self.board.flatten(), reward, self.done, {}

    def _check_winner(self):
        for i in range(3):
            if np.all(self.board[i, :] == self.current_player) or np.all(self.board[:, i] == self.current_player):
                return 10, True, self.current_player
        if self.board[0, 0] == self.board[1, 1] == self.board[2, 2] == self.current_player or \
			self.board[0, 2] == self.board[1, 1] == self.board[2, 0] == self.current_player:
            return 10, True, self.current_player
        if np.all(self.board != 0):
            return 0, True, None  # Draw
        return 0, False, None

    def render(self):
        print(self.board)

class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(9, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 9)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

def train_dqn():
    env = TicTacToe()
    model = DQN()
    target_model = DQN()
    target_model.load_state_dict(model.state_dict())
    target_model.eval()
    
    optimizer = optim.Adam(model.parameters())
    criterion = nn.MSELoss()

    replay_buffer = deque(maxlen=10000)
    batch_size = 64
    gamma = 0.99
    epsilon = 1.0
    epsilon_decay = 0.995
    epsilon_min = 0.1
    target_update = 10
    num_episodes = 1000

    for episode in range(num_episodes):
        state = env.reset()
        done = False
        loss = None
        while not done:
            if random.random() < epsilon:
                action = random.choice([i for i in range(9) if state[i] == 0])
            else:
                with torch.no_grad():
                    q_values = model(torch.FloatTensor(state))
                action = torch.argmax(q_values).item()
                if state[action] != 0:
                    action = random.choice([i for i in range(9) if state[i] == 0])

            next_state, reward, done, _ = env.step(action)
            replay_buffer.append((state, action, reward, next_state, done))
            state = next_state

            if len(replay_buffer) > batch_size:
                batch = random.sample(replay_buffer, batch_size)
                states, actions, rewards, next_states, dones = zip(*batch)

                states = torch.FloatTensor(states)
                actions = torch.LongTensor(actions)
                rewards = torch.FloatTensor(rewards)
                next_states = torch.FloatTensor(next_states)
                dones = torch.FloatTensor(dones)

                q_values = model(states).gather(1, actions.unsqueeze(1)).squeeze(1)
                next_q_values = target_model(next_states).max(1)[0]
                expected_q_values = rewards + gamma * next_q_values * (1 - dones)

                loss = criterion(q_values, expected_q_values)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        if epsilon > epsilon_min:
            epsilon *= epsilon_decay

        if episode % target_update == 0:
            target_model.load_state_dict(model.state_dict())
        
        if loss != None:
            print(f"Episode {episode+1}/{num_episodes}, Loss: {loss.item()}, Epsilon: {epsilon:.3f}")

train_dqn()
