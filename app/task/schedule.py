from datetime import datetime

from app.api.v1.utils import insert_log
from app.controllers.account import account_controller
from app.core.exceptions import HTTPException
from app.models.system import Account, LogDetailType, LogType
from app.schemas.account import AccountUpdate
from app.schemas.base import Success
from app.utils.scraper import scraper_utils


async def get_scheduler_job_bak():
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
        try:
            print(f"监控信息:{account}")
            retry, response = await scraper_utils.login(account=account_in)
            if not retry:
                return Success(msg="Scraper Failed", data={'Scraper_id': account_obj.id}, code=4090)
            for by_account_dict in by_account_dict_list:
                if by_account_dict != 'NSW':
                    retry_l, response_l = await scraper_utils.get_license(index_text=response, type=1)
                    if not retry_l:
                        Success(msg="Scraper Failed", data={'Scraper_id': account_obj.id}, code=4090)
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
        except Exception as e:
            ...
        await scraper_utils.logout()
        await account_controller.update(id=account_obj.id, obj_in={"mtime": datetime.now()})
        await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.ApiScraper, by_user_id=0)


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
        try:
            retry, response = await scraper_utils.login(account=account_in)
            if not retry:
                await account_controller.update(id=account["id"],
                                                obj_in={"feedback": "用户登陆失败!请重新登陆", "mtime": datetime.now()})
                continue
            print(f"当前信息:{account},采集模块:{by_account_dict_list}")
            for account_dict in by_account_dict_list:
                if account_dict == 'NSW':
                    retry_n, response_n = await scraper_utils.get_license(index_text=response, type=2)
                    if not retry_n:
                        await account_controller.update(id=account["id"],
                                                        obj_in={"feedback": response_n, "mtime": datetime.now()})
                    await scraper_utils.get_nsw(response_n)
                else:
                    retry_l, response_l = await scraper_utils.get_license(index_text=response, type=1)
                    if not retry_l:
                        await account_controller.update(id=account["id"],
                                                        obj_in={"feedback": response_l, "mtime": datetime.now()})
                    if account_dict == 'MOR5':
                        retry_m, response_m = await scraper_utils.get_mor5(response_l)
                        if not retry_m:
                            await account_controller.update(id=account["id"],
                                                            obj_in={"feedback": response_m, "mtime": datetime.now()})

                    elif account_dict == 'MOR9':
                        retry_m, response_m = await scraper_utils.get_mor9(response_l)
                        if not retry_m:
                            await account_controller.update(id=account["id"],
                                                            obj_in={"feedback": response_m, "mtime": datetime.now()})
                    elif account_dict == 'AFT':
                        retry_a, response_a = await scraper_utils.get_aft(response_l)
                        if not retry_a:
                            await account_controller.update(id=account["id"],
                                                            obj_in={"feedback": response_a, "mtime": datetime.now()})
                    else:
                        retry_a, response_a = await scraper_utils.get_affa(response_l)
                        if not retry_a:
                            await account_controller.update(id=account["id"],
                                                            obj_in={"feedback": response_a, "mtime": datetime.now()})
            account_in.mtime = datetime.now()
            account_in.feedback = '账号正常'
            await account_controller.update(id=account_in.id, obj_in=account_in, exclude={"by_account_modules"})
            await scraper_utils.logout()
        except Exception as e:
            await account_controller.update(id=account["id"], obj_in={"feedback": "数据采集发送错误,请手动重试!",
                                                                      "mtime": datetime.now()})
        await scraper_utils.logout()
