import matplotlib.pyplot as plt
import numpy as np

class InequalityPlotter:
    def plotInequality(self, inequality):
        #clear past plot
        plt.clf()

        # Create a grid of x, y points
        x = np.linspace(-self.bound, self.bound, self.resolution)  # x values from -10 to 10
        y = np.linspace(-self.bound, self.bound, self.resolution)  # y values from -10 to 10
        X, Y = np.meshgrid(x, y)  # Create a grid from x and y values
        
        # Apply the condition function to each point in the grid
        Z = np.array([[inequality([xi, yi]) for xi, yi in zip(x_row, y_row)] for x_row, y_row in zip(X, Y)])
        
        # Create a plot using the result of the condition function
        plt.contourf(X, Y, Z, levels=[-0.1, 0.5, 1.1], colors=['red', 'green'], alpha=1)
        
        # Show the plot
        plt.show()

    # Call the function to plot the inequality graph
    def __init__(self, bound = 100, resoltion = 150):
        self.bound = bound
        self.resolution = resoltion
