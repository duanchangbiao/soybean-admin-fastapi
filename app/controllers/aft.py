from app.core.crud import CRUDBase
from app.models.system import Aft, Account
from app.schemas.aft import AftCreate, AftUpdate


class AftController(CRUDBase[Aft, AftCreate, AftUpdate]):
    def __init__(self):
        super().__init__(model=Aft)

    @staticmethod
    async def update_aft_account(aft: Aft, aft_account_id: int) -> bool:
        if not aft_account_id:
            return False
        if isinstance(aft_account_id, int):
            aft_account_id = int(aft_account_id)

        account = await Account.get(id=aft_account_id)
        print("account info:", account)
        await aft.by_aft_account.clear()
        await aft.by_aft_account.add(account)


aft_controller = AftController()
