from dishka import Provider, Scope, provide
from sqlalchemy.orm import Session

from database.dao.user_dao import UserAccessUserDAO
from database.dao.weight_dao import UserAccessWeightsDAO
from config_data.config import Config, TgBot
from database.connection import get_db_session


class MyProvider(Provider):
    def __init__(self, config: Config):
        super().__init__()
        self.db_session: Session = get_db_session(config)
        self.config = config


    @provide(scope=Scope.APP)
    async def get_bot_config(self) -> TgBot:
        return self.config.tg_bot


    @provide(scope=Scope.REQUEST)
    async def get_user_dao(self) -> UserAccessUserDAO:
        return UserAccessUserDAO(self.db_session)


    @provide(scope=Scope.REQUEST)
    async def get_weight_dao(self) -> UserAccessWeightsDAO:
        return UserAccessWeightsDAO(self.db_session)
