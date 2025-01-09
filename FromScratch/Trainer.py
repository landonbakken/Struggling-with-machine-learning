from SimpleModel import *
from Plotter import *
import random
import time
import tkinter as tk

radius = 60

def generate_random_points(num_points, condition, x_range=(-100, 100), y_range=(-100, 100)):
	points = []
	for _ in range(num_points):
		x = random.uniform(*x_range)
		y = random.uniform(*y_range)
		points.append((x, y, condition((x, y))))
	return points

def testInequality(point):
	x, y = point
	return x ** 2 + y ** 2 < radius**2 #circle with radius

def stop(event):
	exit()

#create model
dimentions = [2, 3, 2]
model = Model(dimentions)

#main window
root = tk.Tk()
root.title("Controls")

#loop through layers
for layerIndex, layer in enumerate(model.layers):
	#create name
	layerName = f"Hidden Layer {layerIndex} Weights" if layerIndex != len(dimentions) - 1 else "Ouput Weights"

	#create slider windows
	biasSliders = SliderWindow(layer.numOutputs, layerName + " Biases", layer.setBiases, root)
	weightSliders = SliderWindow2D(layer.numInputs, layer.numOutputs, layerName + " Weights", layer.setWeights, root)

#get a dataset
dataset = generate_random_points(100, testInequality)

#create plot
plotter = Plotter(model.calculate, dataset, onCloseFunction=stop)

while True:
	#update sliders
	root.update_idletasks()
	root.update()

	#update plotter
	plotter.updateInequality(model.calculate)

	#delay so cpu doesn't die
	plt.pause(.1)