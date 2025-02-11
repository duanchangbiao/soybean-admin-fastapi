from app.core.crud import CRUDBase
from app.models.system import Aft
from app.schemas.aft import AftCreate, AftUpdate


class AftController(CRUDBase[Aft, AftCreate, AftUpdate]):
    def __init__(self):
        super().__init__(model=Aft)


aft_controller = AftController()
