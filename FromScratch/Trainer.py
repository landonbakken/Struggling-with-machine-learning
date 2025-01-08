from SimpleModel import *
from Plotter import *
import random

def generate_random_points(num_points, condition, x_range=(-100, 100), y_range=(-100, 100)):
    points = []
    for _ in range(num_points):
        x = random.uniform(*x_range)
        y = random.uniform(*y_range)
        points.append((x, y, condition(x, y)))
    return points

def testInequality(x, y):
    return x ** 2 + y ** 2 < 50**2 #circle with radius 50

#create model
dimentions = [2, 3, 2]
model = Model(dimentions, False)

#get a dataset
dataset = generate_random_points(50, testInequality)

#create plot
plotter = CombinedPlot(model.calculate, dataset)

input()