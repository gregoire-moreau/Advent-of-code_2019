class FlyingObject:
    def __init__(self, name, orbits= None, orbiter=None):
        self.orbits = orbits
        self.orbiters = [orbiter] if orbiter else []
        if orbits:
            self.depth = orbits.depth+1
        else:
            self.depth = 0
        self.name = name

    def add_orbiter(self, orbiter):
        if orbiter not in self.orbiters:
            self.orbiters.append(orbiter)

    def add_orbits(self, orbits):
        self.orbits = orbits
        self.reset_depth()

    def reset_depth(self):
        self.depth = self.orbits.depth + 1
        for orbiter in self.orbiters:
            orbiter.reset_depth()


flyingObjects = {}
with open('data/day_6', 'r') as f:
    for line in f.readlines():
        l = line.strip().split(')')
        lhs = l[0]
        rhs = l[1]
        if lhs in flyingObjects:
            objLeft = flyingObjects[lhs]
        else:
            objLeft = FlyingObject(lhs)
            flyingObjects[lhs] = objLeft
        if rhs in flyingObjects:
            objRight = flyingObjects[rhs]
            objRight.add_orbits(objLeft)
        else:
            objRight = FlyingObject(rhs, orbits=objLeft)
            flyingObjects[rhs] = objRight
        objLeft.add_orbiter(objRight)


print("Number of direct and indirect orbits", sum([obj.depth for obj in flyingObjects.values()]))

src = flyingObjects["YOU"].orbits
dest = flyingObjects["SAN"].orbits

i = 0
marked = {}
queue = [src]

while len(queue) > 0:
    obj = queue[i]
    if obj is dest:
        break
    if obj.orbits and obj.orbits.name not in marked:
        queue.append(obj.orbits)
        marked[obj.orbits.name] = obj.name
    for orbiter in obj.orbiters:
        if orbiter.name not in marked:
            queue.append(orbiter)
            marked[orbiter.name] = obj.name
    i += 1

count = 0
name = dest.name
while name != src.name:
    name = marked[name]
    count += 1

print("Number of orbit jumps", count)
