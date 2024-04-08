import numpy as np
import tensorflow as tf
import keras.backend as K
from keras.models import load_model
from scipy.stats import pearsonr, spearmanr


def PCC(y_actual, y_pred):
    return pearsonr(y_pred, y_actual)[0]


def SROCC(y_actual, y_pred):
    return spearmanr(y_actual, y_pred, axis=0)[0]


def MSE(y_actual, y_pred):
    return np.mean(np.subtract(y_actual, y_pred) ** 2)


def RMSE(y_actual, y_pred):
    return np.sqrt(MSE(y_actual, y_pred))


def OR(y_actual, y_pred, epsilon):
    outage = []

    for i, val in enumerate(epsilon):
        if abs(y_actual[i] - y_pred[i]) > val:
            outage.append(i)

    return (len(outage) / float(len(epsilon))) * 100


def FLOPS_keras(model_file):
    run_meta = tf.RunMetadata()
    with tf.Session(graph=tf.Graph()) as sess:
        K.set_session(sess)
        _ = load_model(model_file)

        opts = tf.profiler.ProfileOptionBuilder.float_operation()
        flops = tf.profiler.profile(
            sess.graph, run_meta=run_meta, cmd="op", options=opts
        )

        opts = tf.profiler.ProfileOptionBuilder.trainable_variables_parameter()
        params = tf.profiler.profile(
            sess.graph, run_meta=run_meta, cmd="op", options=opts
        )

        # print("{:,} --- {:,}".format(flops.total_float_ops, params.total_parameters))
        return {
            "flops": flops.total_float_ops,
            "total_parameters": params.total_parameters,
        }


def FLOPS_pb(model_file):
    def _load_pb(pb):
        with tf.gfile.GFile(pb, "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def, name="")
            return graph

    graph = _load_pb(model_file)
    with graph.as_default():
        flops = tf.profiler.profile(
            graph, options=tf.profiler.ProfileOptionBuilder.float_operation()
        )

    return flops.total_float_ops


# def FLOPS_pb_v2(model_file):
#     run_meta = tf.RunMetadata()
#     with tf.Graph().as_default():
#         output_graph_def = graph_pb2.GraphDef()
#         with open(model_file, "rb") as f:
#             output_graph_def.ParseFromString(f.read())
#             _ = importer.import_graph_def(output_graph_def, name="")
#             print("model loaded!")
#         all_keys = sorted([n.name for n in tf.get_default_graph().as_graph_def().node])
#         # for k in all_keys:
#         #   print(k)

#         with tf.Session() as sess:
#             _ = sess.run(
#                 train_op,
#                 options=tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE),
#                 run_metadata=run_metadata,
#             )
#             flops = tf.profiler.profile(
#                 tf.get_default_graph(),
#                 run_meta=run_meta,
#                 options=tf.profiler.ProfileOptionBuilder.float_operation(),
#             )
#             return flops.total_float_ops
