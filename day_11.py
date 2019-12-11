import numpy as np
from matplotlib import pyplot as plt
class GrowingList(list):
    def __init__(self):
        super(list, self).__init__()

    def __getitem__(self, index):
        if index < 0:
            print("SET AT NEGATIVE POSITION")
            return 0
        if index >= len(self):
            return 0
        else:
            return list.__getitem__(self, index)

    def __setitem__(self, index, value):
        if index < 0:
            print("SET AT NEGATIVE POSITION")
            return
        if index >= len(self):
            self.extend([0]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)


def program(op_codes, input_color, pointer = 0, relative_base = 0):

    to_ret = []
    while op_codes[pointer] != 99:
        immediate_left = ((op_codes[pointer] % 1000) //100) == 1
        relative_left = ((op_codes[pointer] % 1000) //100) == 2
        immediate_right = ((op_codes[pointer] % 10000) // 1000) == 1
        relative_right = ((op_codes[pointer] % 10000) // 1000) == 2
        relative_third = ((op_codes[pointer] % 100000) // 10000) == 2
        if op_codes[pointer] > 9999 and op_codes[pointer] < 20000:
            print("Output instead of write")
        op_code = op_codes[pointer] % 100
        if op_code == 1: #add
            lhs = op_codes[pointer+1] if immediate_left else op_codes[op_codes[pointer+1]+ (relative_base if relative_left else 0)]
            rhs = op_codes[pointer+2] if immediate_right else op_codes[op_codes[pointer+2] + (relative_base if relative_right else 0)]
            op_codes[op_codes[pointer+3] + (relative_base if relative_third else 0)] = lhs + rhs
            pointer += 4
        elif op_code == 2: #mult
            lhs = op_codes[pointer + 1] if immediate_left else op_codes[op_codes[pointer + 1]+ (relative_base if relative_left else 0)]
            rhs = op_codes[pointer + 2] if immediate_right else op_codes[op_codes[pointer + 2]+ (relative_base if relative_right else 0)]
            op_codes[op_codes[pointer + 3] + (relative_base if relative_third else 0)] = lhs * rhs
            pointer += 4
        elif op_code == 3: # Input
            if immediate_left:
                print("Input with immediate left")
            if input_color is not None:
                to_put = input_color
                op_codes[op_codes[pointer+1] + (relative_base if relative_left else 0)] = to_put
                pointer += 2
                input_color = None
            else:
                break
        elif op_code == 4: # Output
            if immediate_left:
                to_ret.append(op_codes[pointer+1])
            else:
                to_ret.append(op_codes[op_codes[pointer+1] + (relative_base if relative_left else 0)])
            pointer += 2
        elif op_code == 5: #jump if true
            if immediate_left:
                num = op_codes[pointer+1]
            else:
                num = op_codes[op_codes[pointer+1] + (relative_base if relative_left else 0)]
            if num != 0:
                if immediate_right:
                    pointer = op_codes[pointer+2]
                else:
                    pointer = op_codes[op_codes[pointer+2] + (relative_base if relative_right else 0)]
            else:
                pointer += 3
        elif op_code == 6: # jump if false
            if immediate_left:
                num = op_codes[pointer+1]
            else:
                num = op_codes[op_codes[pointer+1] + (relative_base if relative_left else 0)]
            if num == 0:
                if immediate_right:
                    pointer = op_codes[pointer+2]
                else:
                    pointer = op_codes[op_codes[pointer+2] + (relative_base if relative_right else 0)]
            else:
                pointer += 3
        elif op_code == 7: # less than
            lhs = op_codes[pointer + 1] if immediate_left else op_codes[op_codes[pointer + 1] + (relative_base if relative_left else 0)]
            rhs = op_codes[pointer + 2] if immediate_right else op_codes[op_codes[pointer + 2] + (relative_base if relative_right else 0)]
            to_store = 1 if lhs < rhs else 0
            op_codes[op_codes[pointer+3] + (relative_base if relative_third else 0)] = to_store
            pointer += 4
        elif op_code == 8: # equal
            lhs = op_codes[pointer + 1] if immediate_left else op_codes[op_codes[pointer + 1] + (relative_base if relative_left else 0)]
            rhs = op_codes[pointer + 2] if immediate_right else op_codes[op_codes[pointer + 2]+ (relative_base if relative_right else 0)]
            to_store = 1 if lhs == rhs else 0
            op_codes[op_codes[pointer+3] + (relative_base if relative_third else 0)] = to_store
            pointer += 4
        elif op_code == 9: #relative base adjustment
            lhs = op_codes[pointer + 1] if immediate_left else op_codes[
                op_codes[pointer + 1] + (relative_base if relative_left else 0)]
            relative_base += lhs
            pointer += 2
        else:
            print("Unrecognized opcode : ", op_codes[pointer])
            break
    if op_codes[pointer] == 99:
        pointer = None
    return pointer, relative_base, to_ret


class Robot:
    def __init__(self, opcodes):
        self.opcodes = opcodes
        self.pointer = 0
        self.relative_base = 0
        self.done = False
        self.colors = {}
        self.x = 0
        self.y = 0
        self.directions = {'UP':(0,1), 'DOWN':(0,-1), 'LEFT':(-1,0), 'RIGHT':(1,0)}
        self.direction = 'UP'
        self.dir_change = {'UP':['LEFT', 'RIGHT'], 'LEFT':['DOWN', 'UP'], 'RIGHT':['UP', 'DOWN'], 'DOWN':['RIGHT', 'LEFT']}
        self.c = 0

    def run(self, first=False):
        if self.done:
            print("ERROR, program has finished")
        if (self.x, self.y) in self.colors:
            self.pointer, self.relative_base, instructions = program(self.opcodes, self.colors[(self.x, self.y)], pointer=self.pointer, relative_base=self.relative_base)
        else:
            if first:
                self.pointer, self.relative_base, instructions = program(self.opcodes, 1, pointer=self.pointer, relative_base=self.relative_base)
            else:
                self.pointer, self.relative_base, instructions = program(self.opcodes, 0, pointer=self.pointer, relative_base=self.relative_base)
        if self.pointer is None:
            self.done = True
        if len(instructions) == 0:
            return
        elif len(instructions) == 2:
            self.colors[(self.x, self.y)] = instructions[0]
            self.direction = self.dir_change[self.direction][instructions[1]]
            self.x, self.y = tuple(map(sum, zip((self.x, self.y), self.directions[self.direction])))
        else:
            print("Wrong number of instructions :", len(instructions))

if __name__ == '__main__':
    f = open('data/day_11', 'r')
    op_codes_init = [int(x) for x in f.readlines()[0].strip().split(',')]
    f.close()

    op_codes = GrowingList()
    op_codes[len(op_codes)] = 0
    for i in range(len(op_codes_init)):
        op_codes[i] = op_codes_init[i]
    robot = Robot(op_codes)
    while not robot.done:
        robot.run()
    print("Panels painted :", len(robot.colors.keys()))

    op_codes = GrowingList()
    op_codes[len(op_codes)] = 0
    for i in range(len(op_codes_init)):
        op_codes[i] = op_codes_init[i]
    robot2 = Robot(op_codes)
    robot2.run(first=True)
    while not robot2.done:
        robot2.run()
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    for panel in robot2.colors:
        min_x = min(min_x, panel[0])
        max_x = max(max_x, panel[0])
        min_y = min(min_y, panel[1])
        max_y = max(max_y, panel[1])
    img = np.zeros((max_y-min_y + 1, max_x - min_x+1))
    if (0,0) not in robot2.colors:
        img[-min_y][-min_x] = 1
    robot2.colors[(1,0)] = 1
    for panel in robot2.colors:
        img[panel[1]-min_y][panel[0]-min_x] = robot2.colors[panel]
    img = list(reversed(img))
    plt.imshow(img)
    plt.show()
