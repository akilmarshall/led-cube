import time
from machine import Pin
from neopixel import NeoPixel
from random import randint, choice
from time import sleep_ms
from umatrix import matrix
from math import cos, sin, pi


n = 27


def demo(np, r, b, g):
    n = np.n
    np.fill((0, 0, 0))
    np.write()
    time.sleep_ms(1000)

    for i in range(n):
        np[i] = (r, b, g)
        np.write()
        time.sleep_ms(100)


def run(t):
    np = NeoPixel(Pin(13), n, timing=t)
    demo(np, 255, 0, 0)
    demo(np, 0, 255, 0)
    demo(np, 0, 0, 255)
    demo(np, 255, 255, 255)
    np.fill((0, 0, 0))
    np.write()


def to_homogeneous(point):
    # takes a 3-tuple and returns a related homogeneous vector
    x, y, z = point
    return matrix([x, y, z, 1], are_rows=False)


def from_homogeneous(vector):
    # takes a homogenous vector and returns a 3-tuple
    x = vector[0][0]
    y = vector[1][0]
    z = vector[2][0]
    return (x, y, z)


class Cube:
    def __init__(self, n=27, pin=13):
        # n leds
        self._n = n
        # control pin on the microcontroller
        self._pin = pin

        self._np = NeoPixel(Pin(self._pin), self._n)

        # (x, y, z) -> i, where i is the linear index
        self._mapping = {
            (0, 0, 0): 0,
            (1, 0, 0): 1,
            (2, 0, 0): 2,
            (2, 0, 1): 3,
            (1, 0, 1): 4,
            (0, 0, 1): 5,
            (0, 0, 2): 6,
            (1, 0, 2): 7,
            (2, 0, 2): 8,
            (0, 1, 0): 9,
            (1, 1, 0): 10,
            (2, 1, 0): 11,
            (2, 1, 1): 12,
            (1, 1, 1): 13,
            (0, 1, 1): 14,
            (0, 1, 2): 15,
            (1, 1, 2): 16,
            (2, 1, 2): 17,
            (0, 2, 0): 18,
            (1, 2, 0): 19,
            (2, 2, 0): 20,
            (2, 2, 1): 21,
            (1, 2, 1): 22,
            (0, 2, 1): 23,
            (0, 2, 2): 24,
            (1, 2, 2): 25,
            (2, 2, 2): 26
        }

        # maintain a color state for each point in the cube
        # this acts as the preimage for transforms of the cube, i.e. rotations, translations, etc
        self._state = dict()
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self._state[(i, j, k)] = (0, 0, 0)

    def update(self):
        # realizes self._state on to the cube
        for point in self._state:
            color = self._state[point]
            self._np[self._mapping[point]] = color

        self._np.write()

    def fill(self, color):
        g, r, b = color
        self._np.fill((g, r, b))
        self._np.write()

    def clear(self):
        # short hand to fill with (0, 0, 0)
        self.fill((0, 0, 0))

    def set(self, pos, col):
        # pos is a 3 tuple
        # col is an grb tuple
        self._state[pos] = col

    def _map_update(self, A):
        # compute a new self._state by matrix multiplying each position by A
        new_state = {}

        for point in self._state:
            color = self._state[point]
            point_new = A * to_homogeneous(point)
            new_state[from_homogeneous(point_new)] = color

        self._state = new_state

    def rotate_z(self):
        # rotate about the central z axis pi/2 counterclockwise
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

        # transformation matrix
        A = Tinv * M * T
        self._map_update(A)

    def rotate_x(self):
        # rotate about the central x axis pi/2 counterclockwise
        theta = pi/2
        T = matrix([1, 0, 0, 0],
                   [0, 1, 0, -1],
                   [0, 0, 1, -1],
                   [0, 0, 0, 1])
        Tinv = matrix([1, 0, 0, 0],
                      [0, 1, 0, 1],
                      [0, 0, 1, 1],
                      [0, 0, 0, 1])
        M = matrix([1, 0, 0, 0],
                   [0, round(cos(theta)), round(-sin(theta)), 0],
                   [0, round(sin(theta)), round(cos(theta)), 0],
                   [0, 0, 0, 1])

        # transformation matrix
        A = Tinv * M * T
        self._map_update(A)

    def rotate_y(self):
        # rotate about the central y axis pi/2 counterclockwise
        theta = pi/2
        T = matrix([1, 0, 0, -1],
                   [0, 1, 0, 0],
                   [0, 0, 1, -1],
                   [0, 0, 0, 1])
        Tinv = matrix([1, 0, 0, 1],
                      [0, 1, 0, 0],
                      [0, 0, 1, 1],
                      [0, 0, 0, 1])
        M = matrix([round(cos(theta)), 0, round(-sin(theta)), 0],
                   [0, 1, 0, 0],
                   [round(sin(theta)), 0, round(cos(theta)), 0],
                   [0, 0, 0, 1])

        # transformation matrix
        A = Tinv * M * T
        self._map_update(A)

    def cross(self):
        self.set((1, 1, 0), (10, 0, 0))
        self.set((1, 1, 2), (10, 0, 0))

        self.set((1, 0, 1), (0, 10, 0))
        self.set((1, 2, 1), (0, 10, 0))

        self.set((0, 1, 1), (0, 0, 10))
        self.set((2, 1, 1), (0, 0, 10))

        self.set((1, 1, 1), (10, 10, 10))

        self.update()

    def random_demo(self):
        colors = [(10, 0, 0), (0, 10, 0), (0, 0, 10),
                  (10, 10, 0), (10, 0, 10), (0, 10, 10)]
        on = []
        while True:
            for _ in range(5):
                point = choice(list(self._mapping.keys()))
                color = choice(colors)
                on.append((point, color))

            for p, c in on:
                self.set(p, c)

            self.write()
            sleep_ms(200)
            self.clear()
            on.clear()

    def random_rotations(self):
        colors = [(10, 0, 0), (0, 10, 0), (0, 0, 10),
                  (10, 10, 0), (10, 0, 10), (0, 10, 10)]

        rotations = [self.rotate_x, self.rotate_y, self.rotate_z]
        # turn on 5 random points
        for _ in range(5):
            point = choice(list(self._mapping.keys()))
            color = choice(colors)
            self.set(point, color)

        self.update()
        sleep_ms(1000)

        while True:
            r = choice(rotations)
            r()
            self.update()
            t = choice(range(3000))
            sleep_ms(t)
