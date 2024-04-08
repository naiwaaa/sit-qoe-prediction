from typing import List

from keras import optimizers
from keras.models import Input, Model

from .tcn import Wavenet
from .qoe_base import QoE_Base


class QoE_Wavenet(QoE_Base):
    def __init__(
        self,
        batch_size: int,
        timesteps: int,
        input_dim: int,
        filters: int,
        kernel_size: int,
        dilation_rates: List[int],
        kernel_initializer: str,
        return_sequences: bool,
        learning_rate: float,
    ):
        super().__init__()
        self._construct_model(
            batch_size,
            timesteps,
            input_dim,
            filters,
            kernel_size,
            dilation_rates,
            kernel_initializer,
            return_sequences,
            learning_rate,
        )

    def _construct_model(
        self,
        batch_size: int,
        timesteps: int,
        input_dim: int,
        filters: int,
        kernel_size: int,
        dilation_rates: List[int],
        kernel_initializer: str,
        return_sequences: bool,
        learning_rate: float,
    ):
        inp = Input(batch_shape=(batch_size, timesteps, input_dim), name="input")

        out = Wavenet(
            filters=filters,
            kernel_size=kernel_size,
            dilation_rates=dilation_rates,
            kernel_initializer=kernel_initializer,
            return_sequences=return_sequences,
        )(inp)
        # out = Flatten()(out)
        # out = Dense(1)(out)
        # out = Lambda(lambda tt: tt[..., None])(out)

        self.model = Model(inputs=inp, outputs=out)
        self.model.compile(
            optimizer=optimizers.Adam(lr=learning_rate, clipnorm=1.0),
            loss="mean_squared_error",
        )

    # def predict(self, X):
    #     return self.model.predict(X)[..., None]
