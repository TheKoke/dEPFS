import numpy
from bunch import Bunch
from fitness import Fitness
from dataset import Dataset
from predict import Predictor
from distribution import Distribution


class CMAES:
    def __init__(self, nu: int, distribution: Distribution) -> None:
        self._nu = nu
        self._distr = distribution

    def execute(self, dataset: Dataset) -> list[float]:
        pass

    def run(self, bunch: Bunch) -> list[float]:
        pass

    def run_generation(self, bunch: Bunch) -> list[list[float]]:
        pass

    def update(self, generation: list[list[float]]) -> None:
        pass

    def save(self) -> str:
        pass


if __name__ == '__main__':
    pass