"""This is a Random n-ary Network implementation for micropython. """
from random import randint


class RandomNetwork:
    def __init__(self, m: int, n: int, l: int):
        self._m = m
        self._n = n
        self._l = l

        self.setup()

    def setup(self):
        # generate the graph
        self.G = dict()
        for i in range(self._m):
            for _ in range(self._l):
                if i not in self.G:
                    self.G[i] = list()
                self.G[i].append(randint(0, self._m - 1))

        # generate node list
        self.nodes = []
        # generate random functions f
        self.f = dict()
        for i in range(self._m):
            mapping = [(x, randint(0, self._n - 1))
                       for x in range(self._n**self._l)]
            self.f[i] = dict(mapping)

        # generate initial values
        self.v = [randint(0, self._n - 1) for _ in range(self._m)]

        self.history = [self.v]

    def update(self):
        next_v = []
        for node in range(self._m):
            value = [self.v[x] for x in self.G[node]]
            value = map(str, value)
            value = "".join(value)
            value = int(value, base=self._n)
            next_v.append(self.f[node][value])
        self.v = next_v
        self.history.append(self.v)

    def step(self, n):
        for _ in range(n):
            self.update()
