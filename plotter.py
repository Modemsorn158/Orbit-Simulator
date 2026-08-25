import matplotlib.pyplot as plt
from constants import EARTH_RADIUS

def plot_trajectory(dt, positions):
    """Plots the trajectory of a satellite based on its positions."""
    
    x_list, y_list = zip(*positions)
    plot, ax = plt.subplots()
    ax.plot(x_list, y_list, linestyle='-', color='b')
    earth_circle = plt.Circle((0, 0), EARTH_RADIUS, color='g', alpha=0.5)
    ax.add_artist(earth_circle)
    plt.title(f'Trajectory Plot; dt = {dt}')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.axis('equal')
    plt.grid()
    plt.show()
    
def plot_integrator_comparison(dt, positions1, positions2, label1, label2):
    """Plots the trajectories of two satellites for integrator comparison."""
    
    x_list1, y_list1 = zip(*positions1)
    x_list2, y_list2 = zip(*positions2)
    plot, ax = plt.subplots()
    ax.plot(x_list1, y_list1, linestyle='-', color='b', label=label1)
    ax.plot(x_list2, y_list2, linestyle='-', color='r', label=label2)
    earth_circle = plt.Circle((0, 0), EARTH_RADIUS, color='g', alpha=0.5)
    ax.add_artist(earth_circle)
    plt.title(f'Integrator Comparison; dt = {dt}')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.axis('equal')
    plt.grid()
    plt.legend()
    plt.show()
    
def plot_diagnostic_comparison(dt, changes1, changes2, label1, label2, title, y_label):
    """Plots the relative change in a diagnostic quantity for two integrators."""
    
    time_steps = [i * dt for i in range(len(changes1))]
    plot, ax = plt.subplots()
    ax.plot(time_steps, changes1, linestyle='-', color='b', label=label1)
    ax.plot(time_steps, changes2, linestyle='-', color='r', label=label2)
    plt.title(f'{title}; dt = {dt}')
    plt.xlabel('Time (s)')
    plt.ylabel(f'{y_label}')
    plt.grid()
    plt.legend()
    plt.show()