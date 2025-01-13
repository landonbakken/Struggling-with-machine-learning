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

#plot/data ranges
x_range = (-1, 1)
y_range = (-1, 1)

#memory paths
memoryPath = "FromScratch/Memory/"
memoryFile = memoryPath + "memory.pickle"

#create the memory folder if it doesnt exist
if not os.path.exists(memoryPath):
    os.makedirs(memoryPath)
    print(f"Folder '{memoryPath}' created.")

#model settings
learnRateUpdateRate = .1 #percent, how fast the update rate changes
biasLearnRateRatio = .4 #this is so that the biases don't overshadow the weights
learnRateRange = (.03, 15)
dimentions = [2, 10, 10, 2] #of the model

#data settings
datasetSize = 700 * 40
batchSize = int(datasetSize/700) #each batch is one epoch (kind of useless right now, but helpfull in the future)

#other settings
fps = 1 #attempted

#relates cost to learn rate
#the idea is that as the cost goes down, it slows down the learning, letting the model really zero in on the solution
def costToLearnRate(cost):
	learnRate = 100 * cost**1.5
	learnRate = clamp(learnRate, learnRateRange[0], learnRateRange[1])
	return learnRate

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
	global learnRate

	with open(memoryFile, 'rb') as f:
		variables = pickle.load(f)
	dimentions, weights, biases = variables
	
	if dimentions == model.dimentions:
		model.setValues(weights, biases)

		print("Loaded memory from files")
	else:
		print("Dimentions don't match ):")

	#resets plots and makes sure it doesnt mess up stuff with a big learn rate
	learnRate = 0
	costPlot.values = []
	learnRatePlot.values = []

def randomizeValues():
	model.randomizeValues()
	costPlot.values = []
	learnRatePlot.values = []
	
#create model
model = Model(dimentions, costFunction, leakyReluFunction, sigmoidFunction)

#main window
root = tk.Tk()
root.title("Controls and info")
costLabel = tk.Label(root, text="Cost: N/A")
costLabel.pack(pady=10)
learnRateLabel = tk.Label(root, text="Learn Rate: N/A")
learnRateLabel.pack(pady=10)
learnCyclesLabel = tk.Label(root, text="Learn Cycles per frame: N/A")
learnCyclesLabel.pack(pady=10)

#save/load buttons
button1 = tk.Button(root, text="Save Memory", command=saveMemory)
button1.pack(pady=10)
button2 = tk.Button(root, text="Load Memory", command=loadMemory)
button2.pack(pady=10)
button3 = tk.Button(root, text="Randomize", command=randomizeValues)
button3.pack(pady=10)

#slider windows
#for layerIndex, layer in enumerate(model.layers):
#	#create name
#	layerName = f"Hidden Layer {layerIndex}" if layerIndex != len(dimentions) - 1 else "Ouput "
#
#	#create slider windows
#	layer.biasSliderWindow = SliderWindow(layer.biases, layerName + " Biases", layer.setBiases, root, range=(-10, 10))
#	layer.weightSliderWindow = SliderWindow(layer.weights, layerName + " Weights", layer.setWeights, root, range=(-10, 10))

#make the dataset
dataset = randomPointsWithCondition(datasetSize, testInequality, x_range, y_range)
totalDatapoints = len(dataset)

#matplotlib window
fig, axs = plt.subplots(2, 2, figsize=(14, 11))

#create plots
plotter = Plotter(fig, axs[1][0], model.calculate, dataset, "False------------------->True", onCloseFunction=stop, x_range=x_range, y_range=y_range)
costPlot = IncrementingScatter(fig, axs[1][1], "Learn Cycles", "Cost", (0, 1))
learnRatePlot = IncrementingScatter(fig, axs[0][1], "Learn Cycles", "Learn Rate", (0, learnRateRange[1]))

#adjust layout
fig.tight_layout()

#create visualizer
pygame.init()
visualizer = ModelVisualizer(model, ax=axs[0, 0])

learnRate = learnRateRange[1]
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