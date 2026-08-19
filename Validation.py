from math import sqrt
import matplotlib.pyplot as plt

mu_Earth = 3.986*(10**14) # m^3/s^2

def gravitational_acceleration(x, y):
    r = sqrt((x**2)+(y**2))

    ax = -((mu_Earth*x)/(r**3))
    ay = -((mu_Earth*y)/(r**3))

    return(ax, ay)

def euler_step(x, y, vx, vy, dt):
    ax, ay = gravitational_acceleration(x, y)

    new_vx = vx+ax*dt
    new_vy = vy+ay*dt

    new_x = x+new_vx*dt
    new_y = y+new_vy*dt

    return(new_x, new_y, new_vx, new_vy)

print(euler_step(7000000, 0, 0, 7500, 1))

def specific_energy(x, y, vx, vy):
    r = sqrt((x**2)+(y**2))
    v_squared = (vx**2)+(vy**2)
    e = (v_squared/2)-(mu_Earth/r)

    return e

def specific_angular_momentum(x, y, vx, vy):
    h = (x*vy)-(y*vx)
    
    return h

def simulate(x, y, vx, vy, dt, steps):
    positions = []
    energies = []
    angular_momenta = []

    for i in range(steps):
        e = specific_energy(x, y, vx, vy)
        energies.append(e)
        h = specific_angular_momentum(x, y, vx, vy)
        angular_momenta.append(h)
        x, y, vx, vy = euler_step(x, y, vx, vy, dt)
        positions.append((x, y))
    e = specific_energy(x, y, vx, vy)
    energies.append(e)
    h = specific_angular_momentum(x, y, vx, vy)
    angular_momenta.append(h)

    return positions, energies, angular_momenta

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

r0 = 7000000
vc = sqrt(mu_Earth/r0)

def run_validation(test_number, dt, steps):
    print("TEST UNIT "+str(test_number)+" : dt="+str(dt)+" steps="+str(steps))

    result, energies, angular_momenta = simulate(7000000, 0, 0, vc, dt, steps)    

    e1 = energies[0]
    en = energies[-1]
    de = abs(en-e1)
    pe = ((en-e1)/abs(e1))*100
    print("Initital energy : "+str(e1))
    print("Final energy : "+str(en))
    print("Energy difference : "+str(de))
    print("Energy change percentage : "+str(pe)+"%")

    ha = r0*vc
    h1 = angular_momenta[0]
    hn = angular_momenta[-1]    
    dh = abs(hn-h1)
    ph = ((hn-h1)/abs(h1))*100
    print("Initial angular momentum difference against analytical : "+str((h1-ha)/abs(ha)*100)+"%")
    print("Initial angular momentum : "+str(h1))
    print("Final angular momentum : "+str(hn))
    print("Angular momentum difference : "+str(dh))
    print("Angular momentum change percentage : "+str(ph)+"%")

    show_trajectory(result, test_number)
    show_energy_graph(energies, dt, test_number)
    print("\n")

run_validation(1, 1, 9000)
run_validation(2, 5, 1800)
run_validation(3, 10, 900)
run_validation(4, 30, 300)