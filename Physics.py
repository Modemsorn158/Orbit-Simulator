from math import sqrt

G = 6.6743*(10**-11) # m^3/(kg*s^2)
mu_Earth = 3.986*(10**14) # m^3/s^2
m_Earth = 5.972*(10**24) # kg
r_Earth = 6.371*(10**6) # m

print("μ : "+str(G*m_Earth)+" m^3/s^2")
print("a : "+str(mu_Earth/(r_Earth**2))+" m/s^2")

print("Vc : "+str(sqrt(mu_Earth/r_Earth)))

print("="*20)

def gravitational_acceleration(x, y):
    r = sqrt((x**2)+(y**2))

    ax = -((mu_Earth*x)/(r**3))
    ay = -((mu_Earth*y)/(r**3))

    return(ax, ay)

print(gravitational_acceleration(3, 4))
print(gravitational_acceleration(7000000, 0))

def euler_step(x, y, vx, vy, dt):
    ax, ay = gravitational_acceleration(x, y)

    new_vx = vx+ax*dt
    new_vy = vy+ay*dt

    new_x = x+new_vx*dt
    new_y = y+new_vy*dt

    return(new_x, new_y, new_vx, new_vy)

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

r0 = 7000000
vc = sqrt(mu_Earth/r0)
ve = sqrt((2*mu_Earth)/r0)

print("="*20)