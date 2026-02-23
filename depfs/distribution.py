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

    @property
    def isotropic_decay(self) -> float:
        return 3 / len(self._mean)
    
    @property
    def anisotropic_decay(self) -> float:
        return 4 / len(self._mean)

    def sample(self) -> list[float]:
        return self._N.rvs().tolist()

    def update(self, generation: list[list[float]]) -> None:
        new_mean = self.updated_mean(generation)
        new_isotropic = self.updated_isotropic_path(new_mean)
    
    def updated_mean(self, generation: list[list[float]]) -> float:
        mu = len(generation) // 2
        weights = self.calculate_weights(mu)

        best = generation[:mu]
        return numpy.average(best, axis=0, weights=weights)
    
    def updated_isotropic_path(self, new_mean: float) -> numpy.ndarray:
        pass

    def updated_sigma(self, new_isotropic: numpy.ndarray) -> numpy.ndarray:
        pass

    def updated_anisotropic_path(self, new_mean: float, new_isotropic: numpy.ndarray) -> numpy.ndarray:
        pass

    def updated_covariance(self, new_mean: float, new_anisotropic: numpy.ndarray) -> numpy.ndarray:
        pass

    def calculate_weights(self, mu: int) -> list[float]:
        pass


if __name__ == '__main__':
    pass