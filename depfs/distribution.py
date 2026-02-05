import numpy
from scipy.stats import multivariate_normal


class Distribution:
    def __init__(self):
        self._mean: numpy.ndarray = None
        self._sigma: numpy.ndarray = None
        self._covariance: numpy.ndarray = None
        self._search_path: numpy.ndarray = None
        self._evolution_path: numpy.ndarray = None

    def initialize(self, seed: int) -> None:
        pass

    def sample(self) -> list[float]:
        pass

    def update(self, generation: list[list[float]]) -> None:
        pass


if __name__ == '__main__':
    pass