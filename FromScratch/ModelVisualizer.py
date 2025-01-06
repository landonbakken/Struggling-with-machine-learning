import pygame
import VariableSliders

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
NODE_COLOR_MARGIN = 30
CONNECTION_COLOR = BLUE
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
        self.nodes = [] #just for drawing

        pastLayerNodes = []
        for layerIndex in range(len(dimentions)):
            layerNodes = []
            for nodeIndex in range(dimentions[layerIndex]):
                newNode = Node(layerIndex, nodeIndex, len(dimentions), dimentions[layerIndex], pastLayerNodes)
                layerNodes.append(newNode)
                self.nodes.append(newNode)
            pastLayerNodes = layerNodes
            self.layers.append(layerNodes)

        #for visual reasons (overlapping)
        self.nodes.reverse()
    
    def draw(self):
        #draw each node
        for node in self.nodes:
            node.draw()
    
    def recalculate(self):
        pass

class Node:
    def __init__(self, layerIndex, nodeIndex, totalLayers, totalNodesInLayer, connectedNodes):
        self.layerIndex = layerIndex
        self.nodeIndex = nodeIndex
        self.connectedNodes = connectedNodes
        self.weights = [] #corrispond with connectedNodes
        self.value = 0

        #get draw position
        x = (int) ((layerIndex + 1) / (totalLayers + 1) * NODE_WINDOW_WIDTH)
        y = (int) (NODE_WINDOW_HEIGHT / 2 + (totalNodesInLayer / 2 - (nodeIndex + .5)) * NODE_SPACING)
        self.drawPosition = (x, y)

    def draw(self):
        #connections (drawn first so they don't overlap nodes)
        for connectedNode in self.connectedNodes:
            color = 255
            pygame.draw.line(screen, (color, color, color), self.drawPosition, connectedNode.drawPosition, CONNECTION_WIDTH)
        
        #the circle
        color = (255 - NODE_COLOR_MARGIN) * self.value + NODE_COLOR_MARGIN / 2
        pygame.draw.circle(screen, (color, color, color), self.drawPosition, NODE_RADIUS)

def updateSliderValues(sliderValues):
    for key, value in sliderValues.items():
        parsedKey = [int(item.strip()) for item in key.split(",")]
        model.layers[parsedKey[0]][len(model.layers[parsedKey[0]]) - parsedKey[1] - 1].value = value
    model.recalculate()

def getSliderConfigFromDim(dimentions):
    #variable sliders
    sliderConfig = []
    sliderValues = {}
    for dimentionIndex in range(len(dimentions) - 1):
        for valueIndex in range(dimentions[dimentionIndex]):
            if dimentionIndex == 0:
                name = "Input"
            elif dimentionIndex < len(dimentions) - 1:
                name = "Hidden"
            
            id = f"{dimentionIndex}, {valueIndex}"
            sliderConfig.append((f"{name} {valueIndex} Layer {dimentionIndex}", id, 0, 1))
            sliderValues[id] = .5

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

    # Fill the screen with white
    screen.fill(BLACK)

    model.draw()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
