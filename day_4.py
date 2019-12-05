import re
range_data = [240920, 789857]
counter_part_1 = 0
counter_part_2 = 0
for i in range(range_data[0], range_data[1]):
    password = str(i)
    if password == ''.join(sorted(password)):
        groups = [''.join(x) for x in re.findall(r'(\d)(\1+)', password)]
        if len(groups) > 0:
            counter_part_1 += 1
            if any(len(x) == 2 for x in groups):
                counter_part_2 += 1
print("Part 1 : ", counter_part_1)
print("Part 2 :", counter_part_2)