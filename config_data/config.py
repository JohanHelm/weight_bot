from dataclasses import dataclass

from environs import Env


@dataclass
class DatabaseConfig:
    db_file: str


@dataclass
class TgBot:
    token: str
    bot_pic: tuple[str]

@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env("BOT_TOKEN"),
            bot_pic=tuple(env("BOT_PIC").split(",")),
        ),
        db=DatabaseConfig(
            db_file=env('DB_FILE'),
        )
    )
