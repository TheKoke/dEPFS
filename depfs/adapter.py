import numpy
from bunch import Bunch
from dataset import Dataset
from models.spectrum import Spectrum


class Adapter:
    def __init__(self, dataset: Dataset) -> None:
        self._dataset = dataset

    def to_depfs(self, nbunch: int, seed: int = 42) -> tuple[list[Bunch], list[Bunch]]:
        spectra = self._dataset.spectra.copy()
        numpy.random.seed(seed)
        numpy.random.shuffle(spectra)

        bunches = [Bunch(spectra[i * nbunch: (i + 1) * nbunch]) for i in range(len(spectra) // nbunch)]
        return bunches[:4 * len(bunches) // 5], bunches[4 * len(bunches) // 5:]

    def to_depfinn(self, seed: int = 42, sigma: float = 1.0) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]:
        spectra = self._dataset.spectra.copy()
        numpy.random.seed(seed)
        numpy.random.shuffle(spectra)

        split = int(len(spectra) * 0.8)
        train_x = self._build_x(spectra[:split])
        train_y = self._build_y(spectra[:split], sigma)
        test_x = self._build_x(spectra[split:])
        test_y = self._build_y(spectra[split:], sigma)

        return train_x, train_y, test_x, test_y

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
    

if __name__ == "__main__":
    pass
