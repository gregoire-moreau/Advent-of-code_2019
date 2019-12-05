def program(op_codes):
    pointer = 0
    while op_codes[pointer] != 99:
        immediate_left = ((op_codes[pointer] % 1000) //100) == 1
        immediate_right = ((op_codes[pointer] % 10000) // 1000) == 1
        if op_codes[pointer] > 9999:
            print("Output instead of write")
        op_code= op_codes[pointer] % 100
        if op_code == 1:
            lhs = op_codes[pointer+1] if immediate_left else op_codes[op_codes[pointer+1]]
            rhs = op_codes[pointer+2] if immediate_right else op_codes[op_codes[pointer+2]]
            op_codes[op_codes[pointer+3]] = lhs + rhs
            pointer += 4
        elif op_code == 2:
            lhs = op_codes[pointer + 1] if immediate_left else op_codes[op_codes[pointer + 1]]
            rhs = op_codes[pointer + 2] if immediate_right else op_codes[op_codes[pointer + 2]]
            op_codes[op_codes[pointer + 3]] = lhs * rhs
            pointer += 4
        elif op_code == 3:
            if immediate_left:
                print("Input with immediate left")
            to_put = int(input("Input needed\n"))
            op_codes[op_codes[pointer+1]] = to_put
            pointer += 2
        elif op_code == 4:
            if immediate_left:
                print(op_codes[pointer+1])
            else:
                print(op_codes[op_codes[pointer+1]])
            pointer += 2
        elif op_code == 5:
            if immediate_left:
                num = op_codes[pointer+1]
            else:
                num = op_codes[op_codes[pointer+1]]
            if num != 0:
                if immediate_right:
                    pointer = op_codes[pointer+2]
                else:
                    pointer = op_codes[op_codes[pointer+2]]
            else:
                pointer += 3
        elif op_code == 6:
            if immediate_left:
                num = op_codes[pointer+1]
            else:
                num = op_codes[op_codes[pointer+1]]
            if num == 0:
                if immediate_right:
                    pointer = op_codes[pointer+2]
                else:
                    pointer = op_codes[op_codes[pointer+2]]
            else:
                pointer += 3
        elif op_code == 7:
            lhs = op_codes[pointer + 1] if immediate_left else op_codes[op_codes[pointer + 1]]
            rhs = op_codes[pointer + 2] if immediate_right else op_codes[op_codes[pointer + 2]]
            to_store = 1 if lhs < rhs else 0
            op_codes[op_codes[pointer+3]] = to_store
            pointer += 4
        elif op_code == 8:
            lhs = op_codes[pointer + 1] if immediate_left else op_codes[op_codes[pointer + 1]]
            rhs = op_codes[pointer + 2] if immediate_right else op_codes[op_codes[pointer + 2]]
            to_store = 1 if lhs == rhs else 0
            op_codes[op_codes[pointer+3]] = to_store
            pointer += 4
        else:
            print("Unrecognized opcode : ", op_codes[pointer])
            break
    print("done")

f = open('data/day_5', 'r')
op_codes = [int(x) for x in f.readlines()[0].strip().split(',')]
f.close()
#op_codes = [int(x) for x in "3,0,4,0,99".strip().split(',')]

program(op_codes)