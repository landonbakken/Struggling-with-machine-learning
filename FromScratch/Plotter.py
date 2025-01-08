import matplotlib.pyplot as plt
import numpy as np

def drawInequality(inequalityFunc, ax, X, Y, x_range, y_range):
	# Evaluate the inequality over the grid
	Z = np.zeros_like(X)

	#due to more complex functions
	for i in range(X.shape[0]):
		for j in range(X.shape[1]):
			Z[i, j] = inequalityFunc((X[i, j], Y[i, j]))
		
	# Plot the inequality
	img = ax.imshow(
		Z,
		extent=[x_range[0], x_range[1], y_range[0], y_range[1]],
		origin='lower',
		cmap='RdYlBu',
		alpha=0.7
	)

	#draw everything
	plt.draw()

	return img

def plotScatter(data):
	# Separate the points based on their boolean values
	green_points = [(x, y) for x, y, value in data if not value]
	red_points = [(x, y) for x, y, value in data if value]

	# Unpack the points into x and y coordinates
	green_x, green_y = zip(*green_points) if green_points else ([], [])
	red_x, red_y = zip(*red_points) if red_points else ([], [])

	# Create the scatter plot
	plt.scatter(green_x, green_y, color='green', label='False')
	plt.scatter(red_x, red_y, color='red', label='True')
	 

class CombinedPlot:
	def __init__(self, inequalityFunct, dataset, x_range=(-100, 100), y_range=(-100, 100), resolution=100):
		self.fig, self.ax = plt.subplots()
		self.x_range = x_range
		self.y_range = y_range
		self.resolution = resolution
		
		# Create coordinate grids
		x = np.linspace(x_range[0], x_range[1], resolution)
		y = np.linspace(y_range[0], y_range[1], resolution)
		self.X, self.Y = np.meshgrid(x, y)

		# Scatter plot
		plotScatter(dataset)
		
		# Initialize the plot
		self.img = None
		self.inequalityFunct = inequalityFunct
		self.updateInequality()
		
		# Set up the plot
		self.ax.set_aspect('equal')
		self.ax.set_xlabel('x')
		self.ax.set_ylabel('y')

		#show
		plt.show(block=False)

	def updateInequality(self):
		# Clear previous plot
		if self.img is not None:
			self.img.remove()

		#draw inequality
		self.img = drawInequality(self.inequalityFunct, self.ax, self.X, self.Y, self.x_range, self.y_range)
