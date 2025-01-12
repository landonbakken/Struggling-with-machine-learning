import matplotlib.pyplot as plt
import numpy as np
from MathThings import *

class IncrementingScatter:
	def __init__(self, fig, ax, xLabel, yLabel):
		self.fig = fig
		self.ax = ax

		self.values = []
		self.plot = None

		self.ax.set_xlabel(xLabel)
		self.ax.set_ylabel(yLabel)

		plt.show(block=False)

	def add(self, value):
		self.values.append(value)

		#remake the plot
		if self.plot != None:
			self.plot.remove()
		self.plot, = self.ax.plot(self.values, linestyle='-', color='b')

		plt.draw()

class Plotter:
	def __init__(self, fig, ax, inequalityFunc, dataset, colorbarLabel, x_range=(-100, 100), y_range=(-100, 100), resolution=100, onCloseFunction = None):
		self.fig = fig
		self.ax = ax
		self.x_range = x_range
		self.y_range = y_range
		self.resolution = resolution
		self.colorbarLabel = colorbarLabel
		
		if onCloseFunction != None:
			self.fig.canvas.mpl_connect('close_event', onCloseFunction)
		
		# Create coordinate grids
		x = np.linspace(x_range[0], x_range[1], resolution)
		y = np.linspace(y_range[0], y_range[1], resolution)
		self.X, self.Y = np.meshgrid(x, y)

		# Scatter plot
		self.plotScatter(dataset)
		
		# Initialize the plot
		self.inequalityPlot = None
		self.colorbar = None
		self.updateInequality(inequalityFunc)
		
		# Set up the plot
		self.ax.set_xlabel('x')
		self.ax.set_ylabel('y')

		#show (without blocking)
		plt.show(block=False)

	def updateInequality(self, inequalityFunc):
		#draw inequality
		self.drawInequality(inequalityFunc)
		
		#draw everything
		plt.draw()

	def drawInequality(self, inequalityFunc):
		# Clear previous plot
		if self.inequalityPlot is not None:
			# Remove all contour collections
			for contour in self.inequalityPlot.collections:
				contour.remove()

		if self.colorbar is not None:
			self.colorbar.remove()

		# Evaluate the inequality over the grid
		Z = np.zeros_like(self.X)

		# Due to more complex functions
		for i in range(self.X.shape[0]):
			for j in range(self.X.shape[1]):
				valueList = inequalityFunc((self.X[i, j], self.Y[i, j]))
				value = valueList[0] - valueList[1] #listToBool(valueList)
				Z[i, j] = value

		# Plot the inequality using contourf
		contour = self.ax.contourf(
			self.X, self.Y, Z,
			levels=20,
			cmap='RdYlGn',
			alpha=0.4
		)

		self.colorbar = self.fig.colorbar(contour)
		self.colorbar.set_label(self.colorbarLabel)
		self.inequalityPlot = contour

	def plotScatter(self, dataset):
		# Separate the points based on their boolean values
		greenPoints = []
		redPoints = []
		for datapoint in dataset:
			point = (datapoint.inputs[0], datapoint.inputs[1])
			if datapoint.pointColor == "green":
				greenPoints.append(point)
			else:
				redPoints.append(point)

		# Unpack the points into x and y coordinates
		green_x, green_y = zip(*greenPoints) if greenPoints else ([], [])
		red_x, red_y = zip(*redPoints) if redPoints else ([], [])

		# Create the scatter plot
		self.ax.scatter(green_x, green_y, color='green', label='False')
		self.ax.scatter(red_x, red_y, color='red', label='True')
