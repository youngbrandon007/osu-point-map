import matplotlib.pyplot as plt
from matplotlib import collections
from coordinate import Coordinate as C, distance

nodes = {
  1: C(40.001822, -83.014028),
  2: C(40.001864, -83.013730),
  3: C(40.001743, -83.013701),
  4: C(40.001686, -83.014026),
  5: C(40.001324, -83.013827),
  6: C(40.001175, -83.013924),
  7: C(40.001382, -83.013632),
  8: C(40.001109, -83.013575),
  9: C(40.001040, -83.013669),
  10: C(40.001105, -83.013909),
  11: C(40.001014, -83.013891),
  
}

connections = [
  [1, 2],
  [2, 3],
  [1, 4],
  [4, 5],
  [3, 5],
  [4, 6],
  [5, 6],
  [3, 7],
  [7, 8],
  [8, 9],
  [5, 9],
  [6, 10],
  [10, 11],
  [9, 11]
]


test_lines = []
for a, b in connections:
  test_lines.append([nodes[a], nodes[b]])

fig, ax = plt.subplots()

line_segments = collections.LineCollection(test_lines, array=list(range(len(test_lines))),
                                          colors="black",
                               linewidths=1,
                               linestyles='solid'
                              )

ax.add_collection(line_segments)
ax.set_aspect('equal', adjustable='box')
ax.autoscale()
ax.margins(0.1)


for i in nodes:
  ax.text(nodes[i][0], nodes[i][1], f"{i}", fontsize=8)

plt.show()