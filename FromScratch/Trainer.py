from SimpleModel import *
from Plotter import *
import random
import tkinter as tk
from MathThings import *
from ModelVisualizer import *

radius = 60
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

def stop(event):
	exit()
	
#create model
dimentions = [2, 2]
model = Model(dimentions, costFunction=costFunction)

#main window
root = tk.Tk()
root.title("Controls")
root.geometry("300x200")
costLabel = tk.Label(root, text="Cost: N/A")
costLabel.pack()
numCorrectLabel = tk.Label(root, text="Correct: N/A")
numCorrectLabel.pack()

#loop through layers
for layerIndex, layer in enumerate(model.layers):
	#create name
	layerName = f"Hidden Layer {layerIndex} Weights" if layerIndex != len(dimentions) - 1 else "Ouput Weights"

	#create slider windows
	biasSliders = SliderWindow(layer.numOutputs, layerName + " Biases", layer.setBiases, root, range=(-10, 10))
	weightSliders = SliderWindow2D(layer.numInputs, layer.numOutputs, layerName + " Weights", layer.setWeights, root, range=(-10, 10))

#get a dataset
dataset = randomPointsWithCondition(100, testInequality, x_range=x_range, y_range=y_range)
totalDatapoints = len(dataset)

#create plot
plotter = Plotter(model.calculate, dataset, onCloseFunction=stop, x_range=x_range, y_range=y_range)

visualizer = ModelVisualizer(model)

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

	#show updated model
	visualizer.update()

	#if nothing else is in this loop, add this
	#plt.pause(.01)