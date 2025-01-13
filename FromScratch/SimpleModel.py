from MathThings import *
import numpy as np

class Datapoint:
	def __init__(self, inputs, condition):
		self.inputs = inputs
		self.expectedOutputs = condition(inputs)
		self.pointColor = "green" if self.expectedOutputs[0] == 1 else "red" #really just for true/false (2 output nodes)

class Model:
	def __init__(self, dimentions, costFunction, hiddenActivationFunction, outputActivationFunction, regularizationStrength = None, regularizationOffset = .001):
		self.layers = np.empty(len(dimentions) - 1, dtype=Layer) #-1 becasue the input layer isnt really a layer
		self.dimentions = dimentions.copy()
		self.costFunction = costFunction
		self.regularizationStrength = regularizationStrength
		self.regularizationOffset = regularizationOffset

		dimentions = dimentions.copy()
		numInputs = dimentions.pop(0)
		for numOutputsIndex, numOutputs in enumerate(dimentions):
			if numOutputsIndex + 1 == len(dimentions):
				activationFunction = outputActivationFunction
			else:
				activationFunction = hiddenActivationFunction
			self.layers[numOutputsIndex] = Layer(numInputs, numOutputs, activationFunction, self)
			numInputs = numOutputs

	def learn(self, datapoints, weightLearnRate, biasLearnRate):
		h = .000001 #closer to 0, the better
		initialCost = self.getTotalCost(datapoints, False)

		for layer in self.layers:
			#loop through each weight
			for inputIndex in range(layer.numInputs):
				for outputIndex in range(layer.numOutputs):
					#increment weight
					layer.weights[inputIndex, outputIndex] += h

					#get how much the cost changed
					costChange = self.getTotalCost(datapoints, False) - initialCost 

					#revert so other weights are unaffected
					layer.weights[inputIndex, outputIndex] -= h

					#give the layer gradient (unapplied so other weights can be changed)
					layer.weightCostGradients[inputIndex, outputIndex] = costChange / h

			#same thing as weights, but for biases
			for biasIndex in range(layer.numOutputs):
				layer.biases[biasIndex] += h
				costChange = self.getTotalCost(datapoints, False) - initialCost
				layer.biases[biasIndex] -= h
				layer.biasCostGradients[biasIndex] = costChange / h
		
		#after getting all gradients, apply them
		for layer in self.layers:
			layer.applyGradients(weightLearnRate, biasLearnRate)

		return self.getTotalCost(datapoints, False)
	
	def calculate(self, inputs):
		for layer in self.layers:
			inputs = layer.getOutputs(inputs)

		return inputs

	def randomizeValues(self):
		for layer in self.layers:
			layer.randomizeValues()

	def getValues(self):
		weights = np.empty(len(self.layers), dtype=object)
		biases = np.empty(len(self.layers), dtype=object)
		for layerIndex, layer in enumerate(self.layers):
			weights[layerIndex] = layer.weights
			biases[layerIndex] = layer.biases

		return weights, biases

	def setValues(self, weights, biases):
		for layerIndex, layer in enumerate(self.layers):
			layer.setBiases(biases[layerIndex], True)
			layer.setWeights(weights[layerIndex], True)

	def getCost(self, datapoint):
		outputs = self.calculate(datapoint.inputs)
		cost = 0

		#compare calculated and expected outputs
		for outputIndex in range(len(outputs)):
			cost += self.costFunction(outputs[outputIndex], datapoint.expectedOutputs[outputIndex])
		
		#regularization
		if self.regularizationStrength != None:
			weightsSquaredSum = 0
			for layer in self.layers:
				weightsSquaredSum += np.sum((np.abs(layer.weights) - self.regularizationOffset) ** 2)
			cost += self.regularizationStrength * weightsSquaredSum
		
		return cost, listToBool(datapoint.expectedOutputs) == listToBool(outputs)
	
	def getTotalCost(self, dataset, returnTotalCorrect = True):
		totalCost = 0
		totalCorrect = 0
		for datapoint in dataset:
			cost, wasRight = self.getCost(datapoint)
			totalCost += cost
			if wasRight:
				totalCorrect += 1
		
		if returnTotalCorrect:
			return totalCost / len(dataset), totalCorrect
		return totalCost / len(dataset) #return average
		

class Layer:
	def __init__(self, numInputs, numOutputs, activationFunction, model, weightRange = 1, biasRange = 1):
		self.numInputs = numInputs
		self.numOutputs = numOutputs
		self.activationFunction = activationFunction
		self.model = model

		self.weightRange = weightRange
		self.biasRange = biasRange

		self.weights = np.random.uniform(low=-weightRange, high=weightRange, size=(numInputs, numOutputs))
		self.biases = np.random.uniform(low=-biasRange, high=biasRange, size=(numOutputs))

		self.biasSliderWindow = None
		self.weightSliderWindow = None

		#initialize gradients
		self.biasCostGradients = np.zeros_like(self.biases)
		self.weightCostGradients = np.zeros_like(self.weights)

	def applyGradients(self, weightLearnRate, biasLearnRate):
		self.setBiases(self.biases - self.biasCostGradients * biasLearnRate, True)
		self.setWeights(self.weights - self.weightCostGradients * weightLearnRate, True)

	def randomizeValues(self):
		newWeights = np.random.uniform(low=-self.weightRange, high=self.weightRange, size=(self.numInputs, self.numOutputs))
		newBiases = np.random.uniform(low=-self.biasRange, high=self.biasRange, size=(self.numOutputs))

		self.setBiases(newBiases, True)
		self.setWeights(newWeights, True)

	def getOutputs(self, inputs):
		weightedInputs = np.empty(self.numOutputs, dtype=float)
		for outputIndex, output in enumerate(range(self.numOutputs)):
			weightedInput = self.biases[output]
			for input in range(len(inputs)):
				weightedInput += inputs[input] * self.weights[input][output]
			weightedInputs[outputIndex] = self.activationFunction(weightedInput)
		
		return weightedInputs
	
	def setBiases(self, newBiases, setSliders = False):
		self.biases = np.array(newBiases, dtype=float)

		if setSliders and self.biasSliderWindow is not None:
			self.biasSliderWindow.setValues(newBiases)

	def setWeights(self, newWeights, setSliders = False):
		self.weights = np.array(newWeights, dtype=float)

		if setSliders and self.biasSliderWindow is not None:
			self.weightSliderWindow.setValues(newWeights)

		

