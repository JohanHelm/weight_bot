from database.dao.base_dao import GetOneItemDAO, GetPackItemsDAO, AddOneItemDAO
from database.models import User


class UserAccessUserDAO(GetOneItemDAO,
                        GetPackItemsDAO,
                        AddOneItemDAO):
    model = User