from VariableSliders import SliderWindow2D, SliderWindow
from MathThings import *
import numpy as np
import math

class Model:
	def __init__(self, dimentions):
		self.layers = []
		self.dimentions = dimentions.copy()

		numInputs = dimentions.pop(0)
		for layerIndex, numOutputs in enumerate(dimentions):
			self.layers.append(Layer(numInputs, numOutputs, self))
			numInputs = numOutputs
	
	def calculate(self, inputs):
		if len(inputs) != self.dimentions[0]:
			print("Inputs do not match")
			return None

		for layer in self.layers:
			inputs = layer.getOutputs(inputs)

		return inputs[0] > inputs[1]
	
	def costFunction(calculated, expected):
		error = calculated - expected
		return error ** 2 #emphasises larger errors (and makes positive)

	def getCost(self, inputs, expectedOutputs):
		outputs = self.calculate(inputs)

		cost = 0
		for outputIndex in range(len(outputs)):
			cost += self.costFunction(outputs[outputIndex], expectedOutputs[outputIndex])
		return cost
	
	def getTotalCost(self, inputsList, expectedOutputsList):
		totalCost = 0

		for dataPoint in range(len(inputsList)):
			totalCost += self.cost(inputsList[dataPoint], expectedOutputsList[dataPoint])
		
		return totalCost / len(inputsList) #return average


class Layer:
	def __init__(self, numInputs, numOutputs, model):
		self.numInputs = numInputs
		self.numOutputs = numOutputs
		self.weights = np.zeros((numInputs, numOutputs))
		self.biases = np.zeros(numOutputs)
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

	def setWeights(self, newWeights):
		self.weights = newWeights

		

