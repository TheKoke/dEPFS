import numpy


class DensityMatrix:
    def __init__(self, matrix: numpy.ndarray) -> None:
        self._matrix = matrix

    def densify(self, times: int = 1, zeros: list[int] = [9]) -> numpy.ndarray:
        if times != len(zeros):
            zeros = [9] * times

        densed = self._calc(self._matrix, zeros[0])
        for i in range(1, times - 1):
            densed = self._calc(densed, zeros[i])

        return densed

    def _calc(self, matrix: numpy.ndarray, zeros: int = 9) -> numpy.ndarray:
        copy = numpy.zeros_like(matrix)

        for i in range(len(copy)):
            for j in range(len(copy)):
                copy[i, j] = self._point_density(matrix, i, j, zeros)

        return copy
    
    def _point_density(self, matrix: numpy.ndarray, i: int, j: int, zeros: int = 9) -> int:
        neighrs = []
        for di in [-1, 0, 1]:
            if i + di < 0 or i + di >= len(matrix):
                continue

            for dj in [-1, 0, 1]:
                if j + dj < 0 or j + dj >= len(matrix[i + di]):
                    continue
                
                neighrs.append(matrix[i + di, j + dj])

        if neighrs.count(0) > zeros:
            return 0

        return sum(neighrs) // len(neighrs)


if __name__ == '__main__':
    pass
