from keras import optimizers
from keras.models import Sequential
from keras.layers import LSTM, CuDNNLSTM, TimeDistributed, Dense

from .qoe_base import QoE_Base


class QoE_LSTM(QoE_Base):
    def __init__(self):
        super().__init__()

    def construct_model(
        self, input_shape=(2200, 3), units=(32, 32), learning_rate=0.001, gpu=False
    ):
        LSTM_BLOCK = CuDNNLSTM if gpu else LSTM
        self.model = Sequential()

        for i, _ in enumerate(units):
            layer = (
                LSTM_BLOCK(units[i], return_sequences=True, input_shape=input_shape)
                if i == 0
                else LSTM_BLOCK(units[i], return_sequences=True)
            )
            self.model.add(layer)
        self.model.add(TimeDistributed(Dense(1)))

        self.model.compile(
            optimizer=optimizers.Adam(lr=learning_rate, clipnorm=1.0),
            loss="mean_squared_error",
        )
