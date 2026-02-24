import numpy
from scipy.special import gamma
from scipy.linalg import inv, norm, sqrtm
from scipy.stats import multivariate_normal


class Distribution:
    def __init__(self, dim: int) -> None:
        self._mu = 0
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
        new_sigma = self.updated_sigma(new_isotropic)
    
    def updated_mean(self, generation: list[list[float]]) -> float:
        self._mu = len(generation) // 2
        weights = self.calculate_weights()

        best = generation[:self._mu]
        return numpy.average(best, axis=0, weights=weights)
    
    def updated_isotropic_path(self, new_mean: float) -> numpy.ndarray:
        mueff = self.mu_effective()
        csigma = self.isotropic_decay
        old_psigma = self._isotropic_path.copy()

        discount = numpy.sqrt(csigma(2 - csigma))
        displacement = (new_mean - self._mean) / self._sigma

        new_psigma = (1 - csigma) * old_psigma
        new_psigma += discount * numpy.sqrt(mueff) * sqrtm(inv(self._covariance)) * displacement

        return new_psigma

    def updated_sigma(self, new_isotropic: numpy.ndarray) -> numpy.ndarray:
        n = len(self._mean)
        csigma = self.isotropic_decay
        old_sigma = self._sigma.copy()

        expected_norm = numpy.sqty(2) * gamma((n + 1) / 2) / gamma(n / 2)
        psigma_norm = norm(new_isotropic)

        return old_sigma * numpy.exp(csigma * (psigma_norm / expected_norm - 1))

    def updated_anisotropic_path(self, new_mean: float, new_isotropic: numpy.ndarray) -> numpy.ndarray:
        mueff = self.mu_effective()
        cc = self.anisotropic_decay
        old_pc = self._anisotropic_path.copy()

        discount = (1 - cc) * old_pc
        displacement = (new_mean - self._mean) / self._sigma

        new_pc = discount + numpy.sqrt(cc(2 - cc)) * numpy.sqrt(mueff) * displacement

        return new_pc

    def updated_covariance(self, generation: list[list[float]], new_anisotropic: numpy.ndarray) -> numpy.ndarray:
        n = len(self._mean)
        mueff = self.mu_effective()
        weights = self.calculate_weights()

        c1 = 2 / n ** 2
        cmu = mueff / n ** 2
        
        discount = (1 - c1 - cmu) * self._covariance
        rank_one = c1 * numpy.outer(new_anisotropic, new_anisotropic)

        rank_mu = numpy.zeros((n, n))
        for i in range(len(generation) // 2):
            pass

        rank_mu *= cmu

        return discount + rank_one + rank_mu

    def mu_effective(self) -> float:
        w = self.calculate_weights()
        return numpy.power(numpy.array(w), 2).sum() ** (-1)

    def calculate_weights(self) -> list[float]:
        pass


if __name__ == '__main__':
    pass