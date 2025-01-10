import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create the data for the surface
x = np.linspace(-3, 3, 10)
y = np.linspace(-3, 3, 10)
X, Y = np.meshgrid(x, y)
Z = np.cos(1.5 * X) * np.sin(1.5 * Y) + np.cos(.4 * X)**2 + np.cos(.2 * Y)**2

# Coordinates of the point
point_x = 2
point_y = 3
point_z = np.sin(np.sqrt(point_x**2 + point_y**2))

# Create the figure and 3D axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=1)

# Plot the point
ax.scatter(point_x, point_y, point_z, color='red', s=100)

# Add labels and legend
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()

# Show the plot
plt.show()
