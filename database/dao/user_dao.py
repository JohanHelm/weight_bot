from database.dao.base_dao import GetOneItemDAO, AddOneItemDAO
from database.models import User


class UserAccessUserDAO(GetOneItemDAO,
                        AddOneItemDAO):
    model = User