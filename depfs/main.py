import numpy
from distribution import Distribution
from converter import Converter
from cmaes import CMAES


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    nbunch = 5
    nparams = 15

    path = "./pickles"
    conv = Converter(path)

    dataset = conv.read()
    train, test = dataset.split(nbunch)

    distribution = Distribution(nparams)
    cma_es = CMAES(distribution)

    c = cma_es.run(train[0])
    for i in c:
        print(i)

    # spectrums = train[0].data_x()
    # peaks = train[0].data_y()

    # for i in range(len(peaks)):
    #     plt.plot(numpy.arange(1, len(spectrums[i]) + 1), spectrums[i], color='black')
    #     plt.scatter(peaks[i], [spectrums[i][peaks[i][j] - 1] for j in range(len(peaks[i]))], color='red')
    #     plt.show()

    # cma_es.execute(train)
    # cma_es.test(test)

    # cma_es.save()
