import numpy as np
import pygame
import tkinter as tk
import time
import statistics

from SimpleModel import *
from ModelVisualizer import *
from MathThings import *
from Memory import *

inline_range = 50
fitness_inline = 0#2 #per tick
fitness_passed = 1 #pass gap
fitness_time = 0#.1 #per tick
fitness_death = 0#-5

gravity = -2
jumpVel = 20

#child creation
offsetAmount = .05 #a random range from -offsetAmount to -offsetAmount
offsetPercent =	.05 #percentage of weights/biases that are offset for each child
replacedPercent = .02 #percentage of weights/biases that are replaced for each child
scaleRange = (1, .1) #difference children have different scales of replace and offset percents
replacedRange = (-1, 1) #the random range that weights are set to

"""
inputs:
distance to wall
height #difference between player and center of wall gap
vertical velocity of player

outputs:
jump
don't jump

rewards:
+ passed wall 
+ inline with wall gap
+ time
- death
"""

class Game:
	def __init__(self, screen, players, width=800, height=1200):
		#screen
		self.WIDTH = width
		self.HEIGHT = height
		self.backgroundColor = (0, 0, 0)
		self.screen = screen
		
		#players
		self.playerX = self.WIDTH * 1/4
		self.playerRadius = 10
		self.players = players
		
		#obsticles
		self.gapYPos = self.HEIGHT/2
		self.gapXPos = self.WIDTH
		self.gapMargin = 200 #the distance from top or bottom
		self.gapWidth = 50
		self.gapHeight = 150
		self.gapXVel = -15
		
		#trackers
		self.running = True
		self.deaths = 0
		self.numPlayers = len(self.players)

		#set player variables
		for player in self.players:
			player.yPos = self.HEIGHT/2 #middle
			player.yVel = 0
			player.alive = True

		self.timeResolution = .8 #this is just a simple way to scale accel and velocity, effectivle gives more resolution to the players

	def draw(self):
		global onlyDrawBest

		# Clear the screen
		self.screen.fill(self.backgroundColor)

		#draw players
		for player in self.players:
			if player.alive:
				pygame.draw.circle(self.screen, player.color, (self.playerX, player.yPos), self.playerRadius)
				if onlyDrawBest:
					break

		#gap indicator
		pygame.draw.circle(self.screen, (255, 0, 0), (self.gapXPos, self.gapYPos), 3)
		
		#lower
		pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.gapXPos - self.gapWidth/2, self.gapYPos + self.gapHeight/2, self.gapWidth, self.HEIGHT - self.gapYPos - self.gapHeight/2))
		#upper
		pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.gapXPos - self.gapWidth/2, 0, self.gapWidth, self.gapYPos - self.gapHeight/2))

		#show drawings
		pygame.display.flip()

	def getWallDistance(self):
		return max(self.gapYPos - self.playerX, 0)
	
	def getState(self, player):
		normalizedDistance = self.getWallDistance()/self.WIDTH
		normalizedDifference = (self.gapYPos - player.yPos)/self.HEIGHT
		normalizedHeight = player.yPos/self.HEIGHT
		reducedVelocity = player.yVel/100
		return np.array([normalizedDistance, normalizedDifference, normalizedHeight, reducedVelocity])

	def update(self):
		#change gap
		self.gapXPos += self.gapXVel * self.timeResolution
		if self.gapXPos <= -self.gapWidth/2:
			self.gapYPos = random.randrange(self.gapMargin, self.HEIGHT - self.gapMargin)
			self.gapXPos = self.WIDTH
			
			for player in self.players:
				if player.alive:
					player.fitness += fitness_passed

		#player input
		for player in self.players:
			if player.alive:
				player.fitness += fitness_time

				#gap closenes reward
				if abs(self.gapYPos - player.yPos) < inline_range:
					player.fitness += fitness_inline * ((inline_range - abs(self.gapYPos - player.yPos))/inline_range)**2

				state = self.getState(player)
				jump = player.calculate(state)

				#gravity
				player.yVel += gravity * self.timeResolution

				#jump
				if jump[0] > jump[1]:
					player.yVel = max(player.yVel, 0)
					player.yVel += jumpVel

				#move players (inverted vel)
				player.yPos -= player.yVel * self.timeResolution

				#check if player is still alive
				outOfBounds = player.yPos > self.HEIGHT - self.playerRadius or player.yPos < self.playerRadius
				insideGap = abs(self.gapXPos - self.playerX) < self.playerRadius + self.gapWidth/2
				hitting = abs(self.gapYPos - player.yPos) > self.gapHeight/2 - self.playerRadius/2
				if outOfBounds or (insideGap and hitting):
					player.alive = False
					player.fitness += fitness_death

					self.deaths += 1
					if self.deaths == self.numPlayers:
						self.running = False

