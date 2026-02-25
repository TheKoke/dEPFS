import os
import pickle
from matrix import Matrix
from dataset import Dataset


class Converter:
    def __init__(self, path: str) -> None:
        self._path = path

    def read(self) -> Dataset:
        pickles = self.gather()

        matrixes = []
        for i in range(len(pickles)):
            with open(pickles[i], "rb") as file:
                current: Matrix = pickle.load(file)
                matrixes.append(current)

        return Dataset(matrixes)

    def gather(self) -> list[str]:
        pickles = []

        stack = os.listdir(self._path)
        stack = [self._path + '\\' + stack[i] for i in range(len(stack))]

        while len(stack) != 0:
            current = stack.pop()

            if os.path.isfile(current) and ".pkl" in current:
                pickles.append(current)

            if os.path.isdir(current):
                inside = os.listdir(current)
                inside = [current + '\\' + inside[i] for i in range(len(inside))]
                stack.extend(inside)

        return pickles


if __name__ == '__main__':
    pass
