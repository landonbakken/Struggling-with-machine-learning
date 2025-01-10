import tkinter as tk
from tkinter import ttk
import numpy as np
import random
from MathThings import *

class SliderWindow:
    def __init__(self, numSliders, title, updateFunction, root, range = (-1, 1)):
        self.root = tk.Toplevel(root)
        self.windowTitle = title
        self.numSliders = numSliders
        self.updateFunction = updateFunction
        self.range = range

        self.buildWindow()

    def buildWindow(self):
        self.root.title(self.windowTitle)

        # Create a NumPy array to store slider values
        self.values = np.zeros(self.numSliders)

        # Create labels and sliders
        for idx in range(self.numSliders):
            slider_label = ttk.Label(self.root, text=f"Bias {idx}")
            slider_label.grid(row=0, column=idx, padx=5, pady=5)
            value = mapToRange(random.random(), (-1, 1), self.range)

            slider = ttk.Scale(
                self.root,
                from_=self.range[0],
                to=self.range[1],
                orient="horizontal",
                command=lambda value, i=idx: self.updateValue(value, i),
                value = value
            )
            slider.grid(row=1, column=idx, padx=5, pady=5)

            self.updateValue(value, idx)

    def updateValue(self, value, idx):
        self.values[idx] = float(value)
        self.updateFunction(self.values)

class SliderWindow2D:
    def __init__(self, rows, cols, title, updateFunction, root, range = (-1, 1)):
        self.root = tk.Toplevel(root)
        self.windowTitle = title
        self.rows = rows
        self.cols = cols
        self.updateFunction = updateFunction
        self.range = range

        self.buildWindow()

    def buildWindow(self):
        self.root.title(self.windowTitle)

        # Create a NumPy array to store slider values
        self.values = np.zeros((self.rows, self.cols))

        # Create labels for columns
        for col in range(self.cols):
            label = ttk.Label(self.root, text=f"Output {col}")
            label.grid(row=0, column=col + 1, padx=5, pady=5)

        # Create labels for rows and sliders
        for row in range(self.rows):
            row_label = ttk.Label(self.root, text=f"Input {row}")
            row_label.grid(row=row + 1, column=0, padx=5, pady=5)
            value = mapToRange(random.random(), (-1, 1), self.range)

            for col in range(self.cols):
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
        self.values[row, col] = float(value)
        self.updateFunction(self.values)

