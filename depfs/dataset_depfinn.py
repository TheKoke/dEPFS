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
    
    def train_x(self, seed: int = 42) -> numpy.ndarray:
        train, _ = self.split(seed)
        return self._build_x(train)

    def train_y(self, seed: int = 42, sigma: float = 3.0) -> list[numpy.ndarray]:
        train, _ = self.split(seed)
        return self._build_y(train, sigma)

    def test_x(self, seed: int = 42) -> list[numpy.ndarray]:
        _, test = self.split(seed)
        return self._build_x(test)

    def test_y(self, seed: int = 42, sigma: float = 3.0) -> list[numpy.ndarray]:
        _, test = self.split(seed)
        return self._build_y(test, sigma)
    
    def _build_x(self, spectra: list[Spectrum]) -> numpy.ndarray:
        X = []

        for spectrum in spectra:
            current = spectrum.numbers.astype(numpy.float32)
            current /= current.max()
            X.append(current)

        return numpy.array(X)[..., None]
    
    def _build_y(self, spectra: list[Spectrum], sigma: float) -> numpy.ndarray:
        Y = []

        for spectrum in spectra:
            length = len(spectrum.numbers)
            mask = self._build_mask(length, spectrum.peaks, sigma)
            Y.append(mask)

        return numpy.array(Y)[..., None]
    
    @staticmethod
    def _build_mask(length: int, peaks: list[int], sigma: float) -> numpy.ndarray:
        x = numpy.arange(length)
        mask = numpy.zeros(length)

        for peak in peaks:
            gaussian = numpy.exp(-0.5 * ((x - peak) / sigma) ** 2)
            mask = numpy.maximum(mask, gaussian)

        return mask


if __name__ == '__main__':
    pass