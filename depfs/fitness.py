import numpy


class Fitness:
    def __init__(self) -> None:
        pass

    def calculate(self, true: list[int], predicted: list[int]) -> float:
        pass

    def sieve(self, true: list[int], predicted: list[int]) -> list[int]:
        sieved = []
        copy = predicted.copy()
        for i in range(len(true)):
            if len(copy) <= 0:
                break

            distances = [(true[i] - j)**2 for j in copy]
            nearest = numpy.array(distances).argmin()
            sieved.append(copy.pop(nearest))

        return sieved


if __name__ == '__main__':
    pass