from math import sqrt, inf, pi, acos, degrees, atan2, sin, cos, radians

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

def orbital_period(x, y, vx, vy):
    a = semi_major_axis(x, y, vx, vy)

    T = 2*pi*sqrt(max(0, (a**3)/mu_Earth))

    return T

def orbital_period_SMA(a):
    T = 2*pi*sqrt(max(0, (a**3)/mu_Earth))

    return T

def eccentricity_vector(x, y, vx, vy):
    h = specific_angular_momentum(x, y, vx, vy)
    r = sqrt((x**2)+(y**2))

    ex = ((vy*h)/mu_Earth)-(x/r)
    ey = -((vx*h)/mu_Earth)-(y/r)

    return ex, ey

def radial_velocity(x, y, vx, vy):
    r = sqrt((x**2)+(y**2))

    vr = ((x*vx)+(y*vy))/r

    return vr

def argument_of_periapsis(x, y, vx, vy):
    ex, ey = eccentricity_vector(x, y, vx, vy)

    omega = degrees(atan2(ey, ex))
    if omega < 0:
        omega += 360

    return omega

def true_anomaly(x, y, vx, vy):
    r = sqrt((x**2)+(y**2))
    e = eccentricity(x, y, vx, vy)
    ex, ey = eccentricity_vector(x, y, vx, vy)
    vr = radial_velocity(x, y, vx, vy)

    # Circular orbit
    if e < (10**-2):
        angle = atan2(y, x)
        if angle < 0:
            angle += 2*pi
        return degrees(angle)

    # Elliptical orbit
    if abs(e) > (10**-6):
        av = ((ex*x)+(ey*y))/(e*r)
        av = max(-1, min(1, av))
        angle = acos(av)
    else:
        angle = 0
    
    if vr < 0:
        angle = (2*pi)-angle

    return degrees(angle)

def mean_motion(a):
    n = sqrt(mu_Earth/(a**3))

    return n

def mean_anomaly(t, n):
    M = n*t

    return M%(2*pi)

def eccentric_anomaly(M, e):
    E = M

    for i in range(8):
        E = E-((E-(e*sin(E))-M)/(1-(e*cos(E))))
    v = atan2((sqrt(1-(e**2))*sin(E)), (cos(E)-e))
    if v < 0:
        v += 2*pi

    return E, v

def mean_anomaly_epoch(v, e):
    E = atan2((sqrt(1-(e**2))*sin(v)), (e+cos(v)))
    if E < 0:
        E += 2*pi

    M0 = E-(e*sin(E))

    return M0%(2*pi)

def propagate_position(a ,e, omega, M0, t):
    omega = radians(omega)
    n = mean_motion(a)
    M = (M0+(n*t))%(2*pi)
    E, v = eccentric_anomaly(M, e)

    r = (a*(1-(e**2)))/(1+(e*cos(v)))
    xo = r*cos(v)
    yo = r*sin(v)
    x = (xo*cos(omega))-(yo*sin(omega))
    y = (xo*sin(omega))+(yo*cos(omega))

    return x, y

def simulate(x, y, vx, vy, dt, steps, record):
    # record = True > retains full history, leave false for initial-final only
    positions = []
    energies = []
    angular_momenta = []
    eccentricities = []
    axises = []
    rps = []
    ras = []
    anomalies = []
    omegas = []

    def record_data():
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
        anomaly = true_anomaly(x, y, vx, vy)
        anomalies.append(anomaly)
        omega = argument_of_periapsis(x, y, vx, vy)
        omegas.append(omega)

    record_data()
    for i in range(steps):
        x, y, vx, vy = euler_step(x, y, vx, vy, dt)
        positions.append((x, y))
        if record == True:
            record_data()
    record_data()

    return positions, energies, angular_momenta, eccentricities, classify_orbit(x, y, vx, vy), axises, rps, ras, orbital_period(x, y, vx, vy), anomalies, omegas

r0 = 7000000
vc = sqrt(mu_Earth/r0)
ve = sqrt((2*mu_Earth)/r0)
T = orbital_period_SMA(7000000)

if __name__ == "__main__":
    print("μ : "+str(G*m_Earth)+" m^3/s^2")
    print("a : "+str(mu_Earth/(r_Earth**2))+" m/s^2")
    print("Vc : "+str(vc))
    print("Ve : "+str(ve))
    print(gravitational_acceleration(3, 4))
    print(gravitational_acceleration(7000000, 0))

    print("="*20)
    
    #print(gravitational_acceleration(3, 4))
    #print(gravitational_acceleration(7000000, 0))

    print("="*20)