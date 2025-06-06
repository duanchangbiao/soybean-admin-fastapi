from app.core.crud import CRUDBase
from app.models.system.business import Account, Aft
from app.schemas.aft import AftCreate, AftUpdate


class AftController(CRUDBase[Aft, AftCreate, AftUpdate]):
    def __init__(self):
        super().__init__(model=Aft)

    async def get_by_account_number(self, account_number: str) -> Account | None:
        return await Account.filter(account_number=account_number).first()

    async def get_aft_by_apply_number(self, apply_number: str):
        return await self.model.filter(apply_number=apply_number).first()

    @staticmethod
    async def update_aft_account(aft: Aft, aft_account_id: int) -> bool:
        if not aft_account_id:
            return False
        if isinstance(aft_account_id, int):
            aft_account_id = int(aft_account_id)

        account = await Account.get(account_number=aft_account_id)
        await aft.by_aft_account.clear()
        await aft.by_aft_account.add(account)
        return True


aft_controller = AftController()
