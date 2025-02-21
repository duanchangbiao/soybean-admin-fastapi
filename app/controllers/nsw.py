from app.core.crud import CRUDBase
from app.models.system.business import Nsw, Account
from app.schemas.nsw import NswCreate, NswUpdate


class NswController(CRUDBase[Nsw, NswCreate, NswUpdate]):
    def __init__(self):
        super().__init__(model=Nsw)

    async def get_by_account_number(self, account_number: str) -> Account | None:
        return await Account.filter(account_number=account_number).first()

    async def get_nsw_by_apply_number(self, apply_number: str):
        return await self.model.filter(apply_number=apply_number).first()

    @staticmethod
    async def update_nsw_account(nsw: Nsw, nsw_account_id: int) -> bool:
        if not nsw_account_id:
            return False
        if isinstance(nsw_account_id, int):
            nsw_account_id = int(nsw_account_id)

        account = await Account.get(account_number=nsw_account_id)
        print("account info:", await account.to_dict())
        await nsw.by_nsw_account.clear()
        await nsw.by_nsw_account.add(account)
        return True


nsw_controller = NswController()
