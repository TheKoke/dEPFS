import numpy
from models.matrix import Matrix
from models.spectrum import Spectrum


class Dataset:
    def __init__(self, matrixes: list[Matrix]) -> None:
        self._matrixes = matrixes

    @property
    def spectra(self) -> list[Spectrum]:
        spectra = []

        for matrix in self._matrixes:
            for slice in matrix.slices:
                if matrix.slices[slice].numbers.max() > 0:
                    spectra.append(matrix.slices[slice])

        return spectra
    
    def split(self, seed: int) -> tuple[list[Spectrum], list[Spectrum]]:
        spectra = self.spectra.copy()
        numpy.random.seed(seed)
        numpy.random.shuffle(spectra)

        split_idx = int(len(spectra) * 0.8)
        return spectra[:split_idx], spectra[split_idx:]
    
    def train_x(self, seed: int = 42) -> list[numpy.ndarray]:
        pass

    def train_y(self, seed: int = 42) -> list[numpy.ndarray]:
        pass

    def test_x(self, seed: int = 42) -> list[numpy.ndarray]:
        pass

    def test_y(self, seed: int = 42) -> list[numpy.ndarray]:
        pass


if __name__ == '__main__':
    pass