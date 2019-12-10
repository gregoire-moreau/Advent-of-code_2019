import numpy as np
from math import atan, pi
def obstructions(p1, p2):
    if p1[0] == p2[0] and p1[1] == p2[1]:
        return set([p1])
    to_ret = []
    if p1[0] != p2[0]:
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b = p1[1] - (m * p1[0])
        step = 1 if p1[0] < p2[0] else -1
        for x in range(p1[0] + step, p2[0], step):
            y = m * x + b
            if abs(y - round(y)) < 0.000000000001:
                to_ret.append((x, round(y)))
    else:
        step = 1 if p1[1] < p2[1] else -1
        for y in range(p1[1] + step, p2[1], step):
            to_ret.append((p1[0], y))
    return set(to_ret)


asteroids = []

with open('data/day_10', 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    for j in range(len(lines[i])):
        if lines[i][j] == '#':
            asteroids.append((j , i))

detectable_asteroids = []
detectable_asteroids_lists = []
for asteroid in asteroids:
    counter = 0
    detectable = []
    for other_asteroid in asteroids:
        if asteroid == other_asteroid:
            continue
        else:
            obs = obstructions(asteroid, other_asteroid)
            if not obs.intersection(set(asteroids)):
                counter += 1
                detectable.append(other_asteroid)
    detectable_asteroids.append(counter)
    detectable_asteroids_lists.append(detectable)

print("Coordinates", asteroids[np.argmax(detectable_asteroids)], "max ", max(detectable_asteroids))

ind = np.argmax(detectable_asteroids)
coords = asteroids[ind]
detectable_asteroids = detectable_asteroids_lists[ind]

def sort_angle(point):
    dy = point[1] - coords[1]
    dx = point[0] - coords[0]
    if dx == 0:
        return 0 if point[1] <= coords[1] else 180
    theta = atan(dy / dx)
    theta *= 180 / pi
    theta += 90
    return theta if dx > 0 else theta + 180

detectable_asteroids.sort(key=lambda x:sort_angle(x))
asteroid_200 = detectable_asteroids[199]
print("200th asteroid at coordinates :",asteroid_200[0]*100+asteroid_200[1])