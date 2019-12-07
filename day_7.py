def program(op_codes, input_n, pointer = 0):
    to_ret = None
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
            if input_n is not None:
                op_codes[op_codes[pointer+1]] = input_n
                input_n = None
                pointer += 2
            else:
                return to_ret, pointer
        elif op_code == 4:
            if immediate_left:
                to_ret = op_codes[pointer+1]
            else:
                to_ret = op_codes[op_codes[pointer+1]]
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
    return [to_ret]

class Amplifier:
    def __init__(self, opcodes):
        self.opcodes = opcodes
        self.pointer = 0
        self.done = False

    def run(self, input_n):
        if self.done:
            print("ERROR, program has finished")
        out = program(self.opcodes, input_n, pointer=self.pointer)
        if len(out) == 1:
            self.done = True
            return out[0]
        else:
            self.pointer = out[1]
            return out[0]

f = open('data/day_7', 'r')
op_codes = [int(x) for x in f.readlines()[0].strip().split(',')]
f.close()


phase_sequences = []
for a in range(5):
    for b in range(5):
        if b == a:
            continue
        for c in range(5):
            if c == b or c == a:
                continue
            for d in range(5):
                if d == c or d == b or d == a:
                    continue
                for e in range(5):
                    if e == d or e == c or e == b or e == a:
                        continue
                    phase_sequences.append((a,b,c,d,e))

max_thrust = 0
for phase_seq in phase_sequences:
    A = Amplifier(op_codes.copy())
    A.run(phase_seq[0])
    B = Amplifier(op_codes.copy())
    B.run(phase_seq[1])
    C = Amplifier(op_codes.copy())
    C.run(phase_seq[2])
    D = Amplifier(op_codes.copy())
    D.run(phase_seq[3])
    E = Amplifier(op_codes.copy())
    E.run(phase_seq[4])
    out = A.run(0)
    out = B.run(out)
    out = C.run(out)
    out = D.run(out)
    out = E.run(out)
    max_thrust = out if out > max_thrust else max_thrust

print("Maximum output signal :", max_thrust)


phase_sequences = []
for a in range(5,10):
    for b in range(5,10):
        if b == a:
            continue
        for c in range(5, 10):
            if c == b or c == a:
                continue
            for d in range(5, 10):
                if d == c or d == b or d == a:
                    continue
                for e in range(5,10):
                    if e == d or e == c or e == b or e == a:
                        continue
                    phase_sequences.append((a,b,c,d,e))

max_thrust = 0
for phase_seq in phase_sequences:
    A = Amplifier(op_codes.copy())
    A.run(phase_seq[0])
    B = Amplifier(op_codes.copy())
    B.run(phase_seq[1])
    C = Amplifier(op_codes.copy())
    C.run(phase_seq[2])
    D = Amplifier(op_codes.copy())
    D.run(phase_seq[3])
    E = Amplifier(op_codes.copy())
    E.run(phase_seq[4])
    out = 0
    while not E.done:
        out = A.run(out)
        out = B.run(out)
        out = C.run(out)
        out = D.run(out)
        out = E.run(out)
    max_thrust = out if out > max_thrust else max_thrust

print("Maximum output signal with feedback loop :", max_thrust)

