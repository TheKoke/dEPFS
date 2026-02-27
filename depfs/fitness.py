import numpy


class Fitness:
    def __init__(self) -> None:
        self.__penalty = 10000

    def calculate(self, true: list[int], predicted: list[int]) -> float:
        sieved = self.sieve(true, predicted)

        chi2 = 0
        for i in range(len(sieved)):
            chi2 += (true[i] - sieved[i]) ** 2

        chi2 = chi2 if len(true) == 0 else chi2 / len(true)
        chi2 = chi2 if len(true) >= len(predicted) else chi2 + self.__penalty * (len(predicted) - len(true))
        chi2 = chi2 if len(true) <= len(predicted) else chi2 + self.__penalty * (len(true) - len(predicted))

        return chi2

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


if __name__ == "__main__":
    pass