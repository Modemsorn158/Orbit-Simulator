from Physics import gravitational_acceleration, euler_step, specific_energy, specific_angular_momentum, classify_orbit, simulate
from Physics import mu_Earth, r_Earth, r0, vc, ve
from math import sqrt
import random as random
import matplotlib.pyplot as plt

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

    result, energies, angular_momenta, eccentricities, orbit_type = simulate(7000000, 0, 0, initial_velocity, dt, steps)    

    se1 = energies[0]
    sen = energies[-1]
    dse = abs(sen-se1)
    pse = ((sen-se1)/abs(se1))*100
    print(("=")*5+" Energy "+("=")*5)
    print("Initital energy : "+str(se1))
    print("Final energy : "+str(sen))
    print("Energy difference : "+str(dse))
    if not abs(se1) < 10**-5:
        print("Energy change percentage : "+str(pse)+"%")

    ha = r0*initial_velocity
    h1 = angular_momenta[0]
    hn = angular_momenta[-1]    
    dh = abs(hn-h1)
    ph = ((hn-h1)/abs(h1))*100
    print(("=")*5+" Angular Momentum "+("=")*5)
    print("Initial angular momentum difference against analytical : "+str((h1-ha)/abs(ha)*100)+"%")
    print("Initial angular momentum : "+str(h1))
    print("Final angular momentum : "+str(hn))
    print("Angular momentum difference : "+str(dh))
    print("Angular momentum change percentage : "+str(ph)+"%")

    e1 = eccentricities[0]
    en = eccentricities[-1]
    de = abs(en-e1)
    if e1 < (10**-20):
        pe = 0
    else:
        pe = ((en-e1)/abs(e1))*100
    print(("=")*5+" Eccentricity "+("=")*5)
    print("Initial eccentricity : "+str(e1))
    print("Final eccentricity : "+str(en))
    print("Eccentricity difference : "+str(de))
    print("Eccentricity change percentage : "+str(pe)+"%")
    print("Orbit type : "+orbit_type)

    #show_trajectory(result, test_number)
    #show_energy_graph(energies, dt, test_number)
    print("\n")

    return result

# ve Test
def ve_Test(scales, dt, steps):
    results = []
    for i, scale in enumerate(scales):
        results.append(run_validation(i+1, scale*ve, dt, steps))

    fig, ax = plt.subplots()
    for i in results:
        x, y = zip(*i)
        ax.scatter(x, y, s=1)
    ax.set_aspect('equal')
    ax.set_title("Orbit Comparison")

    plt.show()

if __name__ == "__main__":
    pass

    #print(euler_step(7000000, 0, 0, 7500, 1))

    # Forward x Semi, Energy
    #run_validation(1, vc, 1, 9000)
    #run_validation(2, vc, 5, 1800)
    #run_validation(3, vc, 10, 900)
    #run_validation(4, vc, 30, 300)

    # vc Test
    run_validation(1, 0.9*vc, 1, 9000)
    run_validation(2, vc, 1, 9000)
    run_validation(3, 1.1*vc, 1, 9000)

    ve_Test([0.99, 1, 1.01], 1, 750000)