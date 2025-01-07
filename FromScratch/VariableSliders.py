import tkinter as tk
from tkinter import ttk
import threading
import numpy as np
import time

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
        #root.geometry("300x200")

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
                    from_=0,
                    to=1,
                    orient="horizontal",
                    command=lambda value, r=row, c=col: self.update_value(value, r, c),
                )
                slider.grid(row=row + 1, column=col + 1, padx=5, pady=5)
                
        root.mainloop()
    
    def update_value(self, value, row, col):
        self.values[row, col] = float(value)
        self.updateFunction(self.values)

