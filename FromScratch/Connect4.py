import numpy as np
import pygame
import tkinter as tk
import time
import statistics

from SimpleModel import *
from ModelVisualizer import *
from MathThings import *
from Memory import *

class Game:
	def __init__(self, screen):
		#create the board
		self.WIDTH = 700
		self.HEIGHT = 600
		self.peiceRadius = 45
		self.peiceColors = [(200, 50, 50), (50, 200, 50)]
		self.backgroundColor = (0, 0, 0)
		self.screen = screen

		self.restart()

	def restart(self):
		self.turn = np.random.choice([-1, 1])
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
		y -= 1
		
		#not a valid place (column is full)
		if y == -1:
			return 0, False, fitness_invalid
		
		#place peice
		self.board[x, y] = self.turn

		fitnessOffset = 0
		fitnessOffset += self.defensiveReward(x, y, self.turn)
		fitnessOffset += self.offensiveReward(x, y, self.turn)

		#check if there was a win
		state = self.checkState(x, y, self.turn)

		return state, True, fitnessOffset
	
	def defensiveReward(self, x, y, player):
		reward = 0

		#blocks
		hypotheticalWinState = self.checkState(x, y, -player) #see what would have happened if the other player played there
		if hypotheticalWinState == -player:
			reward += fitness_block

		return reward
	
	def offensiveReward(self, x, y, player):
		reward = 0
		#double 3 in a row
		#line peices up
		return reward

	#checks if the game is over
	#modCol and modRow is the last modified peice position
	def checkState(self, modCol, modRow, target):
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
		
		#draw
		if not np.any(self.board == 0):
			return -2
		
		#nothing (no win, no draw)
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
	
#a model that returns random values
class RandomModel:
	def __init__(self):
		self.fitness = 0 #not used for anything, just so there aren't errors
	def calculate(self, boardState):
		return np.random.random(7)
	
def playGame(game, model_1, model_2, slow = False):
	game.restart()
	winState = 0
	while winState == 0:
		#flip who's turn it is (at the start so things are more simple)
		game.turn = -game.turn

		#get the game state
		boardState = game.board.flatten()
		boardState *= game.turn #flip the peices if its player -1 turn (-1 is always the opponent in the neural model)
		columnState = np.abs(game.board[:, 0])
		gameState = np.concatenate((boardState, columnState))

		#get model's choice
		if game.turn == 1:
			outputs = model_1.calculate(gameState)
		elif game.turn == -1:
			outputs = model_2.calculate(gameState)

		#place and update
		valid = False
		while not valid:
			#get the index of the max value (move with the highest percent)
			position = np.argmax(outputs)

			#remove it from the options (without moving them around)
			outputs[position] = np.min(outputs) - 1

			#place peice
			winState, valid, fitnessEffect = game.place(position)

			#change how good a move is
			if game.turn == 1:
				model_1.fitness += fitnessEffect
			elif game.turn == -1:
				model_2.fitness += fitnessEffect
		
		#valid move
		if game.turn == 1:
			model_1.fitness += fitness_valid
		elif game.turn == -1:
			model_2.fitness += fitness_valid

		if slow:
			game.update()
			time.sleep(.5)

	#tie
	if winState == -2:
		model_1.fitness += fitness_tie
		model_2.fitness += fitness_tie
	#win/lost
	else:
		if winState == 1:
			model_1.fitness += fitness_win
			model_2.fitness += fitness_loss
		elif winState == -1:
			model_1.fitness += fitness_loss
			model_2.fitness += fitness_win

def offsetArrayNormalized(initialArray, offsetAmount, percentToOffset):
	# Number of elements to modify (10% of the total number of elements)
	num_elements_to_modify = int(initialArray.size * percentToOffset)

	# Randomly select indices to modify
	indices = np.unravel_index(np.random.choice(initialArray.size, num_elements_to_modify, replace=False), initialArray.shape)

	# Generate random offsets from a normal distribution
	offsets = np.random.normal(loc=0, scale=offsetAmount, size=num_elements_to_modify)

	# Apply the offsets to the selected indices
	initialArray[indices] += offsets

