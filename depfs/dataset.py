import numpy
from bunch import Bunch
from matrix import Matrix
from spectrum import Spectrum


class Dataset:
    def __init__(self, matrixes: list[Matrix]) -> None:
        self._matrixes = matrixes

    @property
    def spectra(self) -> list[Spectrum]:
        spectra = []

        for matrix in self._matrixes:
            for spectrum in matrix.slices:
                spectra.append(spectrum)

        return spectra
    
    def pick_train(self, n: int) -> list[Bunch]:
        pass

    def pick_test(self, n: int) -> list[Bunch]:
        pass


if __name__ == '__main__':
    pass