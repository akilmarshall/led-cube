from time import sleep, ticks_ms, ticks_diff
# from typing import Iterable, Tuple, Union

from machine import Pin  # type: ignore
import RandomNetwork

INDICES = []
for x in range(3):
    for y in range(3):
        for z in range(3):
            INDICES.append((x, y, z))


class Cube:
    def __init__(self):
        self._slice = [
            {'red': Pin(15, Pin.OUT), 'green': Pin(
                2, Pin.OUT), 'blue': Pin(4, Pin.OUT)},
            {'red': Pin(16, Pin.OUT), 'green': Pin(
                17, Pin.OUT), 'blue': Pin(5, Pin.OUT)},
            {'red': Pin(18, Pin.OUT), 'green': Pin(
                19, Pin.OUT), 'blue': Pin(21, Pin.OUT)},
        ]

        self._point = [
            Pin(13, Pin.OUT),
            Pin(12, Pin.OUT),
            Pin(14, Pin.OUT),
            Pin(27, Pin.OUT),
            Pin(26, Pin.OUT),
            Pin(25, Pin.OUT),
            Pin(33, Pin.OUT),
            Pin(32, Pin.OUT),
            Pin(22, Pin.OUT),
        ]
        # map (x, z) to the point indice
        # (0, 0) (1, 0) (2, 0)          6 7 8
        # (0, 0) (1, 0) (2, 0)    ->    2 4 5
        # (0, 0) (1, 0) (2, 0)          0 1 2
        self._mapping = {
            (0, 0): 0,
            (1, 0): 1,
            (2, 0): 2,
            (0, 1): 3,
            (1, 1): 4,
            (2, 1): 5,
            (0, 2): 6,
            (1, 2): 7,
            (2, 2): 8,
        }
        self._active_points = set()

    def _activate(self, x: int, y: int, z: int, color: str) -> None:
        """This method physically activates the led. """
        assert color in {'red', 'green', 'blue'}
        assert x in range(3)
        assert y in range(3)
        assert z in range(3)
        active_point = (x, y, z, color)
        self._active_points.add(active_point)

        self._slice[y][color].on()
        i = self._mapping[(x, z)]
        self._point[i].on()

    def off(self) -> None:
        if len(self._active_points) == 0:
            return
        for x, y, z, color in self._active_points:
            # x, y, z, color = self._active_point
            self._slice[y][color].off()
            i = self._mapping[(x, z)]
            self._point[i].off()
        self._active_points.clear()

        # # loop over the points and turn them off
        # for pin in self._point:
        #     pin.off()
        # # loop over the _slices and turn off each color
        # for slc in self._slice:
        #     for color in slc:
        #         slc[color].off()

    def on(self, x, y, z, color, delay) -> None:
        self._activate(x, y, z, color)
        sleep(delay)
        self.off()

    # def group_on(self, obj, duration, time_slice=200) -> None:
    #     # obj must be an iterable containing (x: int, y: int, z: int, color: str) tuples
    #     time_slice = 1 / time_slice  # duration of time each led is on
    #     epsilon = time_slice * 5  # time precision
    #     delta = 0  # sum of the time slices experienced thus far

    #     start_time = ticks_ms()
    #     while True:
    #         for x, y, z, color in obj:
    #             self.on(x, y, z, color, time_slice)
    #             cur_time = ticks_ms()
    #             distance = ticks_diff(cur_time, start_time)
    #             print(distance)
    #             if distance > (1000 * duration):
    #                 return
    def group_on(self, group, duration, window=19):
        duration = duration * 1000
        l = len(group)
        time_slice = window / l
        for _ in range(duration / window):
            for x, y, z, c in group:
                self.on(x, y, z, c, time_slice * (1/1000))

    def _group_demo(self, window=25):
        group = [
            (0, 0, 2, 'red'),
            (0, 1, 2, 'red'),
            (0, 2, 2, 'red'),
            (1, 0, 2, 'green'),
            (1, 1, 2, 'green'),
            (1, 2, 2, 'green'),
            (2, 0, 2, 'blue'),
            (2, 1, 2, 'blue'),
            (2, 2, 2, 'blue'),
        ]
        duration = 3 * 1000
        l = len(group)
        time_slice = window / l
        for _ in range(duration / window):
            for x, y, z, c in group:
                self.on(x, y, z, c, time_slice * (1/1000))

    def clear(self) -> None:
        """Synonymous function. """
        self.off()

    def test(self, delay: float = 0.5) -> None:
        """Iterate through the point list and toggle each color. """
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    for c in ['red', 'green', 'blue']:
                        self.on(x, y, z, c, delay)

        # for p in self._point:
        #     for slc in self._slice:
        #         for color in slc:
        #             p.on()
        #             slc[color].on()
        #             sleep(delay)
        #             self.clear()
    def demo(self):
        group1 = [
            (0, 0, 0), (1, 0, 0), (2, 0, 0),
            (0, 1, 0), (1, 1, 0), (2, 1, 0),
            (0, 2, 0), (1, 2, 0), (2, 2, 0),
        ]
        group1 = [(x, y, z, 'red') for x, y, z in group1]
        group2 = []
        group3 = []
        for i in range(3):
            self.group_on(group1, 1)
            group1 = [(x, y, z + 1, c) for (x, y, z, c) in group1]
        self.group_on(group1, 1)
        for i in range(3):
            self.group_on(group1, 1)
            group1 = [(x, y, z - 1, c) for (x, y, z, c) in group1]
        self.group_on(group1, 1)

    def random_network_animation(self, delay=0.1):
        COLORS = ['off', 'red', 'green', 'blue']
        self.network = RandomNetwork.RandomNetwork(27, 4, 3)
        while True:
            group = []
            for i, (x, y, z) in enumerate(INDICES):
                c = self.network.v[i]
                if c != 0:
                    group.append((x, y, z, COLORS[c]))
            self.group_on(group, delay)
            network.update()


