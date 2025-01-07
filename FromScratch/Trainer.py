from SimpleModel import *
from Plotter import *
import time

#settings
dimentions = [2, 3, 2]

#create model
plotter = InequalityPlotter()
model = Model(dimentions, plotter, False)

plt.show()