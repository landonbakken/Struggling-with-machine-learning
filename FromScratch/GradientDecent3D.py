import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import random
from MathThings import *

def curve(point):
	x, y = point
	return math.cos(1 * x) * math.sin(1.1 * y) + math.cos(.3 * x)**2 + math.cos(.15 * y)**2

#im sure there is a way to do this in like one line, but I don't really care right now (:
def stepPoint(point, gradient):
	gradient_x, gradient_y = gradient
	point_x, point_y = point
	return (point_x - gradient_x * learnRate, point_y - gradient_y * learnRate)

def decentDone(point, xRange, yRange, gradient, minGradient):
	if point[0] < xRange[0] or point[0] > xRange[1] or point[1] < yRange[0] or point[1] > yRange[1]:
		print("outside range")
		return True
	
	if abs(gradient[0]) + abs(gradient[1]) < minGradient:
		return True
	
	return False

# Create the data for the surface
plotRange_x = (-4, 4)
plotRange_y = (-4, 4)
randomRange = 1.5
x = np.linspace(plotRange_x[0], plotRange_x[1], 100)
y = np.linspace(plotRange_y[0], plotRange_y[1], 100)
X, Y = np.meshgrid(x, y)

# Due to more complex functions
Z = np.zeros_like(X)
for i in range(X.shape[0]):
	for j in range(X.shape[1]):
		Z[i, j] = curve((X[i, j], Y[i, j]))

# Create the figure and 3D axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=.5)

# Add labels and legend
ax.set_xlabel('Weight 1')
ax.set_ylabel('Weight 2')
ax.set_zlabel('Cost')

# Show the plot
plt.show(block=False)

point = None
point_x = 0
point_y = 0
step = .000001
learnRate = .15

while True:
	plt.pause(.01)
	
	#clear past loop
	if point != None:
		point.remove()

	# Coordinates of the point
	gradient = getGradient(curve, (point_x, point_y), step)
	point_x, point_y = stepPoint((point_x, point_y), gradient)

	if decentDone((point_x, point_y), plotRange_x, plotRange_y, gradient, .001):
		point_x = random.random() * randomRange
		point_y = random.random() * randomRange

	point_z = curve((point_x, point_y))

	# Plot the point
	point = ax.scatter(point_x, point_y, point_z, color='red', s=100)
