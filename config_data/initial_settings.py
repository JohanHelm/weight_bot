from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LogParams:
    loglevel: int = 10 #debug
    log_max_size: int = 10
    log_file_mode: str = "w"
    backup_count: int = 10
    logs_encoding: str = "utf-8"


@dataclass(frozen=True)
class PathParams:
    workdir: Path = Path().resolve()
    logs_catalog = workdir.joinpath("logs")
    bot_logfile = logs_catalog.joinpath("weight_bot.log")


# @dataclass(frozen=True)
# class PlotParams:
#     plot_title: str = "Результаты измерений за "
#     label_temp: str = "Температура, °C"
#     label_hum: str = "Влажность, %"
#     plot_format: str = "png"
#     records_limit: int = 30
#     every_on_x_axis: int = 5
#     img_filename: str = "image from buffer.png"
