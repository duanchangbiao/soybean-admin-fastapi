from sympy import Q

from app.core.crud import CRUDBase
from app.models.system.business import Dict
from app.schemas.dict import DictCreate, DictUpdate


class DictController(CRUDBase[Dict, DictCreate, DictUpdate]):

    def __init__(self):
        super().__init__(model=Dict)

    async def get_by_dict_value(self, dict_type: str, dict_value: str):
        return await self.model.filter(data=dict_value, dict_type=dict_type).first()


dict_controller = DictController()
