f = open('data/day_3')
lines = f.readlines()
f.close()

wires = [line.strip().split(',') for line in lines]


wires_lines = []
for wire in range(len(wires)):
    pointer_x = 0
    pointer_y = 0
    lines = []
    counter = 0
    for move in wires[wire]:
        dist = int(move[1:])
        if move[0] == 'U':
            lines.append(('U',(pointer_x, pointer_y+1), (pointer_x, pointer_y+dist), counter))
            pointer_y += dist
        elif move[0] == 'D':
            lines.append(('D',(pointer_x, pointer_y - 1), (pointer_x, pointer_y - dist), counter))
            pointer_y -= dist
        elif move[0] == 'R':
            lines.append(('R',(pointer_x+1, pointer_y), (pointer_x +dist, pointer_y), counter))
            pointer_x += dist
        elif move[0] == 'L':
            lines.append(('L',(pointer_x - 1, pointer_y), (pointer_x - dist, pointer_y), counter))
            pointer_x -= dist
        else:
            print("Error : unrecognized character : ", move[0])
        counter += dist
    wires_lines.append(lines)

def dist_from_root(point):
    x, y = point
    return abs(x)+abs(y)

def concurrent(a1, a2, b1, b2):
    if a1 > b2 or a2 < b1:
        return 1000000000
    else:
        inter = []
        if a1 >= b1 and a1 <= b2:
            inter.append(a1)
        if a2 >= b1 and a2 <= b2:
            inter.append(a2)
        if b1 >= a1 and b1 <= a2:
            inter.append(b1)
        if b2 >= a1 and b2 <= a2:
            inter.append(b1)
    return min([abs(x) for x in inter])


min_dist = 10000000000
for (d1, (x1,y1), (x2,y2), _) in wires_lines[0]:
    for (d2, (x3, y3), (x4, y4),_) in wires_lines[1]:
        if d1 == 'U' or d1 == 'D':
            if d2 == 'U' or d2 == 'D':
                if x1 == x3:
                    dist = dist_from_root((x1, concurrent(min(y1, y2), max(y1,y2), min(y3, y4), max(y3, y4))))
                    if dist < min_dist:
                        min_dist = dist
                else:
                    continue
            else:
                if x1 >= min(x3, x4) and x1 <= max(x3, x4) and y3 >= min(y1,y2) and y3 <= max(y1, y2):
                    dist = dist_from_root((x1, y3))
                    if dist < min_dist:
                        min_dist = dist
                else:
                    continue
        else:
            if d2 == 'L' or d2 == 'R':
                if y1 == y3:
                    dist = dist_from_root((concurrent(min(x1, x2), max(x1, x2), min(x3, x4), max(x3, x4)), y1))
                    if dist < min_dist:
                        min_dist = dist
                else:
                    continue
            else:
                if x3 >= min(x1, x2) and x3 <= max(x1, x2) and y1 >= min(y3, y4) and y1 <= max(y3,y4) :
                    dist = dist_from_root((x3, y1))
                    if dist < min_dist:
                        min_dist = dist
                else:
                    continue

print("The closest intersection using Manhattan distance is :", min_dist)

def concurrent_all(a1, a2, b1, b2):
    if a1 > b2 or a2 < b1:
        return []
    else:
        inter = []
        if a1 >= b1 and a1 <= b2:
            inter.append(a1)
        if a2 >= b1 and a2 <= b2:
            inter.append(a2)
        if b1 >= a1 and b1 <= a2:
            inter.append(b1)
        if b2 >= a1 and b2 <= a2:
            inter.append(b1)
    return inter

def count_steps(c, x1, y1, xc, yc, d):
    if d == 'U':
        return c + yc - y1 + 1
    elif d == 'D':
        return c + y1 - yc + 1
    elif d == 'R':
        return c + xc - x1 + 1
    elif d == 'L':
        return c + x1 - xc + 1

min_steps = 100000000000
for (d1, (x1,y1), (x2,y2), c1) in wires_lines[0]:
    if c1 >= min_steps:
        break
    for (d2, (x3, y3), (x4, y4),c2) in wires_lines[1]:
        if c1 + c2 >= min_steps:
            break
        if d1 == 'U' or d1 == 'D':
            if d2 == 'U' or d2 == 'D':
                if x1 == x3:
                    intersections = concurrent_all(min(y1, y2), max(y1,y2), min(y3, y4), max(y3, y4))
                    for inter in intersections:
                        steps = count_steps(c1, x1, y1, x1, inter, d1) + count_steps(c2, x3, y3, x1, inter, d2)
                        if steps < min_steps:
                            min_steps = steps
                else:
                    continue
            else:
                if x1 >= min(x3, x4) and x1 <= max(x3, x4) and y3 >= min(y1,y2) and y3 <= max(y1, y2):
                    steps = count_steps(c1, x1, y1, x1, y3, d1) + count_steps(c2, x3, y3, x1, y3, d2)
                    if steps < min_steps:
                        min_steps = steps
                else:
                    continue
        else:
            if d2 == 'L' or d2 == 'R':
                if y1 == y3:
                    intersections = concurrent_all(min(x1, x2), max(x1, x2), min(x3, x4), max(x3, x4))
                    for inter in intersections:
                        steps = count_steps(c1, x1, y1, inter, y1, d1) + count_steps(c2, x3, y3, inter, y1, d2)
                        if steps < min_steps:
                            min_steps = steps
                else:
                    continue
            else:
                if x3 >= min(x1, x2) and x3 <= max(x1, x2) and y1 >= min(y3, y4) and y1 <= max(y3,y4) :
                    dist = dist_from_root((x3, y1))
                    steps = count_steps(c1, x1, y1, x3, y1, d1) + count_steps(c2, x3, y3, x3, y1, d2)
                    if steps < min_steps:
                        min_steps = steps
                else:
                    continue

print("The closest intersection in sum of steps is :", min_steps)