import numpy
from matplotlib.axes import Axes


class Painter:
    def __init__(self):
        pass

    def draw_matrix(self, axes: Axes, matrix: numpy.ndarray) -> None:
        axes.clear()

        logarithmed = numpy.log(matrix)
        minimum = 0; maximum = int(0.75 * logarithmed.max())

        axes.pcolor(logarithmed, vmin=minimum, vmax=maximum, cmap='rainbow')

    def draw_matrix_slices(self, axes: Axes, matrix: numpy.ndarray, completed: list[int], incompleted: list[int]) -> None:
        axes.clear()
        self.draw_matrix(axes, matrix)

        for i in completed:
            axes.plot([i, i], [1, len(matrix)], color='darkblue')

        for i in incompleted:
            axes.plot([i, i], [1, len(matrix)], color='red')

    def draw_spectrum(self, axes: Axes, spectrum: numpy.ndarray) -> None:
        axes.clear()

        axes.plot(numpy.arange(1, len(spectrum) + 1), spectrum, color='blue')
        for i in range(len(spectrum)):
            axes.plot([i + 1, i + 1], [0, spectrum[i]], color='blue')

    def draw_pointers(self, axes: Axes, spectrum: numpy.ndarray, xs: list[float]) -> None:
        axes.clear()
        self.draw_spectrum(axes, spectrum)

        for x in xs:
            nearest = int(round(x))
            axes.scatter(nearest, spectrum[nearest - 1], color='red')


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    rank = 128
    mtx = 1000 * numpy.random.random((rank, rank))
    randinx = numpy.random.randint(rank*rank, size=int(0.5*rank*rank))

    for i in randinx:
        mtx[i // rank, i % rank] = 0

    logged = numpy.log(mtx)

    plt.pcolor(logged, vmin=0, vmax=6)
    plt.show()
