import pygame


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
NODE_COLOR = WHITE
NODE_RADIUS = 25
NODE_SPACING = 100 + NODE_RADIUS * 2
NODE_LAYER_SPACING = 300 + NODE_RADIUS * 2

#set up pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Model Visualizer")


class Model:
    def __init__(self, dimentions):
        self.layers = []
        self.nodes = []

        for layerIndex in range(len(dimentions)):
            layerNodes = []
            for nodeIndex in range(dimentions[layerIndex]):
                newNode = Node(layerIndex, nodeIndex, len(dimentions), dimentions[layerIndex])
                layerNodes.append(newNode)
                self.nodes.append(newNode)
            self.layers.append(layerNodes)
    
    def draw(self):
        for node in self.nodes:
            node.draw()

class Node:
    def __init__(self, layerIndex, nodeIndex, totalLayers, totalNodesInLayer):
        self.layerIndex = layerIndex
        self.nodeIndex = nodeIndex

        #get draw position
        x = (int) (SCREEN_WIDTH / 2 + (totalLayers / 2 - (layerIndex + .5)) * NODE_LAYER_SPACING)
        y = (int) (SCREEN_HEIGHT / 2 + (totalNodesInLayer / 2 - (nodeIndex + .5)) * NODE_SPACING)
        self.drawPosition = (x, y)

    def draw(self):
        pygame.draw.circle(screen, NODE_COLOR, self.drawPosition, NODE_RADIUS)

#model format
dimentions = [2, 3, 2]
model = Model(dimentions)

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
