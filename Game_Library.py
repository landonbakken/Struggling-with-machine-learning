import numpy as np
import random

# Define the Tic-Tac-Toe board
class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.reset()

    def reset(self):
        self.board.fill(0)
        self.current_player = 1#random.randint(1, 2)

    def available_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def get_state(self):
        return str(self.board.reshape(9))

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
    
    def human_game(self, agent):
        playAgain = True
        while playAgain:
            print("Welcome to Tic-Tac-Toe against the Q-learning Agent!")
            print("You are playing as 'O'. Enter your moves in the format 'row,col'. For example, '1,2' for the second row and third column.")

            self.reset()
            state = self.get_state()
            human_player = random.randint(1, 2)
            while True:
                # Print the current board state
                print(self.board,"\n")

                # Human player's turn
                if self.current_player == human_player:
                    while True:
                        try:
                            move = input("Enter your move (row,col): ")
                            row, col = map(int, move.split(','))
                            if (row, col) in self.available_moves():
                                break
                            else:
                                print("Invalid move. Try again.")
                        except ValueError:
                            print("Invalid input format. Please enter row,col (e.g., '1,2').")

                    self.make_move(row, col)
                    state = self.get_state()
                else:
                    # Agent's turn
                    available_moves = self.available_moves()
                    action = agent.choose_action(state, available_moves)
                    self.make_move(*action)
                    state = self.get_state()

                winner = self.check_winner()
                if winner is not None:
                    print(self.board)
                    if winner == 1:
                        print("Agent wins!")
                    elif winner == 2:
                        print("Human wins!")
                    else:
                        print("It's a draw!")
                    break


            print("Game Over!")
            playAgain = input("y to play again") == "y"
    
'''
class ConnectFour:
    
    board layout (columns, rows) (x, y) from top left
    0
    1
    2
    3
    4
    5
        0  1  2  3  4  5  6 
    
    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.nextPlace = np.zeros(7, dtype=int)
        self.reset()

    def reset(self):
        self.board.fill(0)
        self.current_player = random.randint(1, 2)
        self.nextPlace.fill(5) #all of the 5th rows are open

    def available_moves(self):
        #returns all columnds that dont have a peice in the top row
        return [column for column in range(7) if self.board[column, 0] == 0]

    def make_move(self, col):
        if self.board[col, 0] == 0:
            self.board[col, row] = self.current_player
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
        
'''