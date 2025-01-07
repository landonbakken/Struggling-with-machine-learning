import pygame
import VariableSliders
import random

#model settings
dimentions = [2, 3, 2]

# Set screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#visual settings
COLOR_MARGIN = 30
NODE_SCALE = 1
CONNECTION_WIDTH = 5
NODE_RADIUS = 25

#calculations
CONNECTION_WIDTH = (int) (CONNECTION_WIDTH * NODE_SCALE)
NODE_RADIUS = (int) (NODE_RADIUS * NODE_SCALE)
NODE_WINDOW_WIDTH = SCREEN_WIDTH * NODE_SCALE
NODE_WINDOW_HEIGHT = SCREEN_HEIGHT
NODE_SPACING = (NODE_WINDOW_HEIGHT / max(dimentions)) * NODE_SCALE


#connections

#set up pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Model Visualizer")


class Model:
    def __init__(self, dimentions):
        self.layers = []

        #create nodes
        for layerIndex in range(len(dimentions)):
            layerNodes = []
            for nodeIndex in range(dimentions[layerIndex]):
                newNode = Node(layerIndex, nodeIndex, len(dimentions), dimentions[layerIndex])
                layerNodes.append(newNode)
            self.layers.append(layerNodes)
        
        #connect nodes (not last layer since they don't have any)
        for layerIndex in range(len(dimentions) - 1):
            layer = self.layers[layerIndex]
            nextLayer = self.layers[layerIndex + 1]

            for node in layer:
                node.makeConnections(nextLayer)
    
    def draw(self):
        #loop through layer
        for layer in self.layers:
            #get the max value per layer(for percent based coloring)
            maxValue = max([node.value for node in layer])
            maxValue = 1 if maxValue == 0 else maxValue #cant be 0

            #get the max weight per layer (for percent based coloring)
            if layer != self.layers[-1]:
                maxWeight = max(layer[0].weights)
                for node in layer:
                    maxWeight = max(maxWeight, max(node.weights))

                maxWeight = 1 if maxWeight == 0 else maxWeight #cant be 0
            else:
                maxWeight = 1 #doesnt matter since there arent connections for last layer

            #draw each node
            for node in layer:
                node.draw(maxValue, maxWeight)
    
    def recalculate(self):
        #clear values (except for the first one)
        for layerIndex in range(len(self.layers) - 1):
            for node in self.layers[layerIndex + 1]:
                node.clear()

        #add values
        for layer in self.layers:
            for node in layer:
                node.calculate()

def clamp(value, minValue, maxValue):
    return max(min(value, maxValue), minValue)

class Node:
    def __init__(self, layerIndex, nodeIndex, totalLayers, totalNodesInLayer):
        self.layerIndex = layerIndex
        self.nodeIndex = nodeIndex
        self.connectedNodes = []
        self.weights = []
        self.value = 0

        #get draw position
        x = (int) ((layerIndex + 1) / (totalLayers + 1) * NODE_WINDOW_WIDTH)
        y = (int) (NODE_WINDOW_HEIGHT / 2 + (totalNodesInLayer / 2 - (nodeIndex + .5)) * NODE_SPACING)
        self.drawPosition = (x, y)

    def draw(self, maxValueInLayer, maxWeightInLayer):
        #connections (drawn first so they don't overlap nodes)
        for connectedNodeIndex in range(len(self.connectedNodes)):
            color = (int) (255 * self.weights[connectedNodeIndex] / maxWeightInLayer)
            if color > 255 or color < 0:
                print(f"Connection color error: {self.weights[connectedNodeIndex]} -> {color}")
                color = clamp(color, 0, 255)
            pygame.draw.line(screen, (color, color, color), self.drawPosition, self.connectedNodes[connectedNodeIndex].drawPosition, CONNECTION_WIDTH)
        
        #the circle
        color = (int) (255 * self.value / maxValueInLayer)
        if color > 255 or color < 0:
            print(f"Node color error: {self.value} -> {color}")
            color = clamp(color, 0, 255)
        pygame.draw.circle(screen, (color, color, color), self.drawPosition, NODE_RADIUS)

    #one node
    def makeConnection(self, nodeToConnect):
        self.connectedNodes.append(nodeToConnect)
        self.weights.append(.5)

    #a list of nodes
    def makeConnections(self, nodesToConnect):
        for node in nodesToConnect:
            self.makeConnection(node)

    def clear(self):
        self.value = 0

    def calculate(self):
        #add value * weight to connected nodes
        for connectedNodeIndex in range(len(self.connectedNodes)):
            self.connectedNodes[connectedNodeIndex].value += self.value * self.weights[connectedNodeIndex]

def updateSliderValues(sliderValues):
    for key, value in sliderValues.items():
        #parse key into list
        parsedKey = [int(item.strip()) for item in key.split(",")]
        
        #get node
        node = model.layers[parsedKey[0]][len(model.layers[parsedKey[0]]) - parsedKey[1] - 1]
        
        #if input
        if len(parsedKey) == 2:
            node.value = value
        #if weight
        else:
            node.weights[parsedKey[2]] = value

    model.recalculate()
    
    # Fill the screen with white
    screen.fill(BLACK)

    #draw everything
    model.draw() 

    # Update the display
    pygame.display.flip()

def getSliderConfigFromDim(dimentions):
    #variable sliders
    sliderConfig = []
    sliderValues = {}
    for dimentionIndex in range(len(dimentions) - 1):
        for valueIndex in range(dimentions[dimentionIndex]):
            if dimentionIndex == 0:
                id = f"{dimentionIndex}, {valueIndex}"
                name = f"Input {valueIndex}"
                sliderConfig.append((name, id, 0, 1))
                sliderValues[id] = random.random()

            for weight in range(dimentions[dimentionIndex + 1]):
                id = f"{dimentionIndex}, {valueIndex}, {weight}"
                name = f"Weight: layer {dimentionIndex}, node {valueIndex} -> {weight}"
                sliderConfig.append((name, id, 0, 1))
                sliderValues[id] = random.random()

    return sliderConfig, sliderValues

#model format
model = Model(dimentions)

sliderConfig, sliderValues = getSliderConfigFromDim(dimentions)
variableSliders = VariableSliders.sliderWindow("Model Settings", sliderValues, sliderConfig, updateSliderValues)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #nothing currently

# Quit Pygame
pygame.quit()
