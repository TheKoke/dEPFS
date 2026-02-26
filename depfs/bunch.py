import numpy
from models.spectrum import Spectrum


class Bunch:
    def __init__(self, spectra: list[Spectrum]) -> None:
        self._spectra = spectra

    def data_x(self) -> list[numpy.ndarray]:
        numbers = []
        for i in range(len(self._spectra)):
            numbers.append(self._spectra[i].numbers)
        return numbers

    def data_y(self) -> list[list[float]]:
        peaks = []
        for i in range(len(self._spectra)):
            peaks.append(self._spectra[i].peaks)
        return peaks


if __name__ == '__main__':
    pass
