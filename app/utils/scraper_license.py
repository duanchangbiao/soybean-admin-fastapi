import traceback

import requests
from lxml import etree

from app.controllers import license_controller
from app.core.exceptions import HTTPException, HttpExcHandle
from app.models.system import LicenseReport
from app.schemas.license import LicenseCreate


def init_header() -> dict:
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://appdb.tisi.go.th',
        'Referer': 'https://appdb.tisi.go.th/tis_dev/p4_license_report/p4license_report.php',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    }


class scraperReport:

    def __init__(self):
        self.init_url = "https://appdb.tisi.go.th/tis_dev/p4_license_report/p4license_report.php"
        self.headers = init_header()
        self.session = requests.Session()

    async def post_request(self, data: dict) -> str:
        response = self.session.post(self.init_url, headers=self.headers, data=data)
        return response.text

    async def parse_html(self, response: str) -> str:
        tree = etree.HTML(response)
        tr_list = tree.xpath('//*[@id="table1"]/tbody/tr')
        index = 1
        try:
            for tr in tr_list:
                license_id = tr.xpath('./td[1]/text()')[0]  # 许可证
                issuance_time = tr.xpath('./td[3]/text()')[0]  # 许可证发布时间
                license_type = tr.xpath('./td[4]/text()')[0]  # 编号
                license_company = tr.xpath('./td[5]/text()')[0]  # 编号
                license = await LicenseReport.get_or_none(license_id=license_id)
                if not license:
                    report = LicenseCreate(license_id=license_id, issuance_time=issuance_time,
                                           license_type=license_type,
                                           license_company=license_company)
                    await self.get_license_detail(report)
        except Exception as e:
            traceback.print_exc()
            print(e)

    """
      解析详情页数据信息
    """

    async def get_license_detail(self, report: LicenseCreate):
        try:
            data = {
                'n': report.license_id
            }
            response = self.session.post('https://a.tisi.go.th/l/', headers=self.headers, data=data, timeout=20)
            tree = etree.HTML(response.text, etree.HTMLParser())
            if len(tree.xpath("//div[@class='panel panel-success']//div[4]/font/text()")) != 0:
                license_category = tree.xpath("//div[@class='panel panel-success']//div[4]/font/text()")[0]
                report.license_category = license_category
            if len(tree.xpath("//div[@class='panel panel-success']//div[6]/font/text()")) != 0:
                tax_identification_number = tree.xpath("//div[@class='panel panel-success']//div[6]/font/text()")[0]
                report.tax_identification_number = tax_identification_number
            if len(tree.xpath("//div[@class='panel panel-success']//div[7]/font/text()")) != 0:
                company_address = tree.xpath("//div[@class='panel panel-success']//div[7]/font/text()")[0]
                report.company_address = company_address
            if len(tree.xpath("//div[@class='panel panel-success']//div[8]/font/text()")) != 0:
                company_name = tree.xpath("//div[@class='panel panel-success']//div[8]/font/text()")[0]
                report.company_name = company_name
            if len(tree.xpath("//div[@class='panel panel-success']//div[9]/font/text()")) != 0:
                factory_registration_number = tree.xpath("//div[@class='panel panel-success']//div[9]/font/text()")[0]
                report.factory_registration_number = factory_registration_number
            if len(tree.xpath("//div[@class='panel panel-success']//div[10]/font/text()")) != 0:
                factory_address = tree.xpath("//div[@class='panel panel-success']//div[10]/font/text()")[0]
                report.factory_address = factory_address
            detail = tree.xpath("//div[@class='panel panel-success']//div[13]/font//text()")
            text = []
            if detail is not None:
                for i in detail:
                    if i.find("\t") == -1:
                        text.append(i.replace("\r\n", " ").replace("\r", " "))
            licenses_detail = "\n".join(text)
            report.details = licenses_detail
            print(report)
            await license_controller.create(obj_in=report)
        except Exception as e:
            print("数据同步失败,网络异常,请稍后重试!")


scraper_report = scraperReport()
