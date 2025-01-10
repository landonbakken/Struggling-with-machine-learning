from VariableSliders import SliderWindow2D, SliderWindow
from MathThings import *
import numpy as np
import math

class Datapoint:
	def __init__(self, inputs, condition):
		self.inputs = inputs
		self.expectedOutputs = condition(inputs)
		self.pointColor = "green" if self.expectedOutputs[0] == 1 else "red" #really just for true/false (2 output nodes)

class Model:
	def __init__(self, dimentions, costFunction):
		self.layers = []
		self.dimentions = dimentions.copy()
		self.costFunction = costFunction

		numInputs = dimentions.pop(0)
		for numOutputs in dimentions:
			self.layers.append(Layer(numInputs, numOutputs, self))
			numInputs = numOutputs
	
	def calculate(self, inputs):
		if len(inputs) != self.dimentions[0]:
			print("Inputs do not match")
			return

		for layer in self.layers:
			inputs = layer.getOutputs(inputs)

		return inputs

	def getCost(self, datapoint):
		outputs = self.calculate(datapoint.inputs)
		#print(outputs)

		cost = 0
		for outputIndex in range(len(outputs)):
			cost += self.costFunction(outputs[outputIndex], datapoint.expectedOutputs[outputIndex])
		
		return cost, listToBool(datapoint.expectedOutputs) == listToBool(outputs)
	
	def getTotalCost(self, dataset):
		totalCost = 0
		totalCorrect = 0
		for datapoint in dataset:
			cost, wasRight = self.getCost(datapoint)
			totalCost += cost
			if wasRight:
				totalCorrect += 1
		
		return totalCost / len(dataset), totalCorrect #return average

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

		

