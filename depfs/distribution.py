import numpy
from scipy.special import gamma
from scipy.linalg import inv, norm, sqrtm
from scipy.stats import multivariate_normal


class Distribution:
    def __init__(self, dim: int) -> None:
        self.mean: numpy.ndarray = None
        self._sigma: numpy.ndarray = None
        self._covariance: numpy.ndarray = None
        self._isotropic_path: numpy.ndarray = None
        self._anisotropic_path: numpy.ndarray = None

        self.initialize(dim)
        self._N = multivariate_normal(numpy.zeros(dim), self._covariance)

    def initialize(self, n: int) -> None:
        self.mean = numpy.zeros(n)
        self._sigma = 60. * numpy.ones(n)

        self._covariance = numpy.identity(n)
        self._isotropic_path = numpy.zeros(n)
        self._anisotropic_path = numpy.zeros(n)

    @property
    def n(self) -> int:
        return len(self.mean)

    @property
    def isotropic_decay(self) -> float:
        return 3 / len(self.mean)
    
    @property
    def anisotropic_decay(self) -> float:
        return 4 / len(self.mean)

    def sample(self, lamda: int) -> list[list[float]]:
        return (self.mean + self._sigma * self._N.rvs(size=lamda)).tolist()

    def update(self, generation: list[list[float]]) -> None:
        new_mean = self.updated_mean(generation)
        new_isotropic = self.updated_isotropic_path(new_mean)
        new_sigma = self.updated_sigma(new_isotropic)
        new_anisotropic = self.updated_anisotropic_path(new_mean, new_isotropic)
        new_covariance = self.updated_covariance(generation, new_anisotropic)

        self.mean = new_mean.copy()
        self._sigma = new_sigma.copy()
        self._covariance = new_covariance.copy()
        self._isotropic_path = new_isotropic.copy()
        self._anisotropic_path = new_anisotropic.copy()
        self._N = multivariate_normal(numpy.zeros_like(self.mean), self._covariance)
    
    def updated_mean(self, generation: list[list[float]]) -> numpy.ndarray:
        weights = self.calculate_weights()

        best = generation[:self.n // 2]
        return numpy.average(best, axis=0, weights=weights)
    
    def updated_isotropic_path(self, new_mean: float) -> numpy.ndarray:
        mueff = self.mu_effective()
        csigma = self.isotropic_decay
        old_psigma = self._isotropic_path.copy()

        discount = numpy.sqrt(csigma * (2 - csigma))
        displacement = (new_mean - self.mean) / self._sigma

        new_psigma = (1 - csigma) * old_psigma
        new_psigma += discount * numpy.sqrt(mueff) * sqrtm(inv(self._covariance)) @ displacement

        return new_psigma

    def updated_sigma(self, new_isotropic: numpy.ndarray) -> numpy.ndarray:
        csigma = self.isotropic_decay
        old_sigma = self._sigma.copy()

        expected_norm = numpy.sqrt(2) * gamma((self.n + 1) / 2) / gamma(self.n / 2)
        psigma_norm = norm(new_isotropic)

        return old_sigma * numpy.exp(csigma * (psigma_norm / expected_norm - 1))

    def updated_anisotropic_path(self, new_mean: float, new_isotropic: numpy.ndarray) -> numpy.ndarray:
        mueff = self.mu_effective()
        cc = self.anisotropic_decay

        discount = (1 - cc) * new_isotropic
        displacement = (new_mean - self.mean) / self._sigma

        new_pc = discount + numpy.sqrt(cc * (2 - cc)) * numpy.sqrt(mueff) * displacement

        return new_pc

    def updated_covariance(self, generation: list[list[float]], new_anisotropic: numpy.ndarray) -> numpy.ndarray:
        mueff = self.mu_effective()
        weights = self.calculate_weights()

        c1 = 2 / self.n ** 2
        cmu = mueff / self.n ** 2
        
        discount = (1 - c1 - cmu) * self._covariance
        rank_one = c1 * numpy.outer(new_anisotropic, new_anisotropic)

        rank_mu = numpy.zeros((self.n, self.n))
        for i in range(self.n // 2):
            current = (generation[i] - self.mean) / self._sigma
            rank_mu += weights[i] * numpy.outer(current, current)

        rank_mu *= cmu

        return discount + rank_one + rank_mu

    def mu_effective(self) -> float:
        w = self.calculate_weights()
        return numpy.power(numpy.array(w), 2).sum() ** (-1)

    def calculate_weights(self) -> list[float]:
        return numpy.log(self.n // 2 + 1 / 2) - numpy.log(numpy.arange(1, self.n // 2 + 1))


if __name__ == '__main__':
    pass