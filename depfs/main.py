import numpy
import matplotlib.pyplot as plt

from cmaes import CMAES
from depfinn import Depfinn
from adapter import Adapter
from converter import Converter
from distribution import Distribution


def depfs() -> None:
    nbunch = 5
    nparams = 15

    path = "./pickles"
    conv = Converter(path)

    dataset = Adapter(conv.read())
    train, test = dataset.to_depfs(nbunch)

    distribution = Distribution(nparams)
    cmaes = CMAES(distribution)

    best = cmaes.execute(train)
    loss = cmaes.test(test)
    cmaes.save("cmaes.txt")


def depfinn() -> None:
    path = "./pickles"
    conv = Converter(path)

    dataset = Adapter(conv.read())

    X_train, Y_train, X_test, Y_test = dataset.to_depfinn()

    print("Train shape:", X_train.shape, Y_train.shape)
    print("Test shape:", X_test.shape, Y_test.shape)

    detector = Depfinn(input_length=256, learning_rate=1e-2)

    history = detector.train(
        X_train,
        Y_train,
        X_val=X_test,
        Y_val=Y_test,
        batch_size=32,
        epochs=100
    )

    loss, accuracy = detector._model.evaluate(X_test, Y_test)
    print("Test loss:", loss)
    print("Test accuracy:", accuracy)

    detector.save("./saved/v1.keras")


if __name__ == '__main__':
    depfs()
