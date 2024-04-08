from typing import List, Tuple

import keras.layers
from keras.engine.topology import Layer
from keras.layers import Activation, Lambda, Conv1D


class Wavenet:
    def __init__(
        self,
        filters: int,
        kernel_size: int,
        dilation_rates: List[int],
        kernel_initializer: str,
        return_sequences: bool,
        name: str = "wavenet",
    ):
        self.name = name
        self.filters = filters
        self.kernel_size = kernel_size
        self.dilation_rates = dilation_rates
        self.kernel_initializer = kernel_initializer
        self.return_sequences = return_sequences

    def __call__(self, inputs):
        x = inputs

        # causal conv
        x = Conv1D(
            filters=self.filters,
            kernel_size=self.kernel_size,
            padding="causal",
            kernel_initializer=self.kernel_initializer,
            name="initial_causal_conv",
        )(x)

        skip_connections = []
        for dilation_rate in self.dilation_rates:
            x, skip_out = self._residual_block(
                x,
                filters=self.filters,
                kernel_size=self.kernel_size,
                dilation_rate=dilation_rate,
                kernel_initializer=self.kernel_initializer,
            )
            skip_connections.append(skip_out)

        x = keras.layers.add(skip_connections, name="skip_out_add")
        if not self.return_sequences:
            x = Lambda(lambda tt: tt[:, -1:, :])(x)
        x = Activation(activation="relu")(x)
        x = Conv1D(
            self.filters,
            1,
            # padding="same",  # TODO: delete padding ???
            activation="relu",
        )(x)
        x = Conv1D(
            1,
            1,
            activation="relu",
            # padding="same"
        )(x)
        return x

    def _residual_block(
        self,
        x: Layer,
        filters: int,
        kernel_size: int,
        dilation_rate: int,
        kernel_initializer: str,
    ) -> Tuple[Layer, Layer]:
        net = x

        tanh_out = Conv1D(
            filters=filters,
            kernel_size=kernel_size,
            dilation_rate=dilation_rate,
            padding="causal",
            activation="tanh",
            kernel_initializer=kernel_initializer,
            name=f"dilated_conv_d{dilation_rate}_tanh",
        )(net)
        sigmoid_out = Conv1D(
            filters=filters,
            kernel_size=kernel_size,
            dilation_rate=dilation_rate,
            padding="causal",
            activation="sigmoid",
            kernel_initializer=kernel_initializer,
            name=f"dilated_conv_d{dilation_rate}_sigmoid",
        )(net)

        gated = keras.layers.multiply(
            [tanh_out, sigmoid_out], name=f"gated_d{dilation_rate}"
        )

        skip_out = Conv1D(
            filters=filters,  # TODO: 1 ???
            kernel_size=1,
            padding="same",  # TODO: delete ???
            # activation="relu",  # TODO: linear ???
            kernel_initializer=kernel_initializer,
            name=f"skipout_d{dilation_rate}",
        )(gated)

        # res_x = Conv1D(
        #     filters=self.filters,  # TODO: 1 ???
        #     kernel_size=1,
        #     padding="same",  # TODO: delete ???
        #     # activation="relu",  # TODO: linear ???
        #     kernel_initializer=kernel_initializer,
        #     name=f"res_d{dilation_rate}",
        # )(gated)

        out = keras.layers.add([skip_out, x], name=f"residual_out_d{dilation_rate}")

        return out, skip_out
