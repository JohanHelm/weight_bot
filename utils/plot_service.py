from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame

from config_data.initial_settings import PlotParams


def create_plot(two_weeks_df: DataFrame) -> BytesIO:
    dates = two_weeks_df.date.values
    plt.figure(figsize=(PlotParams.width, PlotParams.height))
    plt.plot(dates, two_weeks_df.weight, label=PlotParams.plot_label, marker=PlotParams.marker)
    plt.xticks(dates, dates, rotation=PlotParams.x_label_rotation)

    x = np.arange(len(two_weeks_df))
    z = np.polyfit(x, two_weeks_df.weight, deg=1)
    trend = np.poly1d(z)
    plt.plot(dates, trend(x), label=PlotParams.trend_label, color=PlotParams.trend_color)

    plt.xlabel(PlotParams.x_label)
    plt.ylabel(PlotParams.y_label)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    img_bytes = BytesIO()
    plt.savefig(img_bytes, format=PlotParams.plot_format)
    img_bytes.seek(0)

    plt.clf()
    plt.close()
    return img_bytes
