from models.matrix import Matrix
from models.spectrum import Spectrum


class Scheduler:
    def __init__(self, matrix: Matrix) -> None:
        self._matrix = matrix
        self.__iter = -1

    @property
    def matrix(self) -> Matrix:
        return self._matrix
    
    def complete(self) -> None:
        if self.__iter + 1 >= len(self.matrix.slices):
            return

        self.__iter += 1
    
    def next(self) -> Spectrum:
        return list(self._matrix.slices.values())[self.__iter + 1]
    
    def prev(self) -> Spectrum:
        if self.__iter < 0: return None
        self.__iter -= 1
        return list(self._matrix.slices.values())[self.__iter + 1]
    
    def completed(self) -> list[int]:
        slices = list(self._matrix.slices.keys())
        return [slices[i] for i in range(self.__iter + 1)]

    def incompleted(self) -> list[int]:
        slices = list(self._matrix.slices.keys())
        return [slices[i] for i in range(self.__iter + 1, len(slices))]
    
    def save(self, directory: str) -> bool:
        self._matrix.save(directory)


if __name__ == '__main__':
    pass
