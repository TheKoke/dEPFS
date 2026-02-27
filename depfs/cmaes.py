import numpy
from bunch import Bunch
from fitness import Fitness
from predict import Predictor
from distribution import Distribution


class CMAES:
    def __init__(self, distribution: Distribution) -> None:
        self._distr = distribution
    
    @property
    def lamda(self) -> int:
        return 4 + int(3 * numpy.log(self._distr.n))

    def execute(self, data: list[Bunch]) -> list[float]:
        Gens = 100
        previous = self._distr.mean

        for i in range(Gens):
            print(f"Gen #{i}:")
            for j in range(len(data)):
                generation, chi2s = self.run_generation(data[j])
                print(f"\t Bunch #{j}: avg. chi2 = {numpy.average(chi2s)}")

            if numpy.power(numpy.subtract(generation, previous), 2).sum() <= 1e-2:
                break

            previous = generation.copy()

        return self._distr.mean

    def run_generation(self, bunch: Bunch) -> tuple[list[list[float]], list[float]]:
        generation = self._distr.sample(self.lamda)
        xs = bunch.data_x()
        ys = bunch.data_y()

        chi2s = [0.0] * len(generation)
        for i in range(len(xs)):
            for j in range(len(generation)):
                predicted = Predictor(xs[i]).predict(generation[j])
                chi2s[j] += Fitness().calculate(ys[i], predicted)

        indexes = numpy.argsort(chi2s)
        generation = [generation[i] for i in indexes]
        self._distr.update(generation)
        return (generation, chi2s)

    def test(self, data: list[Bunch]) -> float:
        pass

    def save(self, path: str) -> str:
        with open(path, "w") as txt:
            print(self._distr.mean, file=txt)


if __name__ == '__main__':
    pass