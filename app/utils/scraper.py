import asyncio
import logging
from datetime import datetime

import requests
from fastapi_mail import FastMail, MessageSchema, MessageType

from app.api.v1.utils import insert_log
from app.controllers.account import account_controller
from app.controllers.aft import aft_controller
from app.controllers.dict import dict_controller
from app.controllers.mor import mor_controller
from app.controllers.nsw import nsw_controller
from app.models.system import Mor, Dict, Aft, LogType, LogDetailType, Nsw
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
            'Referer': 'https://sso.tisi.go.th/login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',

        }

    async def login(self, account: AccountUpdate):
        print('login scraper start!')
        self.account = account
        try:
            requests.packages.urllib3.disable_warnings()
            response_login = self.session.get(url=self.url, headers=self.headers, verify=False, timeout=30)
            if response_login.status_code != 200:
                self.account.feedback = '用户登陆异常,请手动重试!'
                await account_controller.update(id=self.account.id, obj_in=self.account)
                return False, self.account.feedback
            tree = etree.HTML(response_login.text)
            if not tree.xpath('//*[@name="_token"]/@value'):
                print("解析login index error!")
                self.account.feedback = '网络异常,请重启网络！'
                await account_controller.update(id=self.account.id, obj_in=self.account)
                await self.logout()
                return False, self.account.feedback
            _token = tree.xpath('//*[@name="_token"]/@value')[0]
            data = {
                'username': self.account.account_number,
                'password': self.account.password,
                'redirect_uri': '',
                '_token': _token
            }
            requests.packages.urllib3.disable_warnings()
            response = self.session.post(url=self.url, headers=self.headers, data=data, verify=False, timeout=30)
            if response.status_code != 200:
                self.account.feedback = '用户登陆异常,请手动重试!'
                await account_controller.update(id=self.account.id, obj_in=self.account, exclude={"by_account_modules"})
                return False, self.account.feedback
        except Exception as e:
            self.account.feedback = '网络异常,请重启网络！'
            await account_controller.update(id=self.account.id, obj_in=self.account)
            await self.logout()
            return False, self.account.feedback
        return True, response.text

    async def get_license(self, index_text, type: int):
        print('index.html scraper start!')
        tree = etree.HTML(index_text)
        try:
            if type == 1:
                url = tree.xpath("//div[@class='row colorbox-group-widget']/div[1]/a/@href")
            else:
                url = tree.xpath("//div[@class='row colorbox-group-widget']/div[2]/a/@href")
            requests.packages.urllib3.disable_warnings()
            response_license = self.session.get(url[0], headers=self.headers, verify=False)
            if response_license.status_code != 200:
                self.account.feedback = '账号密码可能错误,请重试!'
        except Exception as e:
            await self.logout()
            return False, "有账号正在登陆,请退出登陆重试"
        return True, response_license.text

    async def get_mor5(self, mor5_text):
        print('mor5.html scraper start!')
        tree = etree.HTML(mor5_text)
        try:
            if len(tree.xpath("//*[@id='top']/div/nav/div[2]/ul/li[7]/ul/li[3]/a/@href")) == 0:
                self.account.feedback = '账号密码错误,请修改后重试！'
                return False, self.account.feedback
            url = tree.xpath("//*[@id='top']/div/nav/div[2]/ul/li[7]/ul/li[3]/a/@href")[0]
            requests.packages.urllib3.disable_warnings()
            response_mor5 = self.session.get("https://i.tisi.go.th" + url, headers=self.headers, verify=False)
            if response_mor5.status_code != 200:
                self.account.feedback = '账号密码错误,请修改后重试！'
                return False, '账号密码错误,请修改后重试！'
            # 解析页面mor5
            tree = etree.HTML(response_mor5.text, etree.HTMLParser())
            tr_list = tree.xpath("//*[@id='moao5List']/tbody/tr")
            for tr in tr_list:
                item = {}
                if tr.xpath("./td[2]/text()"):
                    if tr.xpath("./td[2]/text()")[0].strip() == "":
                        item["MOR5_APPLY_CODE"] = tr.xpath("./td[2]/text()")[1].strip()
                    else:
                        item["MOR5_APPLY_CODE"] = tr.xpath("./td[2]/text()")[0].strip()
                if tr.xpath("./td[3]/text()"):
                    item["MOR5_APPLY_NAME"] = tr.xpath("./td[3]/text()")[0].strip()
                if tr.xpath("./td[7]//text()"):
                    item["MOR5_APPLY_DATE"] = "".join(tr.xpath("./td[7]//text()")).strip()
                else:
                    item["MOR5_APPLY_DATE"] = ""
                if tr.xpath("./td[8]//span[@class='show_status']"):
                    str_list = "".join(tr.xpath("./td[8]//span[@class='show_status']//text()"))
                    item["MOR5_STATUS"] = str_list.strip()
                else:
                    item["MOR5_STATUS"] = ""
                # 获取状态
                dict_obj: Dict = await dict_controller.get_by_dict_value(dict_value=item["MOR5_STATUS"],
                                                                         dict_type="mor5_status")
                if dict_obj:
                    status = dict_obj.dict_name
                else:
                    status = "异常"
                mor: Mor = await mor_controller.get_mor_by_apply_number(apply_number=item["MOR5_APPLY_CODE"])
                if mor:
                    new_mor: Mor = await mor_controller.update(id=mor.id, obj_in={
                        "apply_number": item["MOR5_APPLY_CODE"],
                        "apply_date": item["MOR5_APPLY_DATE"],
                        "apply_name": item["MOR5_APPLY_NAME"],
                        "mor_type": "mor5",
                        "apply_status": status,
                        "update_by": self.account.update_by,
                        "update_status": 2,
                        "mtime": datetime.now(),
                        "ctime": datetime.now(),
                    })
                    if status != mor.apply_status:
                        await mor_controller.update(id=mor.id, obj_in={
                            "update_status": 1,
                        })
                        mor.apply_status = status
                        await self.sendEmail(user=self.account.nickname, result=mor)
                    await mor_controller.update_mor_account(mor=new_mor, mor_account_id=self.account.account_number)
                else:
                    new_mor = await mor_controller.create(obj_in={
                        "apply_number": item["MOR5_APPLY_CODE"],
                        "apply_date": item["MOR5_APPLY_DATE"],
                        "apply_name": item["MOR5_APPLY_NAME"],
                        "mor_type": "mor5",
                        "apply_status": status,
                        "create_by": self.account.update_by,
                        "update_status": 2,
                        "mtime": datetime.now(),
                        "ctime": datetime.now(),
                    })
                    await mor_controller.update_mor_account(mor=new_mor, mor_account_id=self.account.account_number)
        except Exception as e:
            self.account.feedback = "MOR5数据采集发生错误,请手动重试!"
            return False, self.account.feedback
        return True, "Mor5 scraper success"

    async def get_mor9(self, mor9_text):
        print('mor9.html scraper start!')
        tree = etree.HTML(mor9_text)
        if len(tree.xpath("//*[@id='top']/div/nav/div[2]/ul/li[7]/ul/li[1]/a/@href")) == 0:
            self.account.feedback = '账号密码错误,请修改后重试！'
            return False, ""
        try:
            url = tree.xpath("//*[@id='top']/div/nav/div[2]/ul/li[7]/ul/li[8]/a/@href")[0]
            requests.packages.urllib3.disable_warnings()
            response_mor9 = self.session.get("https://i.tisi.go.th" + url, headers=self.headers, verify=False,
                                             timeout=6)
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

                dict_obj: Dict = await dict_controller.get_by_dict_value(dict_value=item["MOR9_STATUS"],
                                                                         dict_type="mor9_status")
                if dict_obj:
                    status = dict_obj.dict_name
                else:
                    status = "异常"
                mor: Mor = await mor_controller.get_mor_by_apply_number(apply_number=item["MOR9_APPLY_CODE"])
                if mor:
                    await mor_controller.update(id=mor.id, obj_in={
                        "apply_number": item["MOR9_APPLY_CODE"],
                        "apply_date": item["MOR9_APPLY_DATE"],
                        "apply_name": item["MOR9_APPLY_NAME"],
                        "license_code": item["MOR9_LICENSE_CODE"],
                        "mor_type": "mor9",
                        "apply_status": status,
                        "update_status": 2,
                        "update_by": self.account.create_by,
                        "mtime": datetime.now(),
                        "ctime": datetime.now(),
                    })
                    if status != mor.apply_status:
                        await mor_controller.update(id=mor.id, obj_in={
                            "update_status": 1,
                        })
                        mor.apply_status = status
                        await self.sendEmail(user=self.account.nickname, result=mor)
                else:
                    new_mor = await mor_controller.create(obj_in={
                        "apply_number": item["MOR9_APPLY_CODE"],
                        "apply_date": item["MOR9_APPLY_DATE"],
                        "apply_name": item["MOR9_APPLY_NAME"],
                        "license_code": item["MOR9_LICENSE_CODE"],
                        "mor_type": "mor9",
                        "apply_status": status,
                        "create_by": self.account.create_by,
                        "update_status": 2,
                        "mtime": datetime.now(),
                        "ctime": datetime.now(),
                    })
                    await mor_controller.update_mor_account(mor=new_mor, mor_account_id=self.account.account_number)
        except Exception as e:
            self.account.feedback = 'MOR9采集失败,请手动重试'
            return False, self.account.feedback
        return True, "Mor9 scraper success"

    async def get_affa(self, affa_text):
        print('affa.html scraper start!')
        tree = etree.HTML(affa_text)
        if len(tree.xpath("//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[6]/ul/li[2]/a/@href")) == 0:
            self.account.feedback = '账号密码错误,请修改后重试！'
            await account_controller.update(id=self.account.id, obj_in=self.account)
            return False, ""
        url = tree.xpath("//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[6]/ul/li[2]/a/@href")[0]
        try:
            requests.packages.urllib3.disable_warnings()
            response_afft = self.session.get("https://i.tisi.go.th" + url, headers=self.headers, verify=False,
                                             timeout=6)
            tree = etree.HTML(response_afft.text, etree.HTMLParser())
            tr_list = tree.xpath("//*[@id='factoryList']/tbody/tr")
            for tr in tr_list:
                item = {}
                if tr.xpath("./td[2]//text()"):
                    item["AFFA_APPLY_CODE"] = tr.xpath("./td[2]//text()")[0].strip()
                    if item["AFFA_APPLY_CODE"] == "":
                        item["AFFA_APPLY_CODE"] = tr.xpath("./td[2]//text()")[1].strip()
                else:
                    item["AFFA_APPLY_CODE"] = ""
                if tr.xpath("./td[5]//text()"):
                    item["AFFA_APPLY_LICENSE"] = tr.xpath("./td[5]//text()")[0].strip()
                else:
                    item["AFFA_APPLY_LICENSE"] = ""
                if tr.xpath("./td[6]/text()"):
                    item["AFFA_APPLY_DATE"] = "".join(tr.xpath("./td[6]//text()")).strip()
                else:
                    item["AFFA_APPLY_DATE"] = ""
                if tr.xpath("./td[7]/text()"):
                    str_list = "".join(tr.xpath("./td[7]//text()"))
                    item["AFFA_STATUS"] = str_list.strip()
                else:
                    item["AFFA_STATUS"] = ""

                dict_obj: Dict = await dict_controller.get_by_dict_value(dict_value=item["AFFA_STATUS"],
                                                                         dict_type="affa_status")
                if dict_obj:
                    status = dict_obj.dict_name
                else:
                    status = "异常"
                affa: Aft = await aft_controller.get_aft_by_apply_number(apply_number=item["AFFA_APPLY_CODE"])
                if affa:
                    await aft_controller.update(id=affa.id, obj_in={
                        "apply_number": item["AFFA_APPLY_CODE"],
                        "apply_date": item["AFFA_APPLY_DATE"],
                        "apply_license": item["AFFA_APPLY_LICENSE"],
                        "aft_type": "affa",
                        "apply_status": status,
                        "update_status": 2,
                        "update_by": self.account.create_by,
                        "mtime": datetime.now(),
                    })
                    if status != affa.apply_status:
                        await aft_controller.update(id=affa.id, obj_in={
                            "update_status": 1,
                        })
                        affa.apply_status = status
                        await self.sendEmail(user=self.account.nickname, result=affa)
                else:
                    new_affa = await aft_controller.create(obj_in={
                        "apply_number": item["AFFA_APPLY_CODE"],
                        "apply_date": item["AFFA_APPLY_DATE"],
                        "apply_license": item["AFFA_APPLY_LICENSE"],
                        "aft_type": "affa",
                        "apply_status": status,
                        "create_by": self.account.create_by,
                        "update_status": 2,
                        "ctime": datetime.now(),
                    })
                    await aft_controller.update_aft_account(aft=new_affa, aft_account_id=self.account.account_number)
        except Exception as e:
            self.account.feedback = 'AFFA数据采集错误!请手动重试!'
            return False, self.account.feedback
        return True, "Affa scraper success"

    async def get_aft(self, aft_text):
        print('aft.html scraper start!')
        tree = etree.HTML(aft_text)
        if len(tree.xpath("//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[6]/ul/li[3]/a/@href")) == 0:
            self.account.feedback = '账号密码错误,请修改后重试！'
            await account_controller.update(id=self.account.id, obj_in=self.account)
            return False, ""
        url = tree.xpath("//*[@id='top']/div//ul[@class='nav menu nav-pills']/li[6]/ul/li[3]/a/@href")[0]
        try:
            requests.packages.urllib3.disable_warnings()
            response_aft = self.session.get("https://i.tisi.go.th" + url, headers=self.headers, verify=False, timeout=6)
            tree = etree.HTML(response_aft.text, etree.HTMLParser())
            tr_list = tree.xpath("//*[@id='productList']/tbody/tr")
            for tr in tr_list:
                item = {}
                if tr.xpath("./td[2]//text()"):
                    item["AFT_APPLY_CODE"] = tr.xpath("./td[2]//text()")[0].strip()
                    if item["AFT_APPLY_CODE"] == "":
                        item["AFT_APPLY_CODE"] = tr.xpath("./td[2]//text()")[1].strip()
                else:
                    item["AFT_APPLY_CODE"] = ""
                if tr.xpath("./td[5]//text()"):
                    item["AFT_APPLY_LICENSE"] = tr.xpath("./td[5]//text()")[0].strip()
                else:
                    item["AFT_APPLY_LICENSE"] = ""
                if tr.xpath("./td[6]/text()"):
                    item["AFT_APPLY_DATE"] = "".join(tr.xpath("./td[6]//text()")).strip()
                else:
                    item["AFT_APPLY_DATE"] = ""
                if tr.xpath("./td[7]/text()"):
                    str_list = "".join(tr.xpath("./td[7]//text()"))
                    item["AFT_STATUS"] = str_list.strip()
                else:
                    item["AFT_STATUS"] = ""

                dict_obj: Dict = await dict_controller.get_by_dict_value(dict_value=item["AFT_STATUS"],
                                                                         dict_type="aft_status")
                if dict_obj:
                    status = dict_obj.dict_name
                else:
                    status = "异常"
                aft: Aft = await aft_controller.get_aft_by_apply_number(apply_number=item["AFT_APPLY_CODE"])
                if aft:
                    await aft_controller.update(id=aft.id, obj_in={
                        "apply_number": item["AFT_APPLY_CODE"],
                        "apply_date": item["AFT_APPLY_DATE"],
                        "apply_license": item["AFT_APPLY_LICENSE"],
                        "aft_type": "aft",
                        "apply_status": status,
                        "update_status": 2,
                        "update_by": self.account.create_by,
                        "mtime": datetime.now(),
                    })
                    if status != aft.apply_status:
                        await aft_controller.update(id=aft.id, obj_in={
                            "update_status": 1,
                        })
                        aft.apply_status = status
                        await self.sendEmail(user=self.account.nickname, result=aft)
                else:
                    new_aft = await aft_controller.create(obj_in={
                        "apply_number": item["AFT_APPLY_CODE"],
                        "apply_date": item["AFT_APPLY_DATE"],
                        "apply_license": item["AFT_APPLY_LICENSE"],
                        "aft_type": "aft",
                        "apply_status": status,
                        "create_by": self.account.create_by,
                        "update_status": 2,
                        "ctime": datetime.now(),
                    })
                    await aft_controller.update_aft_account(aft=new_aft, aft_account_id=self.account.account_number)
        except Exception as e:
            self.account.feedback = 'AFT数据采集异常,请手动重试!'
            return False, self.account.feedback
        return True, "Aft scraper success"

    async def get_nsw(self, aft_text):
        print('Nsw.html scraper start!')
        tree = etree.HTML(aft_text)
        try:
            if len(tree.xpath("//body/div[@class='container-fluid']/div[@class='col-md-6']/div/a/@href")) == 0:
                self.account.feedback = '账号密码错误,请修改后重试！'
                return False, "账号密码错误,请修改后重试"
            url = tree.xpath("//body/div[@class='container-fluid']/div[@class='col-md-6']/div/a/@href")[0]
            requests.packages.urllib3.disable_warnings()
            response_aft = self.session.get("https://appdb.tisi.go.th/TISINSW/" + url, headers=self.headers,
                                            verify=False,
                                            timeout=30)
            tree = etree.HTML(response_aft.text, etree.HTMLParser())
            tr_list = tree.xpath("//*[@id='table6']/tbody/tr")
            for tr in tr_list:
                item = {}
                if tr.xpath("./td[1]/font/text()"):
                    item["NSW_CODE"] = tr.xpath("./td[1]/font/text()")[0].strip()
                if tr.xpath("./td[6]/font/text()"):
                    item["NSW_APPLY_DATE"] = tr.xpath("./td[6]/font/text()")[0].strip()
                else:
                    item["NSW_APPLY_DATE"] = ""
                if tr.xpath("./td[9]/font/text()"):
                    item["NSW_APPLY_STATUS"] = tr.xpath("./td[9]/font/text()")[0].strip()
                else:
                    item["NSW_APPLY_STATUS"] = ""
                nsw: Nsw = await nsw_controller.get_nsw_by_apply_number(apply_number=item["NSW_CODE"])
                if nsw:
                    await nsw_controller.update(id=nsw.id, obj_in={
                        "apply_number": item["NSW_CODE"],
                        "apply_date": item["NSW_APPLY_DATE"],
                        "apply_status": item["NSW_APPLY_STATUS"],
                        "update_status": 2,
                        "update_by": self.account.create_by,
                        "mtime": datetime.now(),
                    })
                    if item["NSW_APPLY_STATUS"] != nsw.apply_status:
                        await nsw_controller.update(id=nsw.id, obj_in={
                            "update_status": 1,
                        })
                        nsw.apply_status = item["NSW_APPLY_STATUS"]
                        await self.sendEmail(user=self.account.nickname, result=nsw)
                else:
                    new_nsw = await nsw_controller.create(obj_in={
                        "apply_number": item["NSW_CODE"],
                        "apply_date": item["NSW_APPLY_DATE"],
                        "apply_status": item["NSW_APPLY_STATUS"],
                        "update_status": 2,
                        "update_by": self.account.create_by,
                        "ctime": datetime.now(),
                    })
                    await nsw_controller.update_nsw_account(nsw=new_nsw, nsw_account_id=self.account.account_number)
        except Exception as e:
            await self.logout()
            return False, "NSW模块采集发生错误,请手动重试"

    async def logout(self):
        requests.packages.urllib3.disable_warnings()
        self.session.get(url="https://sso.tisi.go.th/logout", headers=self.headers, verify=False, timeout=6)
        print('logout success!')

    @staticmethod
    async def sendEmail(user, result):
        try:
            if not result.remark:
                return
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
                recipients=["duanchangbiao@zhangkongapp.com", " tisi_alert@agileservices.co"],
                body=body,
                subtype=MessageType.plain
            )
            await fm.send_message(message)
        except Exception as e:
            ...


scraper_utils = ScraperUtils()
