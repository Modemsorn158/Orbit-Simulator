from Physics import gravitational_acceleration, euler_step, specific_energy, specific_angular_momentum, simulate
from Physics import mu_Earth, r_Earth, r0, vc, ve
from math import sqrt
import random as random
import matplotlib.pyplot as plt

print(euler_step(7000000, 0, 0, 7500, 1))

def show_trajectory(positions, test_number):
    x, y = zip(*positions)

    fig, ax = plt.subplots()
    ax.scatter(x, y, s=2, color='blue', label='Trajectory')
    ax.set_aspect('equal')
    ax.set_title("Test Number "+str(test_number))
    
    plt.show()

def show_energy_graph(energies, dt, test_number):
    x = [i*dt for i in range(len(energies))]
    y = energies

    fig, ax = plt.subplots()
    ax.plot(x, y, linewidth=2)
    ax.set_title("Test Number "+str(test_number))
    plt.xlabel("Time (s)")
    plt.ylabel("Specific Orbital Energy (J/kg)")

    plt.show()

def run_validation(test_number, initial_velocity, dt, steps):
    print("TEST UNIT "+str(test_number)+" : dt="+str(dt)+" steps="+str(steps))

    result, energies, angular_momenta = simulate(7000000, 0, 0, initial_velocity, dt, steps)    

    e1 = energies[0]
    en = energies[-1]
    de = abs(en-e1)
    pe = ((en-e1)/abs(e1))*100
    print("Initital energy : "+str(e1))
    print("Final energy : "+str(en))
    print("Energy difference : "+str(de))
    print("Energy change percentage : "+str(pe)+"%")

    ha = r0*initial_velocity
    h1 = angular_momenta[0]
    hn = angular_momenta[-1]    
    dh = abs(hn-h1)
    ph = ((hn-h1)/abs(h1))*100
    print("Initial angular momentum difference against analytical : "+str((h1-ha)/abs(ha)*100)+"%")
    print("Initial angular momentum : "+str(h1))
    print("Final angular momentum : "+str(hn))
    print("Angular momentum difference : "+str(dh))
    print("Angular momentum change percentage : "+str(ph)+"%")

    #show_trajectory(result, test_number)
    #show_energy_graph(energies, dt, test_number)
    print("\n")

    return result

# Forward x Semi, Energy
#run_validation(1, vc, 1, 9000)
#run_validation(2, vc, 5, 1800)
#run_validation(3, vc, 10, 900)
#run_validation(4, vc, 30, 300)

# vc Test
#run_validation(1, 0.9*vc, 1, 9000)
#run_validation(2, vc, 1, 9000)
#run_validation(3, 1.1*vc, 1, 9000)

# ve Test
def ve_Test():
    result1 = run_validation(1, 0.99*ve, 1, 9000)
    result2 = run_validation(2, ve, 1, 9000)
    result3 = run_validation(3, 1.01*ve, 1, 9000)

    x1, y1 = zip(*result1)
    x2, y2 = zip(*result2)
    x3, y3 = zip(*result3)

    fig, ax = plt.subplots()
    ax.scatter(x1, y1, s=1, color='blue', label='0.99ve')
    ax.scatter(x2, y2, s=1, color='purple', label='ve')
    ax.scatter(x3, y3, s=1, color='red', label='1.01ve')
    ax.set_aspect('equal')
    ax.set_title("0.99ve, ve, 1.01ve Orbit Comparison")

    plt.show()

ve_Test()