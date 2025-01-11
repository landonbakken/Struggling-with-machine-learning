# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def clamp(value, minValue, maxValue):
	return max(min(value, maxValue), minValue)

def listToBool(list):
	return max(list) == list[0]

def boolToList(bool):
	return [1, 0] if bool else [0, 1]

def testInequality(points):
	x, y = points
	result = x**2 + y**2 < .6**2 #circle with radius
	return [1, 0] if result else [0, 1] #convert to list format

def costFunction(calculated, expected):
	error = calculated - expected
	return error**2 #emphasises larger errors (and makes positive)

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

