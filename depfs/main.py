import numpy
import matplotlib.pyplot as plt

from distribution import Distribution
from converter import Converter
from depfinn import Depfinn
from cmaes import CMAES


def depfs() -> None:
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

def depfinn() -> None:
    path = "./pickles"
    conv = Converter(path)

    dataset = conv.read()

    X_train = dataset.train_x()
    Y_train = dataset.train_y()

    X_test = dataset.test_x()
    Y_test = dataset.test_y()

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

    predicted_peaks = detector.predict_peaks(X_test)

    # for i, peaks in enumerate(predicted_peaks):
    #     plt.plot(numpy.arange(1, len(X_test[i]) + 1), X_test[i], color='black')
    #     plt.plot(numpy.arange(1, len(Y_test[i]) + 1), Y_test[i], color='red')
    #     plt.scatter(peaks, [X_test[i][j - 1] for j in peaks], color='blue')
    #     plt.show()

    detector.save("./saved/v1.keras")


if __name__ == '__main__':
    depfinn()
