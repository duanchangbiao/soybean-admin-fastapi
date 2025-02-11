from app.core.crud import CRUDBase
from app.models.system import Aft, Account
from app.schemas.aft import AftCreate, AftUpdate


class AftController(CRUDBase[Aft, AftCreate, AftUpdate]):
    def __init__(self):
        super().__init__(model=Aft)

    async def create(self, obj_in: AftCreate) -> Aft:  # type: ignore
        return await super().create(obj_in, exclude={"byAftAccount"})

    async def update(self, aft_id: int, obj_in: AftUpdate) -> Aft:  # type: ignore
        return await super().update(id=aft_id, obj_in=obj_in, exclude={"byAftAccount"})

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

    @staticmethod
    async def update_account_by_aft(aft: Aft, account_id: int) -> bool:
        if not account_id:
            return False

        if isinstance(account_id, int):
            account_id = int(account_id)

        account_objs = await Account.get(id=account_id)
        print("user_role_objs", account_objs)
        await aft.by_aft_account.clear()
        await aft.by_aft_account.add(account_id)

        return True


aft_controller = AftController()
