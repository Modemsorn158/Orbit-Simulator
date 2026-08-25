import matplotlib.pyplot as plt
from constants import EARTH_RADIUS

def plot_trajectory(positions):
    """Plots the trajectory of a satellite based on its positions."""
    
    x_list, y_list = zip(*positions)
    plot, ax = plt.subplots()
    ax.plot(x_list, y_list, linestyle='-', color='b')
    earth_circle = plt.Circle((0, 0), EARTH_RADIUS, color='g', alpha=0.5)
    ax.add_artist(earth_circle)
    plt.title('Trajectory Plot')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.axis('equal')
    plt.grid()
    plt.show()