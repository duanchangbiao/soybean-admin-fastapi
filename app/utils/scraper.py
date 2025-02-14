import asyncio
from datetime import datetime

import requests
from fastapi_mail import FastMail, MessageSchema, MessageType

from app.controllers.account import account_controller
from app.controllers.dict import dict_controller
from app.controllers.mor import mor_controller
from app.models.system import Account, Mor, Dict, Aft
from lxml import etree

from app.schemas.account import AccountUpdate
from app.settings.config import fastapi_mail_config


class ScraperUtils:
    def __init__(self):
        self.account = None
        self.session = requests.Session()
        self.url = 'https://sso.tisi.go.th/login'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'https://sso.tisi.go.th/login',
        }

    async def login(self, account: AccountUpdate):
        self.account = account
        response_login = self.session.get(url=self.url, headers=self.headers, verify=False)
        if response_login.status_code != 200:
            self.account.feedback = '用户登陆异常,请手动重试!'
            account_controller.update(id=self.account.id, obj_in=self.account)
            return False, ""
        tree = etree.HTML(response_login.text)
        _token = tree.xpath('//*[@name="_token"]/@value')[0]
        data = {
            'username': self.account.account_number,
            'password': self.account.password,
            'redirect_uri': '',
            '_token': _token
        }
        response = self.session.post(url=self.url, headers=self.headers, data=data, verify=False)
        if response.status_code != 200:
            print(response.text)
            self.account.feedback = '用户登陆异常,请手动重试!'
            account_controller.update(id=self.account.id, obj_in=self.account)
            return False, ""
        return True, response.text

    async def get_license(self, index_text):
        tree = etree.HTML(index_text)
        url = tree.xpath("//div[@class='row colorbox-group-widget']/div[1]/a/@href")
        if len(url) == 0:
            self.account.feedback = '账号密码错误,请修改后重试！'
            account_controller.update(id=self.account.id, obj_in=self.account)
            account_controller.update(id=self.account.id, obj_in=self.account)
            return False, ""
        response_license = self.session.get(url[0], headers=self.headers, verify=False)
        if response_license.status_code != 200:
            self.account.feedback = '账号密码错误,请修改后重试！'
            account_controller.update(id=self.account.id, obj_in=self.account)
            account_controller.update(id=self.account.id, obj_in=self.account)
            return False, ""
        return True, response_license.text

    async def get_mor5(self, mor5_text):
        tree = etree.HTML(mor5_text)
        if len(tree.xpath("//*[@id='top']/div/nav/div[2]/ul/li[7]/ul/li[1]/a/@href")) == 0:
            self.account.feedback = '账号密码错误,请修改后重试！'
            account_controller.update(id=self.account.id, obj_in=self.account)
            account_controller.update(id=self.account.id, obj_in=self.account)
            return False, ""
        url = tree.xpath("//*[@id='top']/div/nav/div[2]/ul/li[7]/ul/li[1]/a/@href")[0]
        response_mor5 = self.session.get("https://i.tisi.go.th" + url, headers=self.headers, verify=False)
        if response_mor5.status_code != 200:
            self.account.feedback = '账号密码错误,请修改后重试！'
            account_controller.update(id=self.account.id, obj_in=self.account)
            account_controller.update(id=self.account.id, obj_in=self.account)
            return False, ""

        with open('mor5.html', 'w', encoding='utf-8') as f:
            f.write(response_mor5.text)
            f.close()
        print('mor5.html download success!')

    async def get_mor9(self, mor5_text):
        tree = etree.HTML(mor5_text)
        if len(tree.xpath("//*[@id='top']/div/nav/div[2]/ul/li[7]/ul/li[1]/a/@href")) == 0:
            self.account.feedback = '账号密码错误,请修改后重试！'
            account_controller.update(id=self.account.id, obj_in=self.account)
            account_controller.update(id=self.account.id, obj_in=self.account)
            return False, ""
        url = tree.xpath("//*[@id='top']/div/nav/div[2]/ul/li[7]/ul/li[8]/a/@href")[0]
        response_mor9 = self.session.get("https://i.tisi.go.th" + url, headers=self.headers, verify=False)
        tree = etree.HTML(response_mor9.text, etree.HTMLParser())
        tr_list = tree.xpath("//*[@id='moao9List']/tbody/tr")
        for tr in tr_list:
            item = {}
            if tr.xpath("./td[2]//text()"):
                item["MOR9_APPLY_CODE"] = tr.xpath("./td[2]//text()")[0].strip()
                if item["MOR9_APPLY_CODE"] == "":
                    item["MOR9_APPLY_CODE"] = tr.xpath("./td[2]//text()")[1].strip()
            if tr.xpath("./td[3]//text()"):
                item["MOR9_APPLY_NAME"] = tr.xpath("./td[3]/text()")[0].strip()
            if tr.xpath("./td[7]//text()"):
                item["MOR9_LICENSE_CODE"] = tr.xpath("./td[7]//text()")[0].strip()
            if tr.xpath("./td[8]//text()"):
                item["MOR9_APPLY_DATE"] = tr.xpath("./td[8]//text()")[0].strip()
            else:
                item["MOR9_APPLY_DATE"] = None
            if tr.xpath("./td[9]/p/span/text()"):
                item["MOR9_STATUS"] = tr.xpath("./td[9]/p/span/text()")[0].strip()
            else:
                item["MOR9_STATUS"] = ""

            dict_obj: Dict = await dict_controller.get_by_dict_value("MOR9_STATUS", item["MOR9_STATUS"])
            if dict_obj:
                status = dict_obj.dict_name
            else:
                status = "其他"
            mor_obj = Mor(
                apply_number=item["MOR9_APPLY_CODE"],
                apply_name=item["MOR9_APPLY_NAME"],
                apply_date=item["MOR9_APPLY_DATE"],
                mor_type="MOR9",
                mor_status=status,
                license_code=item["MOR9_LICENSE_CODE"],
                create_by=self.account.create_by,
                update_by=self.account.update_by,
                ctime=datetime.now(),
                mtime=datetime.now(),
            )
            mor: Mor = await mor_controller.get_apply_number(item["MOR9_APPLY_CODE"])
            if mor:
                await mor_controller.update(id=mor.id, obj_in=mor_obj.to_dict())
                if item["MOR9_STATUS"] != mor.apply_status:
                    await self.sendEmail(user=self.account.nickname, result=mor_obj)
            else:
                await mor_controller.create(mor_obj)
        return True, "Mor9 scraper success"

    @staticmethod
    async def sendEmail(user, result):
        if result.__class__ == Aft:
            title = f'TISI Alert:{result.aft_type}/{user} Adaptor have update!'
            body = (f'----------------------------\n'
                    f'Remark : {result.remark} \n'
                    f'Client :{user}\n '
                    f'{result.aft_type} No : {result.apply_number} \n'
                    f'Current Status : {result.apply_status} \n'
                    f'Current Date : {datetime.now()} \n'
                    f'Quickly Check : https://sso.tisi.go.th/login \n'
                    f'Account Number: {user}, \n')
        elif result.__class__ == Mor:
            title = f'TISI Alert:{result.mor_type}/{user} Mor have update!'
            body = (f'----------------------------\n'
                    f'Remark : {result.remark} \n'
                    f'Client :{user}\n '
                    f'{result.mor_type} No : {result.apply_number} \n'
                    f'----------------------------\n'
                    f'Current Status : {result.apply_status} \n'
                    f'Current Date : {datetime.now()} \n'
                    f'Quickly Check : https://sso.tisi.go.th/login \n'
                    f'Account Number: {user}, \n'
                    )
        else:
            title = f'TISI Alert:NSW/{user} have update!'
            body = (f'----------------------------\n'
                    f'Remark : {result.remark} \n'
                    f'Client :{user}\n '
                    f'NSW No : {result.apply_number} \n'
                    f'----------------------------\n'
                    f'Current Status : {result.apply_status} \n'
                    f'Current Date : {datetime.now()} \n'
                    f'Quickly Check : https://sso.tisi.go.th/login \n'
                    f'Account Number: {user}, \n'
                    )
        fm = FastMail(fastapi_mail_config)
        message = MessageSchema(
            subject=title,
            recipients=["duanchangbiao@zhangkongapp.com"],
            body=body,
            subtype=MessageType.plain
        )
        await fm.send_message(message)


scraper_utils = ScraperUtils()
# if __name__ == '__main__':
#     # scraper = ScraperUtils(username='0105548160264', password='12345')
#     flag, response = asyncio.run(scraper_utils.login(username='0105548160264', password='K@ming0101'))
#     retry, response_l = asyncio.run(scraper_utils.get_license(response))
#     asyncio.run(scraper_utils.get_mor9(response_l, "admin"))
