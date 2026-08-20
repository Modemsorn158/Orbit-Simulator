from math import sqrt, inf

G = 6.6743*(10**-11) # m^3/(kg*s^2)
mu_Earth = 3.986*(10**14) # m^3/s^2
m_Earth = 5.972*(10**24) # kg
r_Earth = 6.371*(10**6) # m

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

def specific_energy(x, y, vx, vy):
    r = sqrt((x**2)+(y**2))
    v_squared = (vx**2)+(vy**2)
    e = (v_squared/2)-(mu_Earth/r)

    return e

def specific_angular_momentum(x, y, vx, vy):
    h = (x*vy)-(y*vx)
    
    return h

def eccentricity(x, y, vx, vy):
    se = specific_energy(x, y, vx, vy)
    h = specific_angular_momentum(x, y, vx, vy)

    e = sqrt(max(0, 1+((2*se*(h**2)/(mu_Earth**2)))))

    return e

def classify_orbit(x, y, vx, vy):
    e = eccentricity(x, y, vx, vy)
    orbit_type = ""

    if e < 3*(10**-3):
        orbit_type = "Circular"
    elif (e < (1+(10**-3))) and (e > (1-(10**-3))):
        orbit_type = "Parabolic"
    elif e > 1:
        orbit_type = "Hyperbolic"
    else:
        orbit_type = "Elliptical"

    return orbit_type

def semi_major_axis(x, y, vx, vy):
    e = specific_energy(x, y, vx, vy)
    
    if abs(e) < (10**-6):
        a = inf
    else:
        a = -(mu_Earth/(2*e))

    return a

def calculate_ap(x, y, vx, vy):
    e = eccentricity(x, y, vx, vy)
    a = semi_major_axis(x, y, vx, vy)

    rp = a*(1-e)
    ra = a*(1+e)

    return rp, ra

def simulate(x, y, vx, vy, dt, steps):
    positions = []
    energies = []
    angular_momenta = []
    eccentricities = []
    axises = []
    rps = []
    ras = []

    for i in range(steps):
        se = specific_energy(x, y, vx, vy)
        energies.append(se)
        h = specific_angular_momentum(x, y, vx, vy)
        angular_momenta.append(h)
        e = eccentricity(x, y, vx, vy)
        eccentricities.append(e)
        a = semi_major_axis(x, y, vx, vy)
        axises.append(a)
        rp, ra = calculate_ap(x, y, vx, vy)
        rps.append(rp)
        ras.append(ra)
        x, y, vx, vy = euler_step(x, y, vx, vy, dt)
        positions.append((x, y))
    se = specific_energy(x, y, vx, vy)
    energies.append(se)
    h = specific_angular_momentum(x, y, vx, vy)
    angular_momenta.append(h)
    e = eccentricity(x, y, vx, vy)
    eccentricities.append(e)
    a = semi_major_axis(x, y, vx, vy)
    axises.append(a)
    rp, ra = calculate_ap(x, y, vx, vy)
    rps.append(rp)
    ras.append(ra)

    return positions, energies, angular_momenta, eccentricities, classify_orbit(x, y, vx, vy), axises, rps, ras

r0 = 7000000
vc = sqrt(mu_Earth/r0)
ve = sqrt((2*mu_Earth)/r0)

if __name__ == "__main__":
    print("μ : "+str(G*m_Earth)+" m^3/s^2")
    print("a : "+str(mu_Earth/(r_Earth**2))+" m/s^2")
    print("Vc : "+str(sqrt(mu_Earth/r_Earth)))
    print(gravitational_acceleration(3, 4))
    print(gravitational_acceleration(7000000, 0))

    print("="*20)
    
    #print(gravitational_acceleration(3, 4))
    #print(gravitational_acceleration(7000000, 0))

    print("="*20)