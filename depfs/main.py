import numpy
from distribution import Distribution
from converter import Converter
from cmaes import CMAES


if __name__ == '__main__':
    nbunch = 5
    nparams = 15

    path = "./pickles"
    conv = Converter(path)

    dataset = conv.read()
    train, test = dataset.split(nbunch)

    distribution = Distribution(nparams)
    cma_es = CMAES(distribution)

    cma_es.execute(train)
    cma_es.test(test)

    cma_es.save()
