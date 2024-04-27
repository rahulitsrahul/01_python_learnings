import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# Create a figure and axis
fig, ax = plt.subplots()

# Set the axis limits
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.5, 1.5)

# Initialize an empty line object (this will be updated in the animation)
line, = ax.plot([], [], lw=2)

# Function to initialize the plot
def init():
    line.set_data([], [])
    return line,

# Function to update the plot for each frame of the animation
def update(frame):
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x + frame*0.1)  # Vary the frequency for animation
    line.set_data(x, y)
    return line,

# Create the animation
ani = FuncAnimation(fig, update, frames=100, init_func=init, blit=True)

# If you want to save the animation to a file, you can use ani.save('filename.mp4')

# Show the animation
plt.show()