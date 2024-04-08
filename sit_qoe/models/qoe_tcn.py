from typing import List

from keras import optimizers
from keras.models import Input, Model

from .tcn import TCN
from .qoe_base import QoE_Base

# from sit_qoe.utils import losses


class QoE_TCN(QoE_Base):
    def __init__(self):
        super().__init__()

    def construct_model(
        self,
        batch_size: int,
        timesteps: int,
        input_dim: int,
        filters: int,
        kernel_size: int,
        dilations: List[int],
        kernel_initializer: str,
        return_sequences: bool,
        learning_rate: float,
        dropout: float,
    ):
        inp = Input(batch_shape=(batch_size, timesteps, input_dim), name="input")

        out = TCN(
            filters=filters,
            kernel_size=kernel_size,
            dilations=dilations,
            kernel_initializer=kernel_initializer,
            return_sequences=return_sequences,
            dropout=dropout,
        )(inp)

        self.model = Model(inputs=inp, outputs=out, name="QoE_TCN")
        self.model.compile(
            optimizer=optimizers.Adam(lr=learning_rate),
            loss="mse",
            # loss=losses.root_mean_squared_error,
        )