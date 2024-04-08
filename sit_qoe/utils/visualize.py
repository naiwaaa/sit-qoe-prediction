from .preprocess import to_sec

friendly_colors = {
    "orange": "#E69F00",
    "blue": "#56B4E9",
    "green": "#009E73",
    "yellow": "#F0E442",
    "red": "#D55E00",
    "darkblue": "#0072B2",
    "pink": "#CC79A7",
}


def visualize_twinx(axis, x_label, y1_data, y1_style, y2_data=None, y2_style=None):
    axis.set_xlabel(x_label)
    axis.set_ylabel(y1_style["label"], color=y1_style["color"])
    axis.plot(y1_data, **y1_style)

    if y2_data is not None:
        second_axis = axis.twinx()
        second_axis.set_ylabel(y2_style["label"], color=y2_style["color"])
        second_axis.plot(y2_data, **y2_style)
    return axis, second_axis


def visualize_qoe_predicted(
    axis,
    y_test,
    y_pred,
    idx=0,
    test_video=None,
    tosec=False,
    legend=True,
    rebuff=True,
    ci=True,
):
    axis.set_xlabel("Time (seconds)")
    axis.set_ylabel("QoE")

    if tosec and test_video is not None:
        y_test = to_sec(y_test, test_video)
        y_pred = to_sec(y_pred, test_video)

    axis.plot(y_test, linestyle="--", label="Subjective QoE")
    axis.plot(y_pred, label="Predicted QoE")

    if rebuff and test_video is not None:
        axis.fill_between(
            range(0, y_test.shape[0]),
            axis.get_ylim()[0],
            axis.get_ylim()[1],
            where=test_video.playback_indicator[-y_test.shape[0] :] == 1,
            facecolor="#0F0F0F0F",
            label="Rebuffering",
            interpolate=True,
        )
    if ci and test_video is not None and test_video.qoe_continuous_CIhigh is not None:
        axis.fill_between(
            range(0, y_test.shape[0]),
            test_video.qoe_continuous_CIhigh[-y_test.shape[0] :],
            test_video.qoe_continuous_CIlow[-y_test.shape[0] :],
            facecolor="#0F0F0F0F",
            label="95% CI",
            interpolate=True,
        )
    if legend:
        axis.legend()
    return axis
