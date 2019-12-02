#Part 1
sum_values = 0
for line in open('data/day_1', 'r'):
    sum_values += (int(line) // 3) - 2
print(sum_values)

#Part 2
sum_values = 0
for line in open('data/day_1', 'r'):
    mass = int(line)
    current = (mass // 3) - 2
    while current > 0:
        sum_values += current
        current = (current // 3) - 2
print(sum_values)