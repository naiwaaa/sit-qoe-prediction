"""Keras implementation of Temporal Convolutional Neural Networks for QoE Prediction.

Code structure based on:
https://github.com/locuslab/TCN
https://github.com/philipperemy/keras-tcn
"""

from typing import List, Tuple

import keras.layers
from keras.engine.topology import Layer
from keras.layers import Activation, Lambda, Conv1D
from keras.initializers import TruncatedNormal


class CustomTCN:
    """Create a CustomTCN layer.

    Input shape:
        A tensor of shape (batch_size, timesteps, input_dim).

    Parameters
    ----------
        filters: int
            The number of filters to use in the convolutional layers.
        kernel_size: int
            The size of the kernel to use in each convolutional layer.
        dilations: List[int]
            The list of the dilations. Example is: [1, 2, 4, 8, 16, 32, 64].
        activation: str = {"relu", "selu", "wavenet"}
            The name of the type of activation to use.
        kernel_initializer: str = {"glorot_uniform", "he_uniform", "truncated_normal"}
            Initializer for the kernel weights matrix.
        use_skip_connections: bool
            If we want to add skip connections from input to each residual block.
        return_sequences: bool
            Whether to return the last output in the output sequence, or the full
            sequence.
        name: str
            Name of the model. Useful when having multiple TCN.

    Returns
    -------
        A CustomTCN layer.

    """

    def __init__(
        self,
        filters: int,
        kernel_size: int,
        dilations: List[int],
        kernel_initializer: str,
        return_sequences: bool,
        activation: str,
        use_skip_connections: bool,
        name: str = "custom_tcn",
    ):
        self.name = name
        self.filters = filters
        self.kernel_size = kernel_size
        self.dilations = _process_dilations(dilations)
        self.kernel_initializer = (
            TruncatedNormal(mean=0.0, stddev=0.05, seed=42)
            if kernel_initializer == "truncated_normal"
            else kernel_initializer
        )
        self.return_sequences = return_sequences
        self.activation = activation
        self.use_skip_connections = use_skip_connections

    def __call__(self, inputs):
        x = inputs

        # Causal conv to create channels
        x = Conv1D(
            filters=self.filters,
            kernel_size=self.kernel_size,
            padding="causal",
            kernel_initializer=self.kernel_initializer,
            name="initial_causal_conv",
        )(x)

        skip_connections = []
        for dilation in self.dilations:
            x, skip_out = self._temporal_block(
                x,
                filters=self.filters,
                kernel_size=self.kernel_size,
                dilation_rate=dilation,
                kernel_initializer=self.kernel_initializer,
                activation=self.activation,
            )
            skip_connections.append(skip_out)

        if self.use_skip_connections:
            x = keras.layers.add(skip_connections, name="skip_out_add")

        # if not self.return_sequences:
        #     x = Lambda(lambda tt: tt[:, -1:, :])(x)

        x = Activation(activation=self.activation)(x)  # TODO: "end" or "between"???
        x = Conv1D(
            filters=self.filters,
            kernel_size=1,
            activation=self.activation,
            kernel_initializer=self.kernel_initializer,
        )(x)
        x = Conv1D(
            1, 1, activation="linear", kernel_initializer=self.kernel_initializer
        )(x)

        if not self.return_sequences:
            x = Lambda(lambda tt: tt[:, -1:, :])(x)
        return x

    def _temporal_block(
        self,
        x: Layer,
        filters: int,
        kernel_size: int,
        dilation_rate: int,
        kernel_initializer: str,
        activation: str,
    ) -> Tuple[Layer, Layer]:
        """Define the residual block for the WaveNet TCN.

        Returns
        -------
            A tuple where the first element is the residual model layer, and the second
            is the skip connection.

        """
        net = x

        net = Conv1D(
            filters=filters,
            kernel_size=kernel_size,
            dilation_rate=dilation_rate,
            padding="causal",
            kernel_initializer=kernel_initializer,
            name=f"dilated_conv_d{dilation_rate}",
        )(net)
        net = Activation(activation)(net)

        skip_out = Conv1D(
            filters=1,  # TODO: =filters?
            kernel_size=1,
            # padding="same",  # TODO: delete?
            kernel_initializer=kernel_initializer,
            name=f"1x1_conv_d{dilation_rate}",
        )(net)

        out = keras.layers.add([skip_out, x])
        # out = Activation("relu")(out)

        return out, skip_out


def _process_dilations(dilations):
    def is_power_of_two(num):
        return num != 0 and ((num & (num - 1)) == 0)

    if all([is_power_of_two(i) for i in dilations]):
        return dilations
    else:
        new_dilations = [2 ** i for i in dilations]
        return new_dilations
