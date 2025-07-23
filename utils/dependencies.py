from dishka import Provider, Scope, provide
from sqlalchemy.orm import Session

from database.dao.user_dao import UserAccessUserDAO
from config_data.config import Config


class MyProvider(Provider):
    def __init__(self, db_session: Session):
        super().__init__()
        self.db_session = db_session

    #
    # @provide(scope=Scope.APP)
    # async def get_int(self) -> AsyncIterator[int]:
    #     print("solve int")
    #     yield random.randint(0, 10000)

    @provide(scope=Scope.REQUEST)
    async def get_user_dao(self) -> UserAccessUserDAO:
        return UserAccessUserDAO(self.db_session)

    # @provide(scope=Scope.REQUEST)
    # async def get_chat(self, middleware_data: AiogramMiddlewareData) -> Chat | None:
    #     return middleware_data.get("event_chat")