def offsetArray(initialArray, offsetAmount, percentToOffset):
	# Number of elements to modify
	num_elements_to_modify = int(initialArray.size * percentToOffset)

	# Get indices of the array's elements
	indices = np.unravel_index(np.random.choice(initialArray.size, num_elements_to_modify, replace=False), initialArray.shape)

	# Set the selected elements to random values
	initialArray[indices] += np.random.uniform(-offsetAmount, offsetAmount, num_elements_to_modify)

def replaceArray(initialArray, randomRange, percentToReplace):
	# Number of elements to modify
	num_elements_to_modify = int(initialArray.size * percentToReplace)

	# Get indices of the array's elements
	indices = np.unravel_index(np.random.choice(initialArray.size, num_elements_to_modify, replace=False), initialArray.shape)

	# Set the selected elements to random values
	initialArray[indices] = np.random.uniform(randomRange[0], randomRange[1], num_elements_to_modify)

def makeChildren(parent, children):
	weights, biases = parent.getValues()
	for child in children:
		
		newWeights = weights.copy()
		newBiases = biases.copy()

		#biases
		for weightsIndex in range(newWeights.shape[0]):
			offsetArrayNormalized(newWeights[weightsIndex], offsetAmount, offsetPercent)
			replaceArray(newWeights[weightsIndex], replacedRange, replacedPercent)

		#biases
		for biasesIndex in range(newBiases.shape[0]):
			offsetArrayNormalized(newBiases[biasesIndex], offsetAmount, offsetPercent)
			replaceArray(newBiases[biasesIndex], replacedRange, replacedPercent)
		
		child.setValues(newWeights, newBiases)
		child.age = 0
		child.generation = parent.generation + 1
"""
Input:
42 for board state (6x7)
	can have -1 for opponent, 1 for you
7 for if the column is filled
	0 for not filled, 1 for filled

Hidden:
128 first
64 second
leaky ReLU

Output:
7 for each possible placement
	uses softmax to get highest
	if it isnt open, penalize then move to next highest
"""
dimentions = [49, 128, 64, 7] #the dimentions of the models

childrenPerParent = 19 #how many models are gotten from each parent
numParents = 8 #the amount of models kept
randomModels = 0#1 #usually just slows down the start
gamesPerGenerationPerModel = 13 #the games that each model plays per generation
minFitness = -10 #how low a model's fitness has to go to just forfiet the rest of the matches

#rewards/punishments
fitness_invalid = -.2 #if there is an invalid move
fitness_valid = 0#.1 #if there is a valid move
fitness_tie = -.2
fitness_loss = -1
fitness_win = 1.5
fitness_block = .5

offsetAmount = .05 #a random range from -offsetAmount to -offsetAmount
offsetPercent =	.005 #percentage of weights/biases that are offset for each child
replacedPercent = .0015 #percentage of weights/biases that are replaced for each child
replacedRange = (-1, 1) #the random range that weights are set to

#memory paths
memoryFile = memoryPath + "memory.pickle"

#create model
populationSize = numParents * childrenPerParent + numParents + randomModels
population = np.empty(populationSize, dtype=Model)
for i in range(populationSize):
	newModel = Model(dimentions, costFunction, leakyReluFunction, softmax)
	population[i] = newModel
	population[i].randomizeValues()
	population[i].generation = 0
	population[i].age = 0

#button vars
watchNextGame = False
saveMem = False
loadMem = False

#create visualizer
pygame.init()
visualizer = ModelVisualizer(population[0], windowHeight=800, windowWidth=1700, nodeRadius=6, connectionWidth=2, outlines=False)

