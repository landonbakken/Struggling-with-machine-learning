from VariableSliders import SliderWindow2D, SliderWindow
from MathThings import *
import numpy as np
import math

class Model:
    def __init__(self, dimentions, useSliders=False):
        self.layers = []
        self.dimentions = dimentions.copy()

        numInputs = dimentions.pop(0)
        for layerIndex, numOutputs in enumerate(dimentions):
            layerName = f"Hidden Layer {layerIndex} Weights" if layerIndex != len(dimentions) - 1 else "Ouput Weights"
            self.layers.append(Layer(numInputs, numOutputs, layerName, self, useSliders))
            numInputs = numOutputs
    
    def calculate(self, inputs):
        if len(inputs) != self.dimentions[0]:
            print("Inputs do not match")
            return None

        for layer in self.layers:
            inputs = layer.getOutputs(inputs)

        return inputs[0] > inputs[1]

class Layer:
    def __init__(self, numInputs, numOutputs, layerName, model, useSliders):
        self.numInputs = numInputs
        self.numOutputs = numOutputs
        self.weights = np.zeros((numInputs, numOutputs))
        self.biases = np.zeros(numOutputs)
        if useSliders:
            self.biasSliders = SliderWindow(numOutputs, layerName + " Biases", self.setBiases)
            self.weightSliders = SliderWindow2D(numInputs, numOutputs, layerName + " Weights", self.setWeights)
        self.model = model

    def getOutputs(self, inputs):
        if len(inputs) != self.numInputs:
            print("Incorrect number of inputs")
            return None

        weightedInputs = []
        for output in range(self.numOutputs):
            weightedInput = self.biases[output]
            for input in range(len(inputs)):
                weightedInput += inputs[input] * self.weights[input][output]
            weightedInputs.append(self.activationFunction(weightedInput))
        
        return weightedInputs
    
    def activationFunction(self, value): 
        return 1/(1+math.exp(-value))
    
    def setBiases(self, newBiases):
        self.biases = newBiases
        self.model.draw()

    def setWeights(self, newWeights):
        self.weights = newWeights

        

