def program(op_codes):
    pointer = 0
    while op_codes[pointer] != 99:
        if op_codes[pointer] == 1:
            op_codes[op_codes[pointer+3]] = op_codes[op_codes[pointer+1]] + op_codes[op_codes[pointer+2]]
        elif op_codes[pointer] == 2:
            op_codes[op_codes[pointer + 3]] = op_codes[op_codes[pointer + 1]] * op_codes[op_codes[pointer + 2]]
        else:
            print("Unrecognized opcode : ", op_codes[pointer])
            break
        pointer += 4
    return op_codes[0]


f = open('data/day_2', 'r')
op_codes = [int(x) for x in f.readlines()[0].strip().split(',')]
f.close()


# Part 1
# restoring state
op_codes[1] = 12
op_codes[2] = 2

print(program(op_codes.copy()))

# Part 2
for noun in range(100):
    for verb in range(100):
        op_codes[1] = noun
        op_codes[2] = verb
        res = program(op_codes.copy())
        if res == 19690720:
            print("100 * noun + verb ="  ,100*noun+verb )
            break
