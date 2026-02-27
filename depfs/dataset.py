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


if __name__ == "__main__":
    pass
