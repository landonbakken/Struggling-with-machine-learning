import pygame
import random
import time

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#point settings
POINT_RADIUS = 5
POINT_COLOR = WHITE

#slope, numbers are in coordinate
SLOPE_STEP = .01
SLOPE_DISTANCE = 1
LEARN_RATE = 50
SLOPE_COLOR = WHITE

# Dimentionas
WIDTH = 800
HEIGHT = 600

#plot settings
GRAPH_COLOR=WHITE
x_range = (-3, 3)
y_range = (-3, 3)


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gradient Decent")

# Define the function to graph
def mathFunction(x):
	return .2 * x**4 + .1 * x**3 - x**2

def pixelToCoord(value, scale, windowSize):
	return (value - windowSize / 2) / scale

def coordToPixel(value, scale, windowSize):
	return int(windowSize / 2 - value * scale)

def xPixelToPoint(x_pixel, lineFunction):
	# Convert pixel to coordinate
	x_coord = pixelToCoord(x_pixel, x_scale, WIDTH)

	#calculate Y
	y_coord = lineFunction(x_coord)

	# Convert coordinate to pixel
	y_pixel = coordToPixel(y_coord, y_scale, HEIGHT)

	return (x_pixel, y_pixel)

def drawFunction(lineFunction):
	# loop through pixels
	prev_point = None
	for x_pixel in range(WIDTH):
		point_pixel = xPixelToPoint(x_pixel, lineFunction)

		# Draw a line from the previous point to the current point
		if prev_point is not None and 0 <= point_pixel[1] < HEIGHT:
			pygame.draw.line(screen, GRAPH_COLOR, prev_point, point_pixel, 1)
		
		# Update previous point
		prev_point = point_pixel

def drawPoint(x_pixel, lineFunction):
	point_pixel = xPixelToPoint(x_pixel, lineFunction)

	# Draw point
	pygame.draw.circle(screen, POINT_COLOR, point_pixel, POINT_RADIUS)

def getSlope(x_pixel, lineFunction):
	# Convert pixel to coordinate
	x_coord = pixelToCoord(x_pixel, x_scale, WIDTH)

	#calculate Y
	y_coord_1 = lineFunction(x_coord)
	y_coord_2 = lineFunction(x_coord + SLOPE_STEP)

	#calculate slope
	slope = (y_coord_2 - y_coord_1)/SLOPE_STEP
	
	return slope

def drawSlope(x_pixel, lineFunction, slope):
	# Convert pixel to coordinate
	x_coord = pixelToCoord(x_pixel, x_scale, WIDTH)
	y_intercept = lineFunction(x_coord)

	#get points
	x_pixel_1 = coordToPixel(x_coord + SLOPE_DISTANCE, x_scale, WIDTH)
	x_pixel_2 = coordToPixel(x_coord - SLOPE_DISTANCE, x_scale, WIDTH)
	y_pixel_1 = coordToPixel(slope * SLOPE_DISTANCE + y_intercept, y_scale, HEIGHT)
	y_pixel_2 = coordToPixel(slope * -SLOPE_DISTANCE + y_intercept, y_scale, HEIGHT)

	pygame.draw.line(screen, POINT_COLOR, (WIDTH - x_pixel_1, y_pixel_1), (WIDTH - x_pixel_2, y_pixel_2))

	return slope

def stepX(currentX, slope, rate):
	return currentX - slope * rate

x_scale = WIDTH / (x_range[1] - x_range[0])
y_scale = HEIGHT / (y_range[1] - y_range[0])

# Main loop
running = True
pointX = random.randrange(0, WIDTH)
slope = 0
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# Clear the screen
	screen.fill(BLACK)

	#math
	pointX = stepX(pointX, slope, LEARN_RATE)
	slope = getSlope(pointX, mathFunction)

	#draw things
	drawFunction(mathFunction)
	drawPoint(pointX, mathFunction)
	drawSlope(pointX, mathFunction, slope)
	
	# Update the display
	pygame.display.flip()

	#pause
	time.sleep(.5)

	#reset if hit the bottom
	if abs(slope) <= .001:
		pointX = random.randrange(0, WIDTH)

# Quit Pygame
pygame.quit()