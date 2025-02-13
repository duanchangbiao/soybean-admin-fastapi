from app.core.crud import CRUDBase
from app.models.system.business import Dict
from app.schemas.dict import DictCreate, DictUpdate


class DictController(CRUDBase[Dict, DictCreate, DictUpdate]):

    def __init__(self):
        super().__init__(model=Dict)


dict_controller = DictController()
