import numpy
import keras
import tensorflow
from scipy.ndimage import label


@keras.saving.register_keras_serializable(package="MyHooks")
def combined_loss(y_true: tensorflow.Tensor, y_pred: tensorflow.Tensor) -> tensorflow.Tensor:
    smooth: float = 1e-6

    y_true = tensorflow.cast(y_true, tensorflow.float32)

    intersection: tensorflow.Tensor = tensorflow.reduce_sum(y_true * y_pred)
    union: tensorflow.Tensor = tensorflow.reduce_sum(y_true) + tensorflow.reduce_sum(y_pred)

    dice = (2.0 * intersection + smooth) / (union + smooth)
    bce = tensorflow.keras.losses.binary_crossentropy(y_true,y_pred)

    return 0.5 * bce + 0.5 * (1.0 - dice)


class Depfinn:
    def __init__(self, input_length: int = 256, learning_rate: float = 1e-3) -> None:
        self._input_length: int = input_length
        self._learning_rate: float = learning_rate
        self._model: keras.models.Model = self._build_model()
        self._compile_model()

    def _build_model(self) -> keras.models.Model:
        inputs: keras.layers.Layer = keras.layers.Input(shape=(self._input_length, 1))

        x = keras.layers.Conv1D(32, 5, padding="same")(inputs)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.Activation("relu")(x)

        x = keras.layers.Conv1D(64, 5, padding="same")(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.Activation("relu")(x)

        x = keras.layers.Conv1D(64, 7, padding="same")(x)
        x = keras.layers.Activation("relu")(x)

        outputs = keras.layers.Conv1D(1, 1, activation="sigmoid")(x)

        return keras.models.Model(inputs, outputs)

    def _compile_model(self) -> None:
        self._model.compile(
            optimizer=tensorflow.keras.optimizers.Adam(learning_rate=self._learning_rate),
            loss=combined_loss,
            metrics=["accuracy"]
        )

    def train(
        self,
        X_train: numpy.ndarray,
        Y_train: numpy.ndarray,
        X_val: numpy.ndarray = None,
        Y_val: numpy.ndarray = None,
        batch_size: int = 32,
        epochs: int = 500
    ) -> keras.callbacks.History:

        callbacks = [keras.callbacks.EarlyStopping(patience=30, restore_best_weights=True, start_from_epoch=10)]

        history = self._model.fit(
            X_train,
            Y_train,
            validation_data=(X_val, Y_val)
            if X_val is not None and Y_val is not None
            else None,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks
        )

        return history

    def predict_mask(self, X: numpy.ndarray, threshold: float = 0.5) -> numpy.ndarray:
        preds = self._model.predict(X)
        return (preds > threshold).astype(numpy.int32)

    def predict_peaks(self, X: numpy.ndarray, threshold: float = 0.5) -> list[list[int]]:
        binary_masks = self.predict_mask(X, threshold)
        all_peaks = []

        for sample in binary_masks:
            labeled_array, num_features = label(sample[:, 0])
            peak_positions = []

            for i in range(1, num_features + 1):
                indices = numpy.where(labeled_array == i)[0]
                center = int(indices.mean())
                peak_positions.append(center)

            all_peaks.append(peak_positions)

        return all_peaks

    def save(self, path: str) -> bool:
        self._model.save(path)
        return True

    def load(self, path: str) -> None:
        self._model = keras.models.load_model(path, custom_objects={"combined_loss": combined_loss})


if __name__ == "__main__":
    pass
