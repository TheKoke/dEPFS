import os
import numpy
import pickle

from models.slice import Slicer
from models.smoothing import QH353
from models.spectrum import Spectrum
from models.density import DensityMatrix


class Matrix:
    def __init__(self, numbers: numpy.ndarray) -> None:
        self._numbers = numbers

        self._densed: numpy.ndarray = numpy.array([])
        self._slices: dict[int, Spectrum] = {}

    @property
    def numbers(self) -> numpy.ndarray:
        return self._numbers
    
    @property
    def densed(self) -> numpy.ndarray:
        if len(self._densed) <= 0:
            densifier = DensityMatrix(self._numbers)
            self._densed = densifier.densify(zeros=[0])

        return self._densed

    @property
    def slices(self) -> dict[int, Spectrum]:
        if len(self._slices) <= 0:
            sc = Slicer()
            qh353 = QH353()

            distance = int(len(self._numbers) ** (1 / 2))
            slices = sc.shred(self._numbers, step=distance, width=1)

            slices = {ch : qh353.smooth(slices[ch]) for ch in slices}
            self._slices = {ch : Spectrum(slices[ch]) for ch in slices}

        return self._slices
    
    def save(self, directory: str) -> bool:
        if os.path.isdir(directory):
            target = os.path.join(directory, 'pickles')

            if not os.path.exists(target):
                os.mkdir(target)

            name = os.path.join(target, f'{len(os.listdir(target)) + 1}.pkl')
            with open(name, 'wb') as file:
                pickle.dump(self, file)

            return True

        return False


if __name__ == '__main__':
    pass
