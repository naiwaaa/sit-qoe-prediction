import numpy as np
from keras.models import load_model

from ..utils import GetBest, metrics


class QoE_Base:
    def __init__(self):
        self.model = None
        self.history = None

    def summary(self):
        print(self.model.summary())

    def fit(
        self,
        X,
        y,
        epochs=1500,
        shuffle=False,
        batch_size=None,
        verbose=2,
        validation_split=None,
        validation_data=None,
    ):
        callbacks = [
            GetBest(
                monitor="loss"
                if validation_data is None and validation_split is None
                else "val_loss",
                verbose=verbose,
                mode="min",
            )
        ]
        self.history = self.model.fit(
            X,
            y,
            epochs=epochs,
            shuffle=shuffle,
            batch_size=batch_size,
            verbose=verbose,
            validation_split=validation_split,
            validation_data=validation_data,
            callbacks=callbacks,
        )

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, test_set, verbose=1):
        y_pred = self.predict(test_set.X).flatten()
        y_test = test_set.y.flatten()

        loss = self.model.evaluate(test_set.X, test_set.y, verbose=0)
        pcc = metrics.PCC(y_pred, y_test)
        srocc = metrics.SROCC(y_pred, y_test)
        rmse = metrics.RMSE(y_pred, y_test)
        if verbose == 1:
            print(f"Loss:\t{loss}")
            print(f"PCC:\t{pcc}")
            print(f"SROCC:\t{srocc}")
            print(f"RMSE:\t{rmse}")

        return {"loss": loss, "srocc": srocc, "pcc": pcc, "rmse": rmse}

    def _evaluate(self, test_set, verbose=1, OR=False, padding=False):
        y_pred = self.predict(test_set.X)
        y_test = test_set.y

        pcc_per_test_samples = []
        srocc_per_test_samples = []
        rmse_per_test_samples = []
        or_per_test_samples = []
        for i in range(0, test_set.y.shape[0]):
            if padding:
                start = -test_set[i].len_in_sec
            else:
                start = 0
            pcc_per_test_samples.append(
                metrics.PCC(y_test[i, start:, 0:1], y_pred[i, start:, 0])
            )
            srocc_per_test_samples.append(
                metrics.SROCC(y_test[i, start:, 0], y_pred[i, start:, 0])
            )
            rmse_per_test_samples.append(
                metrics.RMSE(y_test[i, start:, 0], y_pred[i, start:, 0])
            )
            if OR:
                or_per_test_samples.append(
                    metrics.OR(
                        y_test[i, start:, 0],
                        y_pred[i, start:, 0],
                        test_set[i].qoe_continuous_CIhigh
                        - test_set[i].qoe_continuous_CIlow,
                    )
                )

        loss = self.model.evaluate(test_set.X, test_set.y, verbose=0)
        pcc_mean, pcc_std = np.mean(pcc_per_test_samples), np.std(pcc_per_test_samples)
        srocc_mean, srocc_std = (
            np.mean(srocc_per_test_samples),
            np.std(srocc_per_test_samples),
        )
        rmse_mean, rmse_std = (
            np.mean(rmse_per_test_samples),
            np.std(rmse_per_test_samples),
        )
        or_mean, or_std = np.mean(or_per_test_samples), np.std(or_per_test_samples)

        if verbose == 1:
            print(f"Loss:\t{loss}")
            print(f"PCC:\t{pcc_mean} ± {pcc_std}")
            print(f"SROCC:\t{srocc_mean} ± {srocc_std}")
            print(f"RMSE:\t{rmse_mean} ± {rmse_std}")
            print(f"OR:\t{or_mean} ± {or_std}")

        return {
            "loss": loss,
            "srocc": srocc_mean,
            "pcc": pcc_mean,
            "rmse": rmse_mean,
            "or": or_mean,
        }

    def visualize_learning_curves(self, axis, start_idx=0):
        axis.set_title("Learning curves")
        axis.set_xlabel("epoch")
        axis.set_ylabel("loss")
        axis.plot(self.history.history["loss"][start_idx:], label="train")
        if "val_loss" in self.history.history:
            axis.plot(self.history.history["val_loss"][start_idx:], label="validation")
        axis.legend(loc="upper right")

    def save(self, model_path):
        self.model.save(model_path)

    def save_weights(self, model_path):
        self.model.save_weights(model_path)

    def load(self, model_path):
        self.model = load_model(model_path)

    def load_weights(self, model_path):
        self.model.load_weights(model_path)
