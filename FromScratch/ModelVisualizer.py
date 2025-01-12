from SimpleModel import *
from MathThings import *
import pygame

pygame.init()

class ModelVisualizer:
	def __init__(self, model, windowWidth = 800, windowHeight = 600, nodeRadius = 25, connectionWidth = 5, outlineColor = (100, 100, 100), backgroundColor=(0, 0, 0), minRange = (-1, 1), ax=None):
		self.model = model
		self.WIDTH = windowWidth
		self.HEIGHT = windowHeight
		self.nodeRadius = nodeRadius
		self.connectionWidth = connectionWidth
		self.outlineColor = outlineColor
		self.backgroundColor = backgroundColor
		self.minRange = minRange
		self.ax = ax

		#make flags
		flag = pygame.RESIZABLE if self.ax == None else pygame.HIDDEN

		#create screen
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), flags=flag)
		pygame.display.set_caption("Model Visualizer")

		self.update()

	def drawConnections(self):
		columns = len(self.model.dimentions)
		rows = max([layerOutputs for layerOutputs in self.model.dimentions])

		#first node
		for layerIndex in range(len(self.model.dimentions) - 1):
			layerOutputs_1 = self.model.dimentions[layerIndex]
			layerOutputs_2 = self.model.dimentions[layerIndex + 1]
			layerIndex_2 = layerIndex + 1

			weights = self.model.layers[layerIndex].weights
			maxLayerWeight = max(np.max(weights), abs(np.min(weights)))
			layerWeightRange = (-maxLayerWeight, maxLayerWeight)
			layerWeightRange = maxRangeFromTuples(layerWeightRange, self.minRange)

			for nodeIndex_1 in range(layerOutputs_1):
				x_1 = self.WIDTH * layerIndex/columns + self.WIDTH/columns/2
				y_1 = self.HEIGHT * nodeIndex_1/rows + self.HEIGHT/rows/2 + (rows - layerOutputs_1)*self.HEIGHT/rows/2
				
				#second node
				for nodeIndex_2 in range(layerOutputs_2):
					x_2 = self.WIDTH * layerIndex_2/columns + self.WIDTH/columns/2
					y_2 = self.HEIGHT * nodeIndex_2/rows + self.HEIGHT/rows/2 + (rows - layerOutputs_2)*self.HEIGHT/rows/2

					weight = weights[nodeIndex_1, nodeIndex_2]
					weight = mapToRange(weight, layerWeightRange, (-1, 1))
					color = interpolateColors(weight)
					pygame.draw.line(self.screen, self.outlineColor, (x_1, y_1), (x_2, y_2), self.connectionWidth + 2)
					pygame.draw.line(self.screen, color, (x_1, y_1), (x_2, y_2), self.connectionWidth)

	def drawLayerNodes(self):
		columns = len(self.model.dimentions)
		rows = max([layerOutputs for layerOutputs in self.model.dimentions])

		for layerIndex, layerOutputs in enumerate(self.model.dimentions):
			biases = self.model.layers[layerIndex - 1].biases
			maxLayerBias = max(max(biases), abs(min(biases)))
			layerBiasRange = (-maxLayerBias, maxLayerBias)
			layerBiasRange = maxRangeFromTuples(layerBiasRange, self.minRange)

			for nodeIndex in range(layerOutputs):
				x = self.WIDTH * layerIndex/columns + self.WIDTH/columns/2
				y = self.HEIGHT * nodeIndex/rows + self.HEIGHT/rows/2 + (rows - layerOutputs)*self.HEIGHT/rows/2
				if layerIndex == 0:
					color = (50, 50, 200)
				else:
					bias = mapToRange(biases[nodeIndex], layerBiasRange, (-1, 1))
					color = interpolateColors(bias)
				pygame.draw.circle(self.screen, self.outlineColor, (x, y), self.nodeRadius + 1)
				pygame.draw.circle(self.screen, color, (x, y), self.nodeRadius)

	def update(self):
		#check if closed window
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			elif event.type == pygame.VIDEORESIZE:  # Handles window resize events
				self.WIDTH, self.HEIGHT = event.w, event.h
				self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)

		# Clear the screen
		self.screen.fill(self.backgroundColor)

		self.drawConnections()
		self.drawLayerNodes()
		
		# Update the display
		pygame.display.flip()

		#put into matplotlib (if in settings)
		if self.ax != None:
			pygame_array = pygame.surfarray.array3d(self.screen)
			pygame_array = np.transpose(pygame_array, (1, 0, 2))
			self.ax.clear()
			self.ax.imshow(pygame_array)
			self.ax.axis('off')

		
