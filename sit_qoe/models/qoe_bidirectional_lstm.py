from keras.models import Sequential
from keras.layers import LSTM, CuDNNLSTM, TimeDistributed, Bidirectional
from keras.layers import Dense

from .qoe_base import QoE_Base


class QoE_BidirectionalLSTM(QoE_Base):
    def __init__(self):
        super().__init__()

    def construct_model(self, input_shape=(2200, 3), units=(10, 10), gpu=False):
        LSTM_BLOCK = CuDNNLSTM if gpu else LSTM

        self.model = Sequential()
        self.model.add(
            Bidirectional(
                LSTM_BLOCK(units[0], return_sequences=True),
                merge_mode="concat",
                input_shape=input_shape,
            )
        )
        # self.model.add(Dropout(0.5))
        # self.model.add(
        #     Bidirectional(
        #         LSTM_BLOCK(units[0], return_sequences=True), merge_mode="concat"
        #     )
        # )
        # self.model.add(Dropout(0.5))
        self.model.add(LSTM_BLOCK(units[1], return_sequences=True))
        # self.model.add(Dropout(0.5))
        self.model.add(TimeDistributed(Dense(1)))
        self.model.compile(optimizer="rmsprop", loss="mean_squared_error")
