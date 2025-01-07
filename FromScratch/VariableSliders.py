import tkinter as tk
from tkinter import ttk
import numpy as np
import threading
import random

class SliderWindow:
    def __init__(self, numSliders, title, updateFunction):
        self.windowTitle = title
        self.numSliders = numSliders
        self.updateFunction = updateFunction

        tk_thread = threading.Thread(target=self.buildWindow, daemon=True)
        tk_thread.start()

    def buildWindow(self):
        root = tk.Tk()
        root.title(self.windowTitle)

        # Create a NumPy array to store slider values
        self.values = np.zeros(self.numSliders)

        # Create labels and sliders
        for idx in range(self.numSliders):
            slider_label = ttk.Label(root, text=f"Bias {idx}")
            slider_label.grid(row=0, column=idx, padx=5, pady=5)

            slider = ttk.Scale(
                root,
                from_=-1,
                to=1,
                orient="horizontal",
                command=lambda value, i=idx: self.updateValue(value, i),
                value=random.random()
            )
            slider.grid(row=1, column=idx, padx=5, pady=5)

        root.mainloop()

    def updateValue(self, value, idx):
        self.values[idx] = float(value)
        self.updateFunction(self.values)

class SliderWindow2D:
    def __init__(self, rows, cols, title, updateFunction):
        self.windowTitle = title
        self.rows = rows
        self.cols = cols
        self.updateFunction = updateFunction

        tk_thread = threading.Thread(target=self.buildWindow, daemon=True)
        tk_thread.start()

    def buildWindow(self):
        root = tk.Tk()
        root.title(self.windowTitle)

        # Create a NumPy array to store slider values
        self.values = np.zeros((self.rows, self.cols))

        # Create labels for columns
        for col in range(self.cols):
            label = ttk.Label(root, text=f"Output {col}")
            label.grid(row=0, column=col + 1, padx=5, pady=5)

        # Create labels for rows and sliders
        for row in range(self.rows):
            row_label = ttk.Label(root, text=f"Input {row}")
            row_label.grid(row=row + 1, column=0, padx=5, pady=5)

            for col in range(self.cols):
                slider = ttk.Scale(
                    root,
                    from_=-1,
                    to=1,
                    orient="horizontal",
                    command=lambda value, r=row, c=col: self.updateValue(value, r, c),
                    value=random.random()
                )
                slider.grid(row=row + 1, column=col + 1, padx=5, pady=5)

        root.mainloop()
    
    def updateValue(self, value, row, col):
        self.values[row, col] = float(value)
        self.updateFunction(self.values)

