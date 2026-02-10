import numpy
from spectrum import Spectrum


class Bunch:
    def __init__(self, spectra: list[Spectrum]) -> None:
        self._spectra = spectra

    def pick_train_x(self) -> list[numpy.ndarray]:
        pass
    
    def pick_test_x(self) -> list[list[int]]:
        pass

    def pick_train_y(self) -> list[numpy.ndarray]:
        pass

    def pick_test_y(self) -> list[list[int]]:
        pass


if __name__ == '__main__':
    pass
