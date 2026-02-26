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
        pass

    def run_generation(self, bunch: Bunch) -> list[list[float]]:
        coeffs = self._distr.sample()

    def update(self, generation: list[list[float]]) -> None:
        pass

    def test(self, data: list[Bunch]) -> float:
        pass

    def save(self) -> str:
        pass


if __name__ == '__main__':
    pass