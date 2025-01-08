from SimpleModel import *
from Plotter import *
import random
import time

radius = 1

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

#create model
dimentions = [2, 3, 2]
model = Model(dimentions, False)

#get a dataset
dataset = generate_random_points(100, testInequality)

#create plot
plotter = Plotter(model.calculate, dataset)

while True:
    plotter.updateInequality(testInequality)
    radius += 1
    plt.pause(.1)