#memory paths
memoryFile = memoryPath + "flappyBird.pickle"

#create model
dimentions = [4, 8, 5, 2]
numParents = 10
numChildrenPerParent = 10
numRandomModels = 7
populationSize = numParents + numParents * numChildrenPerParent + numRandomModels
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
onlyDrawBest = True

#create visualizer
pygame.init()
visualizer = ModelVisualizer(population[0], windowHeight=800, windowWidth=650, nodeRadius=6, connectionWidth=2, outlines=False)

#controls window
root = tk.Tk()
root.title("Controls and info")
button1 = tk.Button(root, text="Save Memory", command=lambda: exec("global saveMem; saveMem = True"))
button1.pack(pady=10)
button2 = tk.Button(root, text="Load Memory", command=lambda: exec("global loadMem; loadMem = True"))
button2.pack(pady=10)
button3 = tk.Button(root, text="Toggle Slow", command=lambda: exec("global slowRound; slowRound = not slowRound"))
button3.pack(pady=10)
button4 = tk.Button(root, text="Toggle Model View", command=lambda: exec("global modelView; modelView = not modelView"))
button4.pack(pady=10)
button4 = tk.Button(root, text="Toggle Tick Limit", command=lambda: exec("global noTickLimit; noTickLimit = not noTickLimit"))
button4.pack(pady=10)
button4 = tk.Button(root, text="Toggle Only Draw Best", command=lambda: exec("global onlyDrawBest; onlyDrawBest = not onlyDrawBest"))
button4.pack(pady=10)
ageLabel = tk.Label(root, text="Oldest Model: 0")
ageLabel.pack(pady=10)
generationLabel = tk.Label(root, text="Most Generations: 0")
generationLabel.pack(pady=10)
timeLabel = tk.Label(root, text="Time: 0")
timeLabel.pack(pady=10)
averageFitnessLabel = tk.Label(root, text="Avg Fitness: 0")
averageFitnessLabel.pack(pady=10)
bestFitnessLabel = tk.Label(root, text="Best Fitness: 0")
bestFitnessLabel.pack(pady=10)

trainingStartTime = time.time()
gamesPerSecond = 0
totalRounds = 0
abandoned = 0
slowRound = False
modelView = False
noTickLimit = True
while True:
	startTime = time.time()

	#check events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	#reset fitness
	for model in population:
		model.fitness = 0

	#play game
	game = Game(visualizer.screen, population, visualizer.WIDTH, visualizer.HEIGHT)
	ticks = 0
	while game.running and (ticks < 400 or noTickLimit):
		tickStartTime = time.time()

		#tick
		game.update()
		ticks += 1
		
		#draw players
		if not modelView:
			game.draw()
		
		#show round as slow (only if in gameView)
		if slowRound and not modelView:
			time.sleep(max(.05 - (time.time() - tickStartTime), .001))
		
		#update GUI
		root.update()
		

	#sort by fitness
	population = np.array(sorted(population, key=lambda model: model.fitness, reverse=True))

	#show model
	if modelView:
		visualizer.update(population[0])

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
		startIndex = modelIndex * numChildrenPerParent + numParents #start after the parents
		children = population[startIndex:startIndex + numChildrenPerParent] #8 children per top model in the top 10
		makeChildren(parent, children, offsetAmount, offsetPercent, replacedRange, replacedPercent, scaleRange)
	
	#create new randoms
	for modelIndex in range(numParents + numParents * numChildrenPerParent, populationSize):
		population[modelIndex].randomizeValues()
		population[modelIndex].generation = 0
		population[modelIndex].age = 0

	
	maxAge = max(model.age for model in population)
	ageLabel.config(text=f"Oldest Model: {maxAge}")
	maxGeneration = max(model.generation for model in population)
	generationLabel.config(text=f"Oldest Strand: {maxGeneration}")
	timeLabel.config(text=f"Time: {time.time() - trainingStartTime:.1f} (Secs)")

	averageFitness_mean = statistics.median(model.fitness for model in population)
	averageFitness_median = statistics.mean(model.fitness for model in population)
	averageFitnessLabel.config(text=f"Fitness: Mean: {int(averageFitness_mean):.5g}, Median: {int(averageFitness_median):.5g}")

	bestFitnessLabel.config(text=f"Max Fitness: {int(population[0].fitness):.5g}")
	abandoned = 0