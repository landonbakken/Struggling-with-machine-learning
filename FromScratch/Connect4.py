import numpy as np
import pygame
import tkinter as tk

from SimpleModel import *
from ModelVisualizer import *
from MathThings import *

class Game:
	def __init__(self, firstTurn = 1):
		#create the board
		self.WIDTH = 700
		self.HEIGHT = 600
		self.peiceRadius = 45
		self.peiceColors = [(200, 50, 50), (50, 200, 50)]
		self.backgroundColor = (0, 0, 0)
		self.firstTurn = firstTurn

		self.restart()

		#create screen
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		pygame.display.set_caption("Model Visualizer")

	def restart(self):
		self.turn = self.firstTurn
		self.board = np.zeros((7, 6))

	def draw(self):
		# Clear the screen
		self.screen.fill(self.backgroundColor)

		for x in range(self.board.shape[0]):
			for y in range(self.board.shape[1]):
				#get peice color
				peice = self.board[x, y]
				if peice == 0:
					color = (100, 100, 100)
				else:
					colorIndex = int((peice + 1)/2)
					color = self.peiceColors[colorIndex]

				#draw the peice
				pygame.draw.circle(self.screen, color, (x * 100 + 50, y * 100 + 50), self.peiceRadius)

	def update(self):
		#draw things
		self.draw()

		#show drawings
		pygame.display.flip()

	def place(self, x):
		#get column
		column = self.board[x]

		#get new peice position
		if np.any(column != 0):
			y = np.argmax(column != 0)
		else:
			y = len(column)
		if y == 0:
			return 0, False
		y -= 1

		#place peice
		self.board[x, y] = self.turn

		#check if there was a win
		state = self.checkState(x, y)

		#switch turn
		self.turn = -self.turn

		return state, True

	#checks if the game is over
	#modCol and modRow is the last modified peice position
	def checkState(self, modCol, modRow):
		target = self.board[modCol, modRow]
		
		#horizontal
		if self.stepPeices(modCol, modRow, 1, 0, target) + self.stepPeices(modCol, modRow, -1, 0, target) + 1 >= 4:
			return target
		
		#vertical
		if self.stepPeices(modCol, modRow, 0, 1, target) + self.stepPeices(modCol, modRow, 0, -1, target) + 1 >= 4:
			return target
		
		#negative diagonal
		if self.stepPeices(modCol, modRow, 1, 1, target) + self.stepPeices(modCol, modRow, -1, -1, target) + 1 >= 4:
			return target
		
		#positive diagonal
		if self.stepPeices(modCol, modRow, -1, 1, target) + self.stepPeices(modCol, modRow, 1, -1, target) + 1 >= 4:
			return target
		
		return 0

	def stepPeices(self, x, y, xStep, yStep, target):
		#step
		x += xStep
		y += yStep

		#check bounds
		if x >= self.board.shape[0] or x < 0 or y >= self.board.shape[1] or y < 0:
			return 0
		
		#keep going if it's the same
		if self.board[x, y] == target:
			return self.stepPeices(x, y, xStep, yStep, target) + 1
		
		return 0
	
allowedToStep = False
def step():
	global allowedToStep

	allowedToStep = True

dimentions = [42, 2, 7]

#create model
model_1 = Model(dimentions, costFunction, leakyReluFunction, sigmoidFunction)
model_2 = Model(dimentions, costFunction, leakyReluFunction, sigmoidFunction)

#create visualizer
pygame.init()
#visualizer = ModelVisualizer(model_1)

#controls window
root = tk.Tk()
root.title("Controls and info")
button1 = tk.Button(root, text="Step", command=step)
button1.pack(pady=20)
		

game = Game(firstTurn=-1)
while True:
	#check events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	#update controls window
	root.update_idletasks()
	root.update()

	#visualizer.update()

	if True:#allowedToStep:
		#get the model's placement
		boardState = game.board.flatten()
		if game.turn == 1:
			outputs = model_1.calculate(boardState)
		elif game.turn == -1:
			outputs = model_2.calculate(boardState)

		valid = False
		while not valid:
			#place and update
			position = np.argmax(outputs) #gets the index of the max value
			outputs[position] = -1
			winState, valid = game.place(position)
		game.update()

		if winState != 0:
			game.restart()

		allowedToStep = False