import tkinter as tk
from tkinter import ttk
import threading


class sliderWindow:
    # Create Tkinter window
    def createTkWindow(self):
        root = tk.Tk()
        root.title(self.windowTitle)

        def updateValue(var_name, slider):
            self.sliderValues[var_name] = slider.get()
            self.updateFunction(self.sliderValues)

        for i, (label, var_name, min_val, max_val) in enumerate(self.sliderConfig):
            tk.Label(root, text=label).grid(row=i, column=0)
            slider = ttk.Scale(root, from_=min_val, to=max_val, orient=tk.HORIZONTAL)
            slider.set(self.sliderValues[var_name])
            slider.grid(row=i, column=1)
            slider.bind("<Motion>", lambda e, var_name=var_name, slider=slider: updateValue(var_name, slider))

        root.mainloop()

    #tkinter window
    def __init__(self, windowTitle, sliderValues, sliderConfig, updateFunction):
        self.windowTitle = windowTitle

        # Variables to be controlled by sliders
        self.sliderValues = sliderValues
        self.sliderConfig = sliderConfig

        #function that is called when slider values are changed
        self.updateFunction = updateFunction

        #start window in different thread
        tk_thread = threading.Thread(target=self.createTkWindow, daemon=True)
        tk_thread.start()