"""Keras implementation of Temporal Convolutional Neural Networks for QoE Prediction.

Code structure based on:
https://github.com/locuslab/TCN
https://github.com/philipperemy/keras-tcn
"""

from typing import List, Tuple

import keras.layers
from keras.engine.topology import Layer
from keras.layers import Activation, Lambda
from keras.layers import Conv1D, SpatialDropout1D


class TCN:
    """Create an original TCN layer."""

    def __init__(
        self,
        filters: int,
        kernel_size: int,
        dilations: List[int],
        kernel_initializer: str,
        return_sequences: bool,
        dropout: float,
        name: str = "tcn",
    ):
        self.name = name
        self.filters = filters
        self.kernel_size = kernel_size
        self.dilations = _process_dilations(dilations)
        self.kernel_initializer = kernel_initializer
        self.return_sequences = return_sequences
        self.dropout = dropout

    def __call__(self, inputs):
        x = inputs

        for dilation in self.dilations:
            x = self._temporal_block(
                x,
                filters=self.filters,
                kernel_size=self.kernel_size,
                dilation_rate=dilation,
                kernel_initializer=self.kernel_initializer,
                dropout=self.dropout,
            )

        if not self.return_sequences:
            x = Lambda(lambda tt: tt[:, -1:, :])(x)

        x = Conv1D(1, 1, activation="linear")(x)
        return x

    def _temporal_block(
        self,
        x: Layer,
        filters: int,
        kernel_size: int,
        dilation_rate: int,
        dropout: float,
        kernel_initializer: str,
    ) -> Tuple[Layer, Layer]:
        """Define the residual block for the WaveNet TCN.

        Returns
        -------
            A tuple where the first element is the residual model layer, and the second
            is the skip connection.

        """
        net = x
        for i in range(2):
            net = Conv1D(
                filters=filters,
                kernel_size=kernel_size,
                dilation_rate=dilation_rate,
                padding="causal",
                kernel_initializer=kernel_initializer,
                name=f"dilated_conv_i{i}_d{dilation_rate}",
            )(net)
            net = keras.layers.BatchNormalization()(net)
            net = Activation("relu")(net)
            net = SpatialDropout1D(rate=dropout)(net)

        downsample = Conv1D(
            filters=filters,
            kernel_size=1,
            padding="same",
            kernel_initializer=kernel_initializer,
            name=f"1x1_conv_d{dilation_rate}",
        )(x)

        out = keras.layers.add([downsample, net])
        out = Activation("relu")(out)

        return out


def _process_dilations(dilations):
    def is_power_of_two(num):
        return num != 0 and ((num & (num - 1)) == 0)

    if all([is_power_of_two(i) for i in dilations]):
        return dilations
    else:
        new_dilations = [2 ** i for i in dilations]
        return new_dilations
