import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import random

def curve(x, y):
	return math.cos(1.5 * x) * math.sin(1.5 * y) + math.cos(.4 * x)**2 + math.cos(.2 * y)**2

# Create the data for the surface
plotRange_x = (-3, 3)
plotRange_y = (-3, 3)
x = np.linspace(plotRange_x[0], plotRange_x[1], 10)
y = np.linspace(plotRange_y[0], plotRange_y[1], 10)
X, Y = np.meshgrid(x, y)

# Due to more complex functions
Z = np.zeros_like(X)
for i in range(X.shape[0]):
	for j in range(X.shape[1]):
		Z[i, j] = curve(X[i, j], Y[i, j])

# Create the figure and 3D axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=.5)

# Add labels and legend
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show(block=False)

point = None
point_x = 0
point_y = 0

while True:
	plt.pause(.1)
	
	if point != None:
		point.remove()

	# Coordinates of the point
	point_x += .1
	point_y += .1

	if point_x < plotRange_x[0] or point_x > plotRange_x[1] or point_y < plotRange_y[0] or point_y > plotRange_y[1]:
		point_x = random.randrange(plotRange_x[0], plotRange_x[1])
		point_y = random.randrange(plotRange_y[0], plotRange_y[1])
		
	point_z = curve(point_x, point_y)

	# Plot the point
	point = ax.scatter(point_x, point_y, point_z, color='red', s=100)
