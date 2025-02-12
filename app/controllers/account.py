from app.core.crud import CRUDBase
from app.models.system import Account, Dict
from app.schemas.account import AccountCreate, AccountUpdate


class AccountController(CRUDBase[Account, AccountCreate, AccountUpdate]):

    def __init__(self):
        super().__init__(model=Account)

    @staticmethod
    async def update_account_dict_by_value(account: Account, dict_value_list: list[str] | str):
        if not dict_value_list:
            return False
        if isinstance(dict_value_list, str):
            dict_value_list = dict_value_list.split(",")

        account_dict_objs = await Dict.filter(dict_value__in=dict_value_list)
        await account.by_account_dict.clear()
        for dict_value in account_dict_objs:
            await account.by_account_dict.add(dict_value)


account_controller = AccountController()
