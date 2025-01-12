import math

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def clamp(value, minValue, maxValue):
	return max(min(value, maxValue), minValue)

def listToBool(list):
	return max(list) == list[0]

def boolToList(bool):
	return [1, 0] if bool else [0, 1]

def circleInequality(point, radius, offset):
	x, y = point
	x_off, y_off = offset
	return (x - x_off)**2 + (y - y_off)**2 < radius

def testInequality(point):
	x, y = point
	#result = math.cos(10*x)/10 + .5 - y > 0 #sin wave
	#result = x**2 + y**2 < .6**2 #circle
	result = circleInequality(point, .9, (1, 1))#circle with radius in the corner
	result = result or circleInequality(point, .9, (-1, -1))#circle with radius in the corner

	#result = x < -.5 or x > .5
	return [1, 0] if result else [0, 1] #convert to list format

def sigmoidFunction(value): 
	return 1/(1 + math.exp(-value))

def sigmoidFunction_fromTanH(value): 
	return (math.tanh(value) + 1)/2

def tanhFunction(value):
	return math.tanh(value)

def reluFunction(value): 
	return max(0, value)

def leakyReluFunction(value):
	return max(.1 * value, value)

#def activationFunctionDerivative(value): 
#	activationValue = activationFunction(value)
#	return activationValue * (1 - activationValue)

def costFunction(calculated, expected):
	error = calculated - expected
	return error**2 #emphasises larger errors (and makes positive)

def costFunctionDerivative(calculated, expected):
	return 2 * (calculated - expected)

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

# gets the max range from two tuples
# (-2, .1), (-.3, 5) -> (-2, 5)
def maxRangeFromTuples(tuple1, tuple2):
	return tuple((min(tuple1[0], tuple2[0]), max(tuple1[1], tuple2[1])))

# takes two numbers, and a percent of what the first number should be
# good for rolling averages
def rollingMeanRatio(value1, value2, percent):
	return value1 * percent + value2 * (1 - percent)

