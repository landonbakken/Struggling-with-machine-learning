from SimpleModel import *
from Plotter import *
import random
import tkinter as tk

radius = 60
decisionLine=.2
x_range = (0, 1)
y_range = (0, 1)

def randomPointsWithCondition(num_points, condition, x_range=(-100, 100), y_range=(-100, 100)):
	dataPoints = []
	for _ in range(num_points):
		x = random.uniform(*x_range)
		y = random.uniform(*y_range)
		newDataPoint = Datapoint([x, y], condition)
		dataPoints.append(newDataPoint)
	return dataPoints

def testInequality(points):
	x, y = points
	result = x < .5#** 2 + y ** 2 < radius**2 #circle with radius
	return [1, 0] if result else [0, 1] #convert to list format

def stop(event):
	exit()
	
def costFunction(calculated, expected):
	error = calculated - expected
	return abs(error) #emphasises larger errors (and makes positive)

#create model
dimentions = [2, 3, 2]
model = Model(dimentions, costFunction=costFunction)

#main window
root = tk.Tk()
root.title("Controls")
root.geometry("300x200")
costLabel = tk.Label(root, text="Cost: N/A")
costLabel.pack()
numCorrectLabel = tk.Label(root, text="Correct: N/A")
numCorrectLabel.pack()

ranges = [(-10, 10), (-2, 2), (-5, 5), (-10, 10)]
#loop through layers
for layerIndex, layer in enumerate(model.layers):
	#create name
	layerName = f"Hidden Layer {layerIndex} Weights" if layerIndex != len(dimentions) - 1 else "Ouput Weights"

	#create slider windows
	biasSliders = SliderWindow(layer.numOutputs, layerName + " Biases", layer.setBiases, root, range=ranges[layerIndex])
	weightSliders = SliderWindow2D(layer.numInputs, layer.numOutputs, layerName + " Weights", layer.setWeights, root, range=ranges[layerIndex + 1])

#get a dataset
dataset = randomPointsWithCondition(100, testInequality, x_range=x_range, y_range=y_range)
totalDatapoints = len(dataset)

#create plot
plotter = Plotter(model.calculate, dataset, onCloseFunction=stop, decisionLine=decisionLine, x_range=x_range, y_range=y_range)

while True:
	#update main gui
	cost, numCorrect = model.getTotalCost(dataset)
	costLabel.config(text=f"Cost: {cost}")
	numCorrectLabel.config(text=f"Correct: {numCorrect}/{totalDatapoints}")
	
	#update sliders
	root.update_idletasks()
	root.update()

	#update plotter
	plotter.updateInequality(model.calculate)

	#delay so cpu doesn't die
	plt.pause(.01)