from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from config_data.config import Config
from config_data.initial_settings import AppParams


class Base(DeclarativeBase):
    pass


def get_db_session(config: Config) -> Session:
    sqlite_database = f"{AppParams.db_type}:///{config.db.db_file}"
    engine = create_engine(sqlite_database)
    with Session(autoflush=False, bind=engine) as session:
        return session
