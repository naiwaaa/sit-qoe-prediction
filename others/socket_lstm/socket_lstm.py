#!/usr/bin/env python3

import sys
import os
import atexit
import socket

import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from qoe_lstm import QoE_LSTM  # noqa

PORT = 12347

model = None
client_data = {}


def main():
    global client_data
    atexit.register(save_input)
    load_model()

    with socket.socket() as s:
        s.bind(("localhost", PORT))
        print(f"Socket successfully created at {PORT}")
        s.listen(5)
        print("Socket is listening...")
        try:
            while True:
                conn, addr = s.accept()
                print(f"Connected by {addr}")

                data = conn.recv(1024)
                if not data:
                    break
                data = data.decode()
                print(f"Data received: {data}")

                client_id, input_features = process_data(data)
                output = retrieve_output(client_id, input_features)
                client_data[client_id][3].append(output)
                conn.send("{0:.4f}".format(output).encode())

                print("Data send: ", "{0:.4f}".format(output))

        except Exception as ex:
            print(ex)
        finally:
            save_input()


def load_model():
    global model
    model = QoE_LSTM()
    model.construct_model(input_shape=(2200, 3), units=(22, 22), gpu=True)
    model.summary()
    model.load("./model_lstm_PsnrPiTr_20e_qoe-noscaled_gpu.h5")


def process_data(data):
    global client_data
    client_id, stsq, tr = data.split(";")
    pi = 1 if float(tr) < 1e-6 else 0
    if client_id in client_data:
        client_data[client_id][0].append(float(stsq))
        client_data[client_id][1].append(float(pi))
        client_data[client_id][2].append(float(tr))
    else:
        client_data[client_id] = [[float(stsq)], [float(pi)], [float(tr)], []]

    input_features = np.vstack(
        [
            np.vstack(
                [
                    client_data[client_id][0],
                    client_data[client_id][1],
                    client_data[client_id][2],
                ]
            ).T,
            np.zeros([2200 - len(client_data[client_id][0]), 3]),
        ]
    ).reshape([1, 2200, 3])

    return client_id, input_features


def retrieve_output(client_id, input_features):
    global model, client_data
    output_qoe = model.predict(input_features)[0, :, 0][len(client_data[client_id][0])]
    return output_qoe


def save_input():
    global client_data
    import pickle as pkl

    with open("data.pkl", "wb") as file:
        pkl.dump(client_data, file)


if __name__ == "__main__":
    main()
