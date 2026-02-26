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
        pass

    def run(self, bunch: Bunch) -> list[float]:
        gen = 1000

        with open("log.txt", "w") as txt:
            for _ in range(gen):
                print(self._distr.mean, file=txt)
                print("\n", file=txt)
                current_gen = self.run_generation(bunch)
                self._distr.update(current_gen)

        return current_gen[0]

    def run_generation(self, bunch: Bunch) -> list[list[float]]:
        generation = self._distr.sample(self.lamda)
        xs = bunch.data_x()
        ys = bunch.data_y()

        chi2s = [0.0] * len(generation)
        for i in range(len(xs)):
            for j in range(len(generation)):
                predicted = Predictor(xs[i]).predict(generation[j])
                chi2s[j] += Fitness().calculate(ys[i], predicted)

        indexes = numpy.argsort(chi2s)
        return [generation[i] for i in indexes]

    def test(self, data: list[Bunch]) -> float:
        pass

    def save(self) -> str:
        pass


if __name__ == '__main__':
    pass