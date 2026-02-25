import numpy
from distribution import Distribution
from converter import Converter
from dataset import Dataset
from bunch import Bunch
from cmaes import CMAES


if __name__ == '__main__':
    nparams = 15
    path = "./pickles"
    conv = Converter(path)
    dataset = conv.read()

    distribution = Distribution(nparams)
    cma_es = CMAES(distribution)

    cma_es.execute(dataset)
    cma_es.save()
