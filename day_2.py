


def program(op_codes):
    cursor = 0
    while op_codes[cursor] != 99:
        if op_codes[cursor] == 1:
            op_codes[op_codes[cursor+3]] = op_codes[op_codes[cursor+1]] + op_codes[op_codes[cursor+2]]
        elif op_codes[cursor] == 2:
            op_codes[op_codes[cursor + 3]] = op_codes[op_codes[cursor + 1]] * op_codes[op_codes[cursor + 2]]
        else:
            print("Unrecognized opcode : ", op_codes[cursor])
            break
        cursor += 4
    return op_codes[0]


f = open('data/day_2', 'r')
op_codes = [int(x) for x in f.readlines()[0].strip().split(',')]
f.close()


# Part 1
# restoring state
op_codes[1] = 12
op_codes[2] = 2

print(program(op_codes.copy()))

for noun in range(100):
    for verb in range(100):
        op_codes[1] = noun
        op_codes[2] = verb
        res = program(op_codes.copy())
        if res == 19690720:
            print("100 * noun + verb ="  ,100*noun+verb )
            break
