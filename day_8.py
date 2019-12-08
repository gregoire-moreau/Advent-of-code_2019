import numpy as np
from matplotlib import pyplot as plt
with open('data/day_8', 'r') as f:
    line = f.readlines()[0].strip()

width = 25
height = 6

layers = [line[i*(width*height):(i+1)*(width*height)] for i in range(len(line)//(width*height))]

layer_index = int(np.argmin([layer.count('0') for layer in layers]))

print(layers[layer_index].count("1")*layers[layer_index].count("2"))

img = np.zeros((6, 25))
for i in range(height):
   for j in range(width):
       k = 0
       while layers[k][width * i + j] == '2':
           k += 1
       img[i][j] = int(layers[k][width * i + j])

plt.imshow(img)
plt.show()
