import matplotlib.pyplot as plt
import numpy as np
	 
class Plotter:
	def __init__(self, inequalityFunc, dataset, x_range=(-100, 100), y_range=(-100, 100), resolution=100):
		self.fig, self.ax = plt.subplots()
		self.x_range = x_range
		self.y_range = y_range
		self.resolution = resolution
		
		# Create coordinate grids
		x = np.linspace(x_range[0], x_range[1], resolution)
		y = np.linspace(y_range[0], y_range[1], resolution)
		self.X, self.Y = np.meshgrid(x, y)

		# Scatter plot
		self.plotScatter(dataset)
		
		# Initialize the plot
		self.inequalityPlot = None
		self.inequalityFunc = inequalityFunc
		self.updateInequality()
		
		# Set up the plot
		self.ax.set_aspect('equal')
		self.ax.set_xlabel('x')
		self.ax.set_ylabel('y')

		#show
		plt.show(block=False)

	def updateInequality(self):
		#draw inequality
		self.drawInequality()
		
		#draw everything
		plt.draw()

	def drawInequality(self):
		# Clear previous plot
		if self.inequalityPlot is not None:
			# Remove all contour collections
			for contour in self.inequalityPlot.collections:
				contour.remove()

		# Evaluate the inequality over the grid
		Z = np.zeros_like(self.X, dtype=bool)

		# Due to more complex functions
		for i in range(self.X.shape[0]):
			for j in range(self.X.shape[1]):
				Z[i, j] = self.inequalityFunc((self.X[i, j], self.Y[i, j]))

		# Plot the inequality using contourf
		contour = self.ax.contourf(
			self.X, self.Y, Z,
			levels=[-0.5, 0.5, 1.5],  # Thresholds for boolean values
			colors=['red', 'green'],
			alpha=0.4
		)

		self.inequalityPlot = contour

	def plotScatter(self, data):
		# Separate the points based on their boolean values
		green_points = [(x, y) for x, y, value in data if value]
		red_points = [(x, y) for x, y, value in data if not value]

		# Unpack the points into x and y coordinates
		green_x, green_y = zip(*green_points) if green_points else ([], [])
		red_x, red_y = zip(*red_points) if red_points else ([], [])

		# Create the scatter plot
		plt.scatter(green_x, green_y, color='green', label='False')
		plt.scatter(red_x, red_y, color='red', label='True')
