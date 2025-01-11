import random
import tkinter as tk
import pickle
import os
import time

from SimpleModel import *
from Plotter import *
from MathThings import *
from ModelVisualizer import *
from VariableSliders import *

radius = 60
x_range = (0, 1)
y_range = (0, 1)

memoryPath = "FromScratch/Memory/"
memoryFile = memoryPath + "memory.pickle"

#for getting learn rate
learnRate = 10

datasetSize = 300
batchSize = 50
fps = 15
dimentions = [2, 3, 2]

def costToLearnRate(cost):
	cost = min(cost, 1) #limit to 1
	learnRate = clamp(100 * cost**1.4, .1, 15)
	return learnRate

if not os.path.exists(memoryPath):
    os.makedirs(memoryPath)
    print(f"Folder '{memoryPath}' created.")

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
	costPlot.values = []
	
#create model
model = Model(dimentions, costFunction, activationFunction)

#main window
root = tk.Tk()
root.title("Controls and info")
costLabel = tk.Label(root, text="Cost: N/A")
costLabel.pack()
numCorrectLabel = tk.Label(root, text="Correct: N/A")
numCorrectLabel.pack()
learnCyclesLabel = tk.Label(root, text="Learn Cycles per frame: N/A")
learnCyclesLabel.pack()

#save/load buttons
button1 = tk.Button(root, text="Save Memory", command=saveMemory)
button1.pack(pady=10)
button2 = tk.Button(root, text="Load Memory", command=loadMemory)
button2.pack(pady=10)
button3 = tk.Button(root, text="Randomize", command=randomizeValues)
button3.pack(pady=10)

##loop through layers
#for layerIndex, layer in enumerate(model.layers):
#	#create name
#	layerName = f"Hidden Layer {layerIndex}" if layerIndex != len(dimentions) - 1 else "Ouput "
#
#	#create slider windows
#	layer.biasSliderWindow = SliderWindow(layer.biases, layerName + " Biases", layer.setBiases, root, range=(-10, 10))
#	layer.weightSliderWindow = SliderWindow(layer.weights, layerName + " Weights", layer.setWeights, root, range=(-10, 10))

#get a dataset
dataset = randomPointsWithCondition(datasetSize, testInequality, x_range=x_range, y_range=y_range)
totalDatapoints = len(dataset)

#create plots
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

plotter = Plotter(fig, axs[0], model.calculate, dataset, onCloseFunction=stop, x_range=x_range, y_range=y_range)
costPlot = IncrementingScatter(fig, axs[1])
fig.tight_layout() #adjust layout

visualizer = ModelVisualizer(model)

while True:
	#learn!
	guiUpdateTime = time.time() + 1/fps
	learnCycles = 0
	while guiUpdateTime - time.time() > 0:
		batch = np.random.choice(dataset, size=batchSize, replace=False)
		model.learn(batch, learnRate)
		learnCycles += 1


	#update main gui
	cost, numCorrect = model.getTotalCost(dataset)
	costLabel.config(text=f"Cost: {cost}")
	numCorrectLabel.config(text=f"Correct: {numCorrect}/{totalDatapoints}")
	learnCyclesLabel.config(text=f"Learn Cycles per frame: {learnCycles}")

	#add to plot
	costPlot.add(cost)
	
	#update sliders
	root.update_idletasks()
	root.update()

	#update plotter
	plotter.updateInequality(model.calculate)

	#show updated model
	visualizer.update()

	#get new learn rate
	learnRate = costToLearnRate(cost)
	print(learnRate)