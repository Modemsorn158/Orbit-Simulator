import matplotlib.pyplot as plt
from state import Body, BodyState, SystemState

def plot_trajectory(
    dt: float,
    positions: list[tuple],
    source: BodyState,
    title: str
):
    """Plots the trajectory of a satellite based on its positions."""
    
    x_list, y_list = zip(*positions)
    plot, ax = plt.subplots()
    ax.plot(x_list, y_list, linestyle='-', color='b')
    body_circle = plt.Circle((source.position.x, source.position.y), source.body.radius, color='g', alpha=0.5)
    ax.add_artist(body_circle)
    plt.title(f'{title}; dt = {dt}')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.axis('equal')
    plt.grid()
    plt.show()
    
def plot_system_trajectory(
    dt: float,
    systems: list[SystemState],
    title: str,
    body_scale: float = 1,
    reference_point: int = None,
    display_list: list[int] = None
):
    """Plots the trajectory of every object in the system."""
    
    plot, ax = plt.subplots()
    final_system = systems[-1]
    if reference_point is not None:
        reference_position = final_system.body_states[reference_point].position
    for i in range(len(final_system.body_states)):
        if display_list:
            if i in display_list:
                pass
            else:
                continue
        state = final_system.body_states[i]
        x_list = []
        y_list = []
        for j in range(len(systems)):
            x = systems[j].body_states[i].position.x
            y = systems[j].body_states[i].position.y
            if reference_point is not None:
                reference_position_state = systems[j].body_states[reference_point].position
                x = x - reference_position_state.x
                y = y - reference_position_state.y
            x_list.append(x)
            y_list.append(y)
        ax.plot(x_list, y_list, linestyle='-')
        if reference_point is not None:
            ax.add_artist(plt.Circle((state.position.x - reference_position.x, state.position.y - reference_position.y), (state.body.radius * body_scale)))
            ax.text(state.position.x - reference_position.x, state.position.y - reference_position.y, state.body.name)
        else:
            ax.add_artist(plt.Circle((state.position.x, state.position.y), (state.body.radius * body_scale)))
            ax.text(state.position.x, state.position.y, state.body.name)
    plt.title(f'{title}; dt = {dt}; body size scale = {body_scale}')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.axis('equal')
    plt.grid()
    plt.show()
    
def plot_integrator_comparison(
    dt: float,
    positions1: list[tuple],
    positions2: list[tuple],
    source: BodyState,
    label1: str,
    label2: str,
    title: str
):
    """Plots the trajectories of two satellites for integrator comparison."""
    
    x_list1, y_list1 = zip(*positions1)
    x_list2, y_list2 = zip(*positions2)
    plot, ax = plt.subplots()
    ax.plot(x_list1, y_list1, linestyle='-', color='b', label=label1)
    ax.plot(x_list2, y_list2, linestyle='-', color='r', label=label2)
    body_circle = plt.Circle((source.position.x, source.position.y), source.body.radius, color='g', alpha=0.5)
    ax.add_artist(body_circle)
    plt.title(f'{title}; dt = {dt}')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.axis('equal')
    plt.grid()
    plt.legend()
    plt.show()
    
def plot_diagnostic_comparison(
    dt: float,
    changes1: list[float],
    changes2: list[float],
    label1: str,
    label2: str,
    title: str,
    y_label: str
):
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
    
def plot_table(
    headers: list[str],
    data: list[list[str]],
    title: str
):
    """Plots a table with the given headers and data."""
    
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=data, colLabels=headers, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    plt.title(title)
    plt.show()