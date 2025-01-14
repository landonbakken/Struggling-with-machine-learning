import pickle
import os

memoryPath = "FromScratch/Memory/"

#create the memory folder if it doesnt exist
if not os.path.exists(memoryPath):
    os.makedirs(memoryPath)
    print(f"Folder '{memoryPath}' created.")

def saveModels(path, models):
	variables = []
	for model in models:
		weights, biases = model.getValues()
		dimentions = model.dimentions

		variables.append([dimentions, weights, biases])

	with open(path, 'wb') as f:
		pickle.dump(variables, f)

def loadModels(path, models):
	with open(path, 'rb') as f:
		variables = pickle.load(f)

	for modelIndex, model in enumerate(models):
		dimentions, weights, biases = variables[modelIndex]
		
		if dimentions == model.dimentions:
			model.setValues(weights, biases)
		else:
			print("Dimentions don't match ):")
			return
		
def saveModel(path, model):
	weights, biases = model.getValues()
	dimentions = model.dimentions

	variables = [dimentions, weights, biases]
	with open(path, 'wb') as f:
		pickle.dump(variables, f)

	print("Saved memory to files")

def loadModel(path, model):
	with open(path, 'rb') as f:
		variables = pickle.load(f)
	dimentions, weights, biases = variables
	
	if dimentions == model.dimentions:
		model.setValues(weights, biases)

		print("Loaded memory from files")
	else:
		print("Dimentions don't match ):")