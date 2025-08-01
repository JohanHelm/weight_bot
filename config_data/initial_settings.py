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

@dataclass(frozen=True)
class AppParams:
    db_type: str = "sqlite"
    minimal_interval: int = 7
    threshold_percent: float = 1.5


@dataclass(frozen=True)
class PlotParams:
    y_label: str = "Вес, кг"
    x_label: str = "Дата"
    plot_format: str = "png"
    img_filename: str = "image from buffer.png"
    width: int = 10
    height: int = 7
    plot_label: str = "Вес"
    x_label_rotation: int = 90
    marker: str = 'o'
    trend_label="Тренд"
    trend_color = "red"
