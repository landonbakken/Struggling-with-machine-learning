import pygame
from VariableSliders import SliderWindow2D
from MathThings import *
import numpy as np
import time
from Plotter import InequalityPlotter

#model settings
MODEL_DIMENTIONS = [2, 2]

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
NODE_SPACING = (NODE_WINDOW_HEIGHT / max(MODEL_DIMENTIONS)) * NODE_SCALE

#set up pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Model Visualizer")

def drawThings():
    InequalityPlotter(model.calculate)

class Model:
    def __init__(self, dimentions):
        self.layers = []
        self.dimentions = dimentions.copy()

        numInputs = dimentions.pop(0)
        for layerIndex, numOutputs in enumerate(dimentions):
            layerName = f"Hidden Layer {layerIndex} Weights" if layerIndex != len(dimentions) - 1 else "Ouput Weights"
            self.layers.append(Layer(numInputs, numOutputs, layerName))
            numInputs = numOutputs
    
    def calculate(self, inputs):
        if len(inputs) != self.dimentions[0]:
            print("Inputs do not match")
            return None

        for layer in self.layers:
            inputs = layer.getOutputs(inputs)

        return inputs[0] > inputs[1]

class Layer:
    def __init__(self, numInputs, numOutputs, layerName):
        self.numInputs = numInputs
        self.numOutputs = numOutputs
        self.weights = np.random.rand(numInputs, numOutputs)
        self.weightSliders = SliderWindow2D(numInputs, numOutputs, layerName, self.setWeights)

    def getOutputs(self, inputs):
        if len(inputs) != self.numInputs:
            print("Incorrect number of inputs")
            return None

        weightedInputs = []
        for output in range(self.numOutputs):
            weightedInput = 0
            for input in range(len(inputs)):
                weightedInput += inputs[input] * self.weights[input][output]
            weightedInputs.append(weightedInput)
        
        return weightedInputs

    def setWeights(self, newWeights):
        self.weights = newWeights
        drawThings()

#model format
changes = False
model = Model(MODEL_DIMENTIONS)

# Main loop
running = True
while running:
    time.sleep(.001) #time for tkinter to process some things

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
