import numpy
from bunch import Bunch
from matrix import Matrix
from spectrum import Spectrum


class Dataset:
    def __init__(self, matrixes: list[Matrix]) -> None:
        self._matrixes = matrixes

    @property
    def spectra(self) -> list[Spectrum]:
        pass
    
    def pick_train(self) -> list[Bunch]:
        pass

    def pick_test(self) -> list[Bunch]:
        pass


if __name__ == '__main__':
    pass