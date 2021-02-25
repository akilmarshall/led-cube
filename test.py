from math import pi, cos, sin
from umatrix import matrix


theta = pi/2
T = matrix([1, 0, 0, -1],
           [0, 1, 0, -1],
           [0, 0, 1, 0],
           [0, 0, 0, 1])
Tinv = matrix([1, 0, 0, 1],
              [0, 1, 0, 1],
              [0, 0, 1, 0],
              [0, 0, 0, 1])
M = matrix([round(cos(theta)), round(-sin(theta)), 0, 0],
           [round(sin(theta)), round(cos(theta)), 0, 0],
           [0, 0, 1, 0],
           [0, 0, 0, 1])

# vector
point = matrix([0, 0, 0, 1], are_rows=False)
