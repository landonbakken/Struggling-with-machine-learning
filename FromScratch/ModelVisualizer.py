from SimpleModel import *
from MathThings import *
import pygame

pygame.init()

class ModelVisualizer:
	def __init__(self, model, windowWidth = 800, windowHeight = 600, nodeRadius = 25, connectionWidth = 5, colorRange = (0, 255), outlineColor = (255, 255, 255), backgroundColor=(0, 0, 0)):
		self.model = model
		self.WIDTH = windowWidth
		self.HEIGHT = windowHeight
		self.nodeRadius = nodeRadius
		self.connectionWidth = connectionWidth
		self.colorRange = colorRange
		self.outlineColor = outlineColor
		self.backgroundColor = backgroundColor

		# Initialize Pygame
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		pygame.display.set_caption("Model Visualizer")

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

			for nodeIndex_1 in range(layerOutputs_1):
				x_1 = self.WIDTH * layerIndex/columns + self.WIDTH/columns/2
				y_1 = self.HEIGHT * nodeIndex_1/rows + self.HEIGHT/rows/2 + (rows - layerOutputs_1)*self.HEIGHT/rows/2
				
				#second node
				for nodeIndex_2 in range(layerOutputs_2):
					x_2 = self.WIDTH * layerIndex_2/columns + self.WIDTH/columns/2
					y_2 = self.HEIGHT * nodeIndex_2/rows + self.HEIGHT/rows/2 + (rows - layerOutputs_2)*self.HEIGHT/rows/2

					weight = weights[nodeIndex_1, nodeIndex_2]
					color = mapToRange(weight, layerWeightRange, self.colorRange)
					pygame.draw.line(self.screen, self.outlineColor, (x_1, y_1), (x_2, y_2), self.connectionWidth + 2)
					pygame.draw.line(self.screen, (color, color, color), (x_1, y_1), (x_2, y_2), self.connectionWidth)

	def drawLayerNodes(self):
		columns = len(self.model.dimentions)
		rows = max([layerOutputs for layerOutputs in self.model.dimentions])

		for layerIndex, layerOutputs in enumerate(self.model.dimentions):
			biases = self.model.layers[layerIndex - 1].biases
			maxLayerBias = max(max(biases), abs(min(biases)))
			layerBiasRange = (-maxLayerBias, maxLayerBias)

			for nodeIndex in range(layerOutputs):
				x = self.WIDTH * layerIndex/columns + self.WIDTH/columns/2
				y = self.HEIGHT * nodeIndex/rows + self.HEIGHT/rows/2 + (rows - layerOutputs)*self.HEIGHT/rows/2
				if layerIndex == 0:
					color = (50, 200, 50)
				else:
					color = mapToRange(biases[nodeIndex], layerBiasRange, self.colorRange)
					color = (color, color, color)
				pygame.draw.circle(self.screen, self.outlineColor, (x, y), self.nodeRadius + 1)
				pygame.draw.circle(self.screen, color, (x, y), self.nodeRadius)

	def update(self):
		#check if closed window
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

		# Clear the screen
		self.screen.fill(self.backgroundColor)

		self.drawConnections()
		self.drawLayerNodes()
		
		# Update the display
		pygame.display.flip()
