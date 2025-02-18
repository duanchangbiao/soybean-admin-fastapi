from datetime import datetime

from app.api.v1.utils import insert_log
from app.controllers.account import account_controller
from app.models.system import Account, LogDetailType, LogType
from app.schemas.account import AccountUpdate
from app.schemas.base import Success
from app.utils.scraper import scraper_utils


async def get_scheduler_job():
    account_objs: list[Account] = await Account.filter(activate=1)
    for account_obj in account_objs:
        account = await account_obj.to_dict()
        await account_obj.fetch_related("by_account_dict")
        by_account_dict_list = [by_account_dict.dict_name for by_account_dict in account_obj.by_account_dict]
        if not len(by_account_dict_list):
            await account_controller.update(id=account["id"], obj_in={"feedback": "未选择监控项,请添加监控项!"})
        account_in = AccountUpdate(
            id=account["id"],
            nickname=account["nickname"],
            account_number=account["accountNumber"],
            password=account["password"],
            remark=account["remark"],
            ctime=account["ctime"],
            mtime=account["mtime"],
            create_by=account["createBy"],
        )
        print(f"监控信息:{account}")
        retry, response = await scraper_utils.login(account=account_in)
        if not retry:
            return Success(msg="Scraper Failed", data={'Scraper_id': account_obj.id}, code=4090)
        for by_account_dict in by_account_dict_list:
            if by_account_dict != 'NSW':
                retry_l, response_l = await scraper_utils.get_license(index_text=response, type=1)
                if not retry_l:
                    return Success(msg="Scraper Failed", data={'Scraper_id': account_obj.id}, code=4090)
                if by_account_dict == 'MOR9':
                    retry_m, response_m = await scraper_utils.get_mor9(response_l)
                    if not retry_m:
                        return Success(msg="Scraper Failed", data={'Scraper_id': account_obj.id}, code=4090)
                if by_account_dict == 'MOR5':
                    retry_m, response_m = await scraper_utils.get_mor5(response_l)
                    if not retry_m:
                        return Success(msg="Scraper Failed", data={'Scraper_id': account_obj.id}, code=4090)
                if by_account_dict == 'AFFA':
                    retry_a, response_a = await scraper_utils.get_affa(response_l)
                    if not retry_a:
                        return Success(msg="Scraper Failed", data={'Scraper_id': account_obj.id}, code=4090)
                if by_account_dict == 'AFT':
                    retry_a, response_a = await scraper_utils.get_aft(response_l)
                    if not retry_a:
                        return Success(msg="Scraper Failed", data={'Scraper_id': account_obj.id}, code=4090)
            if by_account_dict == 'NSW':
                retry_n, response_n = await scraper_utils.get_license(index_text=response, type=2)
                if not retry_n:
                    return Success(msg="Scraper Failed", data={'Scraper_id': account_obj.id}, code=4090)
                await scraper_utils.get_nsw(response_n)
        await scraper_utils.logout()
        await account_controller.update(id=account_obj.id, obj_in={"mtime": datetime.now()})
        await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.ApiScraper, by_user_id=0)
