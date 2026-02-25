import numpy
from scipy.signal import find_peaks


class Predictor:
    PARAMS = 3

    def __init__(self, spectrum: numpy.ndarray):
        self._spectrum = spectrum

    @property
    def normalized(self) -> numpy.ndarray:
        return self._spectrum / self._spectrum.max()

    def predict(self, coeffs: list[float]) -> list[float]:
        cn = len(coeffs) // Predictor.PARAMS

        x = numpy.linspace(1 / len(self._spectrum), 1, len(self._spectrum))
        y = self.normalized

        h_coeffs = coeffs[:cn]
        p_coeffs = coeffs[cn:2 * cn]
        w_coeffs = coeffs[2 * cn:]

        h = numpy.zeros_like(x)
        p = numpy.zeros_like(x)
        w = numpy.zeros_like(x)
        for i in range(len(h_coeffs)):
            h += h_coeffs[i] * x ** i
            p += p_coeffs[i] * x ** i
            w += w_coeffs[i] * x ** i

        peaks, _ = find_peaks(y, height=h, prominence=p, width=w)
        return peaks + 1


if __name__ == '__main__':
    pass