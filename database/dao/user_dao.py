from database.dao.base_dao import AddOneItemDAO, GetOneItemDAO
from database.models import User


class UserAccessUserDAO(GetOneItemDAO,
                        AddOneItemDAO):
    model = User