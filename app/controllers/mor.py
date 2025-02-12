from app.core.crud import CRUDBase
from app.models.system.business import Mor, Account
from app.schemas.mor import MorCreate, MorUpdate


class MorController(CRUDBase[Mor, MorCreate, MorUpdate]):

    def __init__(self):
        super().__init__(model=Mor)

    async def get_by_account_number(self, account_number: str) -> Account | None:
        return await Account.filter(account_number=account_number).first()

    @staticmethod
    async def update_mor_account(mor: Mor, mor_account_id: int) -> bool:
        if not mor_account_id:
            return False
        if isinstance(mor_account_id, int):
            mor_account_id = int(mor_account_id)

        account = await Account.get(account_number=mor_account_id)
        print("account info:", account.to_dict())
        await mor.by_mor_account.clear()
        await mor.by_mor_account.add(account)
        return True


mor_controller = MorController()
