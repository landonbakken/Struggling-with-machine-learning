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
x_range = (-1, 1)
y_range = (-1, 1)

memoryPath = "FromScratch/Memory/"
memoryFile = memoryPath + "memory.pickle"

#for getting learn rate
learnRate = 0 #just an initial, this is overwritten
learnRateUpdateRate = .1 #percent
biasLearnRateRatio = .4 #this is so that the biases don't overshadow the weights

datasetSize = 700 * 40
batchSize = int(datasetSize/700) #each batch is one epoch
fps = 1 #attempted
dimentions = [2, 8, 8, 2]

def costToLearnRate(cost):
	cost = min(cost, 1) #limit to 1
	learnRate = clamp(100 * cost**1.5, .03, 15)
	return learnRate

if not os.path.exists(memoryPath):
    os.makedirs(memoryPath)
    print(f"Folder '{memoryPath}' created.")

def randomPointsWithCondition(num_points, condition, x_range, y_range):
	dataPoints = np.empty(num_points, dtype=Datapoint)
	for i in range(num_points):
		x = random.uniform(*x_range)
		y = random.uniform(*y_range)
		newDataPoint = Datapoint([x, y], condition)
		dataPoints[i] = newDataPoint
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
model = Model(dimentions, costFunction, leakyReluFunction, sigmoidFunction)

#main window
root = tk.Tk()
root.title("Controls and info")
costLabel = tk.Label(root, text="Cost: N/A")
costLabel.pack()
learnRateLabel = tk.Label(root, text="Learn Rate: N/A")
learnRateLabel.pack()
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
dataset = randomPointsWithCondition(datasetSize, testInequality, x_range, y_range)
totalDatapoints = len(dataset)

#create plots
fig, axs = plt.subplots(2, 2, figsize=(14, 11))

plotter = Plotter(fig, axs[1][0], model.calculate, dataset, "False------------------->True", onCloseFunction=stop, x_range=x_range, y_range=y_range)
costPlot = IncrementingScatter(fig, axs[1][1], "Learn Cycles", "Cost", (0, 1))
learnRatePlot = IncrementingScatter(fig, axs[0][1], "Learn Cycles", "Learn Rate", (0, 1))
fig.tight_layout() #adjust layout

visualizer = ModelVisualizer(model)

while True:
	#learn!
	guiUpdateTime = time.time() + 1/fps
	learnCycles = 0
	while guiUpdateTime - time.time() > 0:
		#get a new random datapoint batch
		batch = np.random.choice(dataset, size=batchSize, replace=False)

		#learn, and get the cost
		cost = model.learn(batch, learnRate, learnRate * biasLearnRateRatio)

		#get new learn rate
		newLearnRate = costToLearnRate(cost)
		learnRate = rollingMeanRatio(newLearnRate, learnRate, learnRateUpdateRate)

		learnCycles += 1

	#update main gui
	costLabel.config(text=f"Cost: {cost:.5g}")
	learnRateLabel.config(text=f"Learn Rate: {learnRate:.5g}")
	learnCyclesLabel.config(text=f"Learn Cycles per frame: {learnCycles}")

	#add to plots
	costPlot.add(cost)
	learnRatePlot.add(learnRate)
	
	#update sliders
	root.update_idletasks()
	root.update()

	#update plotter
	plotter.updateInequality(model.calculate)

	#show updated model
	visualizer.update()