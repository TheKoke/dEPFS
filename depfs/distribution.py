import numpy
from scipy.stats import multivariate_normal


class Distribution:
    def __init__(self, dim: int) -> None:
        self._mean: numpy.ndarray = None
        self._sigma: numpy.ndarray = None
        self._covariance: numpy.ndarray = None
        self._isotropic_path: numpy.ndarray = None
        self._anisotropic_path: numpy.ndarray = None

        self.initialize(dim)
        self._N = multivariate_normal(self._mean, numpy.power(self._sigma, 2) * self._covariance)

    def initialize(self, n: int) -> None:
        self._mean = 10. * numpy.random.random(n)
        self._sigma = numpy.random.random(n)

        self._covariance = numpy.identity(n)
        self._isotropic_path = numpy.zeros(n)
        self._anisotropic_path = numpy.zeros(n)

    def sample(self) -> list[float]:
        return self._N.rvs().tolist()

    def update(self, generation: list[list[float]]) -> None:
        pass
    
    def update_mean(self) -> None:
        pass

    def update_covariance(self) -> None:
        pass

    def update_isotropic_path(self) -> None:
        pass

    def update_anisotropic_path(self) -> None:
        pass

    def calculate_weights(self) -> list[float]:
        pass


if __name__ == '__main__':
    pass