from database.dao.base_dao import AddOneItemDAO, GetAwgDataDAO, GetCountItemsDAO
from database.models import Weights


class UserAccessWeightsDAO(GetAwgDataDAO,
                           GetCountItemsDAO,
                           AddOneItemDAO):
    model = Weights