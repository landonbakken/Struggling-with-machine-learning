import tkinter as tk
from tkinter import ttk
import numpy as np
import random
from MathThings import *

#can make a 1d or 2d slider grid
class SliderWindow:
    def __init__(self, initialValues, title, updateFunction, root, range = (-1, 1)):
        self.root = tk.Toplevel(root)
        self.windowTitle = title
        self.shape = initialValues.shape
        self.dimentions = len(self.shape)
        if self.dimentions == 1:
            self.shape = (self.shape[0], 1)

        self.updateFunction = updateFunction
        self.range = range

        self.buildWindow(initialValues)

    def buildWindow(self, initialValues):
        self.root.title(self.windowTitle)

        # Create a NumPy array to store slider values
        self.values = initialValues.copy()

        # Create labels for columns
        for col in range(self.shape[1]):
            label = ttk.Label(self.root, text=f"Output {col}")
            label.grid(row=0, column=col + 1, padx=5, pady=5)

        # Create labels for rows and sliders
        for row in range(self.shape[0]):
            row_label = ttk.Label(self.root, text=f"Input {row}")
            row_label.grid(row=row + 1, column=0, padx=5, pady=5)
            value = mapToRange(random.random(), (-1, 1), self.range)

            for col in range(self.shape[1]):
                slider = ttk.Scale(
                    self.root,
                    from_=self.range[0],
                    to=self.range[1],
                    orient="horizontal",
                    command=lambda value, r=row, c=col: self.updateValue(value, r, c),
                    value=value
                )
                slider.grid(row=row + 1, column=col + 1, padx=5, pady=5)

                #initial update
                self.updateValue(value, row, col)
    
    def updateValue(self, value, row, col):
        if self.dimentions == 1: #1D
            self.values[row] = float(value)
        else: #2D
            self.values[row, col] = float(value)
        self.updateFunction(self.values)

