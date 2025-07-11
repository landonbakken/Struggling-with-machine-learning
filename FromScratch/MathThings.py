import math
import numpy as np
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def clamp(value, minValue, maxValue):
	return max(min(value, maxValue), minValue)

def listToBool(list):
	return max(list) == list[0]

def boolToList(bool):
	return [1, 0] if bool else [0, 1]

def circleInequality(point, radius, offset = (0, 0)):
	x, y = point
	x_off, y_off = offset
	return (x - x_off)**2 + (y - y_off)**2 < radius

def testInequality(point):
	x, y = point
	#result = math.cos(5*x)/2.5 - y > 0 #sin wave
	
	result = circleInequality(point, .7) #circle
	
	#result = circleInequality(point, .9, (1, 1))#circle with radius in the corner
	#result = result or circleInequality(point, .9, (-1, -1))#circle with radius in the corner

	#result = x < -.5 or x > .5
	return [1, 0] if result else [0, 1] #convert to list format

def raw(value):
	return value

#vectorized
def softmax(values):
    shifted_values = values - np.max(values, axis=-1, keepdims=True)
    exp_values = np.where(np.abs(shifted_values) > 500, 0, np.exp(shifted_values)) #ensure no errors
    softmax_values = exp_values / np.sum(exp_values, axis=-1, keepdims=True)
    return softmax_values

#vectorized (and with a limit)
def sigmoidFunction(value):
    return np.where(np.abs(value) > 500, 0, 1 / (1 + np.exp(-value)))

def tanhFunction(value):
	return math.tanh(value)

#vectorized
def reluFunction(value): 
	return np.maximum(0, value)

#vectorized
def leakyReluFunction(value):
	return np.maximum(.1, value)

#def activationFunctionDerivative(value): 
#	activationValue = activationFunction(value)
#	return activationValue * (1 - activationValue)

def costFunction(calculated, expected):
	return (calculated - expected)**2 #emphasises larger errors (and makes positive)

# Define the function to graph
def mathFunction(x):
	return .2 * x**4 + .1 * x**3 - x**2

def pixelToCoord(value, scale, windowSize):
	return (value - windowSize / 2) / scale

def coordToPixel(value, scale, windowSize):
	return int(windowSize / 2 - value * scale)

def mapToRange(value, oldRange, newRange):
	if oldRange[1] - oldRange[0] == 0:
		return (newRange[0] + newRange[1])/2
	
	return newRange[0] + (value - oldRange[0]) * (newRange[1] - newRange[0]) / (oldRange[1] - oldRange[0])

def getGradient(curve, point, step):
	x, y = point
	z_initial = curve(point)

	xStepped = x + step
	z_xStepped = curve((xStepped, y))

	yStepped = y + step
	z_yStepped = curve((x, yStepped))

	return ((z_xStepped - z_initial)/step, (z_yStepped - z_initial)/step)

# right now just red -> black -> green
# -1 to 1
def interpolateColors(value):
    if value <= 0:
        r = int(255 * -value)
        g = 0
        b = 0
    else:
        r = 0
        g = int(255 * value)
        b = 0
    
    return (r, g, b)


def randomColor():
    """Returns a random RGB color as a tuple of three integers between 0 and 255."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# gets the max range from two tuples
# (-2, .1), (-.3, 5) -> (-2, 5)
def maxRangeFromTuples(tuple1, tuple2):
	return tuple((min(tuple1[0], tuple2[0]), max(tuple1[1], tuple2[1])))

# takes two numbers, and a percent of what the first number should be
# good for rolling averages
def rollingMeanRatio(value1, value2, percent):
	return value1 * percent + value2 * (1 - percent)


#model modification
def offsetArrayNormalized(initialArray, offsetAmount, percentToOffset):
	# Number of elements to modify (10% of the total number of elements)
	num_elements_to_modify = int(initialArray.size * percentToOffset)

	# Randomly select indices to modify
	indices = np.unravel_index(np.random.choice(initialArray.size, num_elements_to_modify, replace=False), initialArray.shape)

	# Generate random offsets from a normal distribution
	offsets = np.random.normal(loc=0, scale=offsetAmount, size=num_elements_to_modify)

	# Apply the offsets to the selected indices
	initialArray[indices] += offsets

def offsetArray(initialArray, offsetAmount, percentToOffset):
	# Number of elements to modify
	num_elements_to_modify = int(initialArray.size * percentToOffset)

	# Get indices of the array's elements
	indices = np.unravel_index(np.random.choice(initialArray.size, num_elements_to_modify, replace=False), initialArray.shape)

	# Set the selected elements to random values
	initialArray[indices] += np.random.uniform(-offsetAmount, offsetAmount, num_elements_to_modify)

def replaceArray(initialArray, randomRange, percentToReplace):
	# Number of elements to modify
	num_elements_to_modify = int(initialArray.size * percentToReplace)

	# Get indices of the array's elements
	indices = np.unravel_index(np.random.choice(initialArray.size, num_elements_to_modify, replace=False), initialArray.shape)

	# Set the selected elements to random values
	initialArray[indices] = np.random.uniform(randomRange[0], randomRange[1], num_elements_to_modify)

def makeChildren(parent, children, offsetAmount, offsetPercent, replacedRange, replacedPercent, scaleRange = (1, 1)):
	weights, biases = parent.getValues()
	for childIndex, child in enumerate(children):
		
		newWeights = weights.copy()
		newBiases = biases.copy()

		percent = (childIndex+1)/len(children)
		multiplier = scaleRange[0] * (1-percent) + scaleRange[1] * percent

		#biases
		for weightsIndex in range(newWeights.shape[0]):
			offsetArrayNormalized(newWeights[weightsIndex], offsetAmount, offsetPercent*multiplier)
			replaceArray(newWeights[weightsIndex], replacedRange, replacedPercent*multiplier)

		#biases
		for biasesIndex in range(newBiases.shape[0]):
			offsetArrayNormalized(newBiases[biasesIndex], offsetAmount, offsetPercent*multiplier)
			replaceArray(newBiases[biasesIndex], replacedRange, replacedPercent*multiplier)
		
		child.setValues(newWeights, newBiases)
		child.age = 0
		child.generation = parent.generation + 1

