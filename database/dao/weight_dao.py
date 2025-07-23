from database.dao.base_dao import GetPackItemsDAO, AddOneItemDAO
from database.models import Weights


class UserAccessWeightsDAO(GetPackItemsDAO,
                           AddOneItemDAO):
    model = Weights