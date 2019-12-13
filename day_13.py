import matplotlib.pyplot as plt
import matplotlib
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

def program(op_codes, input_color=None, pointer = 0, relative_base = 0):
    to_ret = []
    while op_codes[pointer] != 99 and len(to_ret) < 3:
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
    def __init__(self, opcodes, display=False):
        self.opcodes = opcodes
        self.pointer = 0
        self.relative_base = 0
        self.done = False
        self.tiles = {}
        self.score = 0
        self.ball_x = -1
        self.paddle_x = -1
        self.display = display
        if display:
            self.img = [[0 for _ in range(42)] for _ in range(24)]
            self.im = plt.imshow(self.img)
            matplotlib.use("TkAgg")
            plt.ion()
            self.draw_step = 10

    def run(self, play=False):
        if self.done:
            print("ERROR, program has finished")
        if play:
            action = -1 if self.paddle_x > self.ball_x else (1 if self.paddle_x < self.ball_x else 0)
            self.pointer, self.relative_base, instructions = program(self.opcodes, input_color=action, pointer=self.pointer, relative_base=self.relative_base)
        else:
            self.pointer, self.relative_base, instructions = program(self.opcodes, input_color=None, pointer=self.pointer, relative_base=self.relative_base)
        self.done = self.pointer is None
        if len(instructions) == 3:
            x, y, type = instructions
            if (x, y) == (-1, 0):
                self.score = type
            else:
                self.tiles[(x, y)] = type
                if type == 4:
                    self.ball_x = x
                elif type == 3:
                    self.paddle_x = x
                if self.display:
                    self.img[y][x] = type
                    if self.draw_step == 0:
                        plt.imshow(self.img)
                        plt.pause(0.001)
                        print(self.score)
                        self.draw_step = 10
                    else:
                        self.draw_step -= 1
        elif len(instructions) != 3 and len(instructions) != 0:
            print("Wrong number of instructions :", len(instructions))

if __name__ == '__main__':
    f = open('data/day_13', 'r')
    op_codes_init = [int(x) for x in f.readlines()[0].strip().split(',')]
    f.close()

    op_codes = GrowingList()
    op_codes[len(op_codes)] = 0
    for i in range(len(op_codes_init)):
        op_codes[i] = op_codes_init[i]
    robot = Robot(op_codes)
    while not robot.done:
        robot.run()

    print("Number of blocks:", sum(robot.tiles[key] == 2 for key in robot.tiles))

    op_codes = GrowingList()
    op_codes[len(op_codes)] = 0
    for i in range(len(op_codes_init)):
        op_codes[i] = op_codes_init[i]
    op_codes[0] = 2
    robot = Robot(op_codes, display=False)
    while not robot.done and sum(robot.tiles[key] == 2 for key in robot.tiles) == 0:
        robot.run(play=True)
    while not robot.done:
        robot.run(play=True)

    print("Final score :", robot.score, "Blocks remaining :", sum(robot.tiles[key] == 2 for key in robot.tiles))
