import re
import matplotlib.pyplot as plt

class Moon:
    def __init__(self, coords):
        match = re.match(r'^<x=(-?\d+), y=(-?\d+), z=(-?\d+)>$', coords)
        self.x = int(coords[match.regs[1][0]:match.regs[1][1]])
        self.y = int(coords[match.regs[2][0]:match.regs[2][1]])
        self.z = int(coords[match.regs[3][0]:match.regs[3][1]])
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def apply_gravity(self, other):
        if self.x != other.x:
            self.vx += 1 if self.x < other.x else -1
        if self.y != other.y:
            self.vy += 1 if self.y < other.y else -1
        if self.z != other.z:
            self.vz += 1 if self.z < other.z else -1

    def apply_velocity(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def energy(self):
        return (abs(self.x)+abs(self.y)+abs(self.z)) * (abs(self.vx)+abs(self.vy)+abs(self.vz))

with open('data/day_12', 'r') as f:
    lines = f.readlines()

io = Moon(lines[0].strip())
europa = Moon(lines[1].strip())
ganymede = Moon(lines[2].strip())
callisto = Moon(lines[3].strip())
moons = [io, europa, ganymede, callisto]
pairs = [(m1, m2) for m1 in moons for m2 in moons if m1 is not m2]

for i in range(1000):
    for m1, other in pairs:
        m1.apply_gravity(other)
    io.apply_velocity()
    europa.apply_velocity()
    ganymede.apply_velocity()
    callisto.apply_velocity()


print("Total energy =", io.energy()+europa.energy()+ganymede.energy()+callisto.energy())

io = Moon(lines[0].strip())
europa = Moon(lines[1].strip())
ganymede = Moon(lines[2].strip())
callisto = Moon(lines[3].strip())

orig_x = (io.x, europa.x, ganymede.x, callisto.x)
x = orig_x
vx = (0,0,0,0)
i = 0
while True:
    vx = tuple(map(sum, zip(vx, [sum(x_o > x_m for x_o in x) - sum(x_o < x_m for x_o in x) for x_m in x])))
    x = tuple(map(sum, zip(x, vx)))
    i += 1
    if x == orig_x and vx == (0, 0, 0, 0):
        cycle_x = i
        break

orig_y = (io.y, europa.y, ganymede.y, callisto.y)
y = orig_y
vy = (0,0,0,0)
i = 0
while True:
    vy = tuple(map(sum, zip(vy, [sum(y_o > y_m for y_o in y) - sum(y_o < y_m for y_o in y) for y_m in y])))
    y = tuple(map(sum, zip(y, vy)))
    i += 1
    if y == orig_y and vy == (0, 0, 0, 0):
        cycle_y = i
        break

orig_z = (io.z, europa.z, ganymede.z, callisto.z)
z = orig_z
vz = (0,0,0,0)
i = 0
while True:
    vz = tuple(map(sum, zip(vz, [sum(z_o > z_m for z_o in z) - sum(z_o < z_m for z_o in z) for z_m in z])))
    z = tuple(map(sum, zip(z, vz)))
    i += 1
    if z == orig_z and vz == (0, 0, 0, 0):
        cycle_z = i
        break

#https://www.programiz.com/python-programming/examples/lcm
def compute_lcm(x, y, z):
    x_powers = {}
    y_powers = {}
    z_powers = {}
    primes = []
    curr_prime = 2
    while x != 1 or y != 1 or z != 1:
        i = 0
        while x % curr_prime == 0:
            x /= curr_prime
            i += 1
        x_powers[curr_prime] = i
        i = 0
        while y % curr_prime == 0:
            y /= curr_prime
            i += 1
        y_powers[curr_prime] = i
        i = 0
        while z % curr_prime == 0:
            z /= curr_prime
            i += 1
        z_powers[curr_prime] = i
        primes.append(curr_prime)
        found = False
        while not found:
            curr_prime += 1
            found = True
            for prime in primes:
                if curr_prime % prime == 0:
                    found = False
                    break
    to_ret = 1
    for prime in primes:
        to_ret *= prime ** max([x_powers[prime], y_powers[prime], z_powers[prime]])
    return to_ret

print("Complete cycle :", compute_lcm(cycle_x, cycle_y, cycle_z))