#controls window
root = tk.Tk()
root.title("Controls and info")
button1 = tk.Button(root, text="Watch Game", command=lambda: exec("global watchNextGame; watchNextGame = True"))
button1.pack(pady=10)
button1 = tk.Button(root, text="Save Memory", command=lambda: exec("global saveMem; saveMem = True"))
button1.pack(pady=10)
button1 = tk.Button(root, text="Load Memory", command=lambda: exec("global loadMem; loadMem = True"))
button1.pack(pady=10)
gamesDone = tk.Label(root, text="Games done: 0/0")
gamesDone.pack(pady=10)
ageLabel = tk.Label(root, text="Oldest Model: 0")
ageLabel.pack(pady=10)
generationLabel = tk.Label(root, text="Most Generations: 0")
generationLabel.pack(pady=10)		
roundsLabel = tk.Label(root, text="Rounds: 0")
roundsLabel.pack(pady=10)		
timeLabel = tk.Label(root, text="Time: 0")
timeLabel.pack(pady=10)		
gamesPerSecondLabel = tk.Label(root, text="Games Per Second: 0")
gamesPerSecondLabel.pack(pady=10)
prematureStopLabel = tk.Label(root, text="Models Abandoned: 0")
prematureStopLabel.pack(pady=10)
averageFitnessLabel = tk.Label(root, text="Avg Fitness: 0")
averageFitnessLabel.pack(pady=10)
bestFitnessLabel = tk.Label(root, text="Best Fitness: 0")
bestFitnessLabel.pack(pady=10)

game = Game(visualizer.screen)
trainingStartTime = time.time()
gamesPerSecond = 0
totalRounds = 0
abandoned = 0
randomModel = RandomModel()
while True:
	startTime = time.time()

	#check events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	#reset fitness
	for model in population:
		model.fitness = 0

	#play matches
	for modelIndex, model in enumerate(population):
		
		#get opponents
		opponents = np.random.choice(population, gamesPerGenerationPerModel, replace=False)

		for opponent in opponents:
			#play each match per opponent
			playGame(game, model, opponent)

			if model.fitness < minFitness:
				abandoned += 1
				break

		#update GUI
		gamesDone.config(text=f"Games Done: {(modelIndex + 1) * gamesPerGenerationPerModel}/{(populationSize * gamesPerGenerationPerModel)}")
		root.update()
	totalRounds += 1

	#sort by fitness
	population = np.array(sorted(population, key=lambda model: model.fitness, reverse=True))

	if saveMem:
		saveMem = False
		saveModels(memoryFile, population[0:numParents])
		print("Saved memory to files")

	if loadMem:
		loadMem = False
		loadModels(memoryFile, population[0:numParents])
		print("Loaded memory from files")

	#create children
	for modelIndex in range(numParents):
		parent = population[modelIndex]
		parent.age += 1
		startIndex = modelIndex * childrenPerParent + numParents #start after the parents
		children = population[startIndex:startIndex + childrenPerParent] #8 children per top model in the top 10
		makeChildren(parent, children)
	
	#create new
	for modelIndex in range(numParents * (childrenPerParent + 1), populationSize):
		population[modelIndex].randomizeValues()
		population[modelIndex].generation = 0
		population[modelIndex].age = 0

	visualizer.update(population[0])

	gamesPerSecond = (gamesPerSecond + (populationSize * gamesPerGenerationPerModel)/(time.time() - startTime))/2
	gamesPerSecondLabel.config(text=f"Games Per Second: {int(gamesPerSecond)}")
	roundsLabel.config(text=f"Generations: {totalRounds}")
	timeLabel.config(text=f"Time (seconds): {int(time.time() - trainingStartTime)}")
	
	maxAge = max(model.age for model in population)
	ageLabel.config(text=f"Oldest Model: {maxAge}")
	maxGeneration = max(model.generation for model in population)
	generationLabel.config(text=f"Oldest Strand: {maxGeneration}")

	averageFitness_mean = statistics.median(model.fitness for model in population)
	averageFitness_median = statistics.mean(model.fitness for model in population)
	averageFitnessLabel.config(text=f"Fitness: Mean: {int(averageFitness_mean):.5g}, Median: {int(averageFitness_median):.5g}")

	bestFitnessLabel.config(text=f"Max Fitness: {int(population[0].fitness):.5g}")

	prematureStopLabel.config(text=f"Models Abandoned this round: {abandoned}")
	abandoned = 0

	if watchNextGame:
		watchNextGame = False
		playGame(game, population[0], population[1], slow=True) #top two play