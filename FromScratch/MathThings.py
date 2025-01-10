def clamp(value, minValue, maxValue):
    return max(min(value, maxValue), minValue)

def listToBool(list):
	return max(list) == list[0]

def boolToList(bool):
	return [1, 0] if bool else [0, 1]