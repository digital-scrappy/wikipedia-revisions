from statistics import mean, median, pstdev
import json
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

with open("test.json", "r") as handle:
    page_lenghts = json.load(handle)

strict_lengths = list(map(lambda x: x[1], page_lenghts))
lenient_lengths = list(map(lambda x: x[2], page_lenghts))
filtered_strict = list(filter(lambda x: x if (x < 10000) else None, strict_lengths))
filtered_lenient = lenient_lengths[:len(filtered_strict)]

print(np.percentile(strict_lengths,40))
print(pstdev(map(lambda x: x[1], page_lenghts)))

plt.scatter(filtered_strict, filtered_lenient)
plt.show()