cube = Cube()
colors = ['red', 'green', 'blue']
group = []
# for x in range(3):
#     for y in range(3):
#         for z in range(3):
#             group.append((x, y, z, colors[x]))
group1 = [
    (0, 0, 0, 'red'),
    (0, 1, 0, 'red'),
    (0, 2, 0, 'red'),
    (1, 0, 0, 'red'),
    (1, 1, 0, 'red'),
    (1, 2, 0, 'red'),
    (2, 0, 0, 'red'),
    (2, 1, 0, 'red'),
    (2, 2, 0, 'red'),
]

group2 = [
    (0, 0, 0, 'green'),
    (0, 1, 0, 'green'),
    (0, 2, 0, 'green'),
    (0, 0, 1, 'green'),
    (0, 1, 1, 'green'),
    (0, 2, 1, 'green'),
    (0, 0, 2, 'green'),
    (0, 1, 2, 'green'),
    (0, 2, 2, 'green'),
]
group3 = [
    (0, 0, 0, 'blue'),
    (1, 0, 0, 'blue'),
    (2, 0, 0, 'blue'),
    (0, 0, 1, 'blue'),
    (1, 0, 1, 'blue'),
    (2, 0, 1, 'blue'),
    (0, 0, 2, 'blue'),
    (1, 0, 2, 'blue'),
    (2, 0, 2, 'blue'),
]


def f():
    def g(group, i, j, k):
        t = 1
        cube.group_on(group, t)
        for _ in range(2):
            group = [(x + i, y + j, z + k, c) for (x, y, z, c) in group]
            cube.group_on(group, t)
        cube.group_on(group, t)
        for _ in range(2):
            group = [(x - i, y - j, z - k, c) for (x, y, z, c) in group]
            cube.group_on(group, t)

    g(group1, 0, 0, 1)
    # cube.group_on(group1, 1)
    # for i in range(3):
    #     group = [x, y, z + 1, c for x, y, z, c in group1]
    #     cube.group_on(group)

    # cube.group_on(group2, 1)
    # cube.group_on(group3, 1)
    # for i in range(3):
    #     group = [x, y, z, c for x, y, z, c in group1]
