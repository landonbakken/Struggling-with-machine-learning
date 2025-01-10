import random
import tkinter as tk
import pickle

from SimpleModel import *
from Plotter import *
from MathThings import *
from ModelVisualizer import *
from VariableSliders import *

radius = 60
x_range = (0, 1)
y_range = (0, 1)

memoryFile = "FromScratch/Memory/memory.pickle"

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

def saveMemory():
	weights, biases = model.getValues()
	dimentions = model.dimentions

	variables = [dimentions, weights, biases]
	with open(memoryFile, 'wb') as f:
		pickle.dump(variables, f)

	print("Saved memory to files")

def loadMemory():
	with open(memoryFile, 'rb') as f:
		variables = pickle.load(f)
	dimentions, weights, biases = variables
	
	if dimentions == model.dimentions:
		model.setValues(weights, biases)

		print("Loaded memory from files")
	else:
		print("Dimentions don't match ):")

def randomizeValues():
	model.randomizeValues()
	
#create model
dimentions = [2, 3, 2]
model = Model(dimentions, costFunction=costFunction)

#main window
root = tk.Tk()
root.title("Controls and info")
costLabel = tk.Label(root, text="Cost: N/A")
costLabel.pack()
numCorrectLabel = tk.Label(root, text="Correct: N/A")
numCorrectLabel.pack()

#save/load buttons
button1 = tk.Button(root, text="Save Memory", command=saveMemory)
button1.pack(pady=10)
button2 = tk.Button(root, text="Load Memory", command=loadMemory)
button2.pack(pady=10)
button3 = tk.Button(root, text="Randomize", command=randomizeValues)
button3.pack(pady=10)

#loop through layers
for layerIndex, layer in enumerate(model.layers):
	#create name
	layerName = f"Hidden Layer {layerIndex}" if layerIndex != len(dimentions) - 1 else "Ouput "

	#create slider windows
	layer.biasSliderWindow = SliderWindow(layer.biases, layerName + " Biases", layer.setBiases, root, range=(-10, 10))
	layer.weightSliderWindow = SliderWindow(layer.weights, layerName + " Weights", layer.setWeights, root, range=(-10, 10))

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