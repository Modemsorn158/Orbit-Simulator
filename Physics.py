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