#https://stackoverflow.com/questions/4544630/automatically-growing-lists-in-python
class GrowingList(list):
    def __init__(self):
        super(list, self).__init__()

    def __getitem__(self, index):
        if index >= len(self):
            return 0
        else:
            return list.__getitem__(self, index)

    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([0]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)


def program(op_codes, pointer = 0):
    relative_base = 0
    while op_codes[pointer] != 99:
        immediate_left = ((op_codes[pointer] % 1000) //100) == 1
        relative_left = ((op_codes[pointer] % 1000) //100) == 2
        immediate_right = ((op_codes[pointer] % 10000) // 1000) == 1
        relative_right = ((op_codes[pointer] % 10000) // 1000) == 2
        relative_third = ((op_codes[pointer] % 100000) // 10000) == 2
        if op_codes[pointer] > 9999 and op_codes[pointer] < 20000:
            print("Output instead of write")
        op_code = op_codes[pointer] % 100
        if op_code == 1:
            lhs = op_codes[pointer+1] if immediate_left else op_codes[op_codes[pointer+1]+ (relative_base if relative_left else 0)]
            rhs = op_codes[pointer+2] if immediate_right else op_codes[op_codes[pointer+2] + (relative_base if relative_right else 0)]
            op_codes[op_codes[pointer+3] + (relative_base if relative_third else 0)] = lhs + rhs
            pointer += 4
        elif op_code == 2:
            lhs = op_codes[pointer + 1] if immediate_left else op_codes[op_codes[pointer + 1]+ (relative_base if relative_left else 0)]
            rhs = op_codes[pointer + 2] if immediate_right else op_codes[op_codes[pointer + 2]+ (relative_base if relative_right else 0)]
            op_codes[op_codes[pointer + 3] + (relative_base if relative_third else 0)] = lhs * rhs
            pointer += 4
        elif op_code == 3:
            if immediate_left:
                print("Input with immediate left")
            to_put = int(input("Input needed\n"))
            op_codes[op_codes[pointer+1] + (relative_base if relative_left else 0)] = to_put
            pointer += 2
        elif op_code == 4:
            if immediate_left:
                print(op_codes[pointer+1])
            else:
                print(op_codes[op_codes[pointer+1] + (relative_base if relative_left else 0)])
            pointer += 2
        elif op_code == 5:
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
        elif op_code == 6:
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
        elif op_code == 7:
            lhs = op_codes[pointer + 1] if immediate_left else op_codes[op_codes[pointer + 1] + (relative_base if relative_left else 0)]
            rhs = op_codes[pointer + 2] if immediate_right else op_codes[op_codes[pointer + 2] + (relative_base if relative_right else 0)]
            to_store = 1 if lhs < rhs else 0
            op_codes[op_codes[pointer+3] + (relative_base if relative_third else 0)] = to_store
            pointer += 4
        elif op_code == 8:
            lhs = op_codes[pointer + 1] if immediate_left else op_codes[op_codes[pointer + 1] + (relative_base if relative_left else 0)]
            rhs = op_codes[pointer + 2] if immediate_right else op_codes[op_codes[pointer + 2]+ (relative_base if relative_right else 0)]
            to_store = 1 if lhs == rhs else 0
            op_codes[op_codes[pointer+3] + (relative_base if relative_third else 0)] = to_store
            pointer += 4
        elif op_code == 9:
            lhs = op_codes[pointer + 1] if immediate_left else op_codes[
                op_codes[pointer + 1] + (relative_base if relative_left else 0)]
            relative_base += lhs
            pointer += 2
        else:
            print("Unrecognized opcode : ", op_codes[pointer])
            break
    return


if __name__ == '__main__':
    f = open('data/day_9', 'r')
    op_codes_init = [int(x) for x in f.readlines()[0].strip().split(',')]
    f.close()
    op_codes = GrowingList()
    op_codes[len(op_codes)] = 0
    for i in range(len(op_codes_init)):
        op_codes[i] = op_codes_init[i]
    program(op_codes)
