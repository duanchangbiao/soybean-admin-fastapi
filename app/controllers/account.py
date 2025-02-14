from app.core.crud import CRUDBase
from app.models.system.business import Account, Dict
from app.schemas.account import AccountCreate, AccountUpdate


class AccountController(CRUDBase[Account, AccountCreate, AccountUpdate]):

    def __init__(self):
        super().__init__(model=Account)

    async def get_account_by_account_number(account_number: str) -> Account | None:
        return await Account.filter(account_number=account_number).first()

    async def get_dict_by_id(self, dict_id: list[str]):
        return await Dict.filter(id__in=dict_id).all()

    @staticmethod
    async def update_dict_by_value(account: Account, dict_value_list: list[str] | str):
        if not dict_value_list:
            return False
        if isinstance(dict_value_list, str):
            dict_value_list = dict_value_list.split(",")

        account_dict_objs = await Dict.filter(id__in=dict_value_list)
        await account.by_account_dict.clear()
        for dict_value in account_dict_objs:
            await account.by_account_dict.add(dict_value)


account_controller = AccountController()
