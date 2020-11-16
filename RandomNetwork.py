from collections import defaultdict
from random import randint

from colorama import Fore

COLORS = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.MAGENTA,
          Fore.YELLOW, Fore.CYAN, Fore.WHITE, Fore.BLACK]


class RandomNetwork:
    def __init__(self, m: int, n: int, l: int):
        self._m = m
        self._n = n
        self._l = l

        self.setup()

    def setup(self):
        # generate the graph
        self.G = defaultdict(list)
        for i in range(self._m):
            for _ in range(self._l):
                self.G[i].append(randint(0, self._m - 1))

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

    def print(self):
        assert self._n <= len(COLORS)
        print(f'┌{"─"*self._m}┐')
        for s in self.history:
            print('│', end='')
            # print("".join(map(lambda x: '█' if x == 1 else ' ', s)), end='')
            print("".join(map(lambda x: f'{COLORS[x]}█', s)), end=Fore.RESET)
            print('│')
        print(f'└{"─"*self._m}┘')

    def save_to_file(self, fname: str = None):
        if fname is None:
            fname = f'RandomNetwork_m={self._m}_n={self._n}_l={self._l}.hist'
            with open(fname, 'w') as f:
                for s in self.history:
                    f.write(
                        "".join(map(lambda x: f'{COLORS[x]}█', s)))
                    f.write(f'{Fore.RESET}\n')
