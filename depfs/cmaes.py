import numpy
from fitness import Fitness
from distribution import Distribution


class CMAES:
    def __init__(self, nu: int, distribution: Distribution) -> None:
        self._nu = nu
        self._distr = distribution

    def run_generation(self) -> list[list[float]]:
        pass

    def update(self, generation: list[list[float]]) -> None:
        pass

    def execute(self) -> list[float]:
        pass

    def save(self) -> str:
        pass


if __name__ == '__main__':
    pass