import numpy
from bunch import Bunch
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
    
    def split(self, nbunch: int) -> tuple[list[Bunch], list[Bunch]]:
        spectra = self.spectra.copy()
        shuffled = []

        for i in range(len(spectra)):
            index = numpy.random.randint(0, len(spectra))
            shuffled.append(spectra.pop(index))

        bunches = [Bunch(shuffled[i * nbunch: (i + 1) * nbunch]) for i in range(len(shuffled) // nbunch)]
        train = bunches[:4 * len(bunches) // 5]
        test = bunches[4 * len(bunches) // 5:]

        return train, test


if __name__ == '__main__':
    pass