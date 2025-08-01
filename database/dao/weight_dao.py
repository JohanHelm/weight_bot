from database.dao.base_dao import (
    AddOneItemDAO,
    GetAwgDataDAO,
    GetCountItemsDAO,
    GetOneItemDAO,
    GetPackItemsDAO,
)
from database.models import Weights


class UserAccessWeightsDAO(GetAwgDataDAO,
                           GetCountItemsDAO,
                           AddOneItemDAO,
                           GetOneItemDAO,
                           GetPackItemsDAO,
                           ):
    model = Weights