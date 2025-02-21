import asyncio

import requests
from lxml import etree


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

    async def post_request(self, data: dict) -> str:
        response = requests.post(self.init_url, headers=self.headers, data=data)
        return response.text


    async def parse_html(self, response: str) -> str:
        tree = etree.parse(response)
        tr_list = tree.xpath('//*[@id="table1"]/tbody/tr')
        license_list = []
        for tr in tr_list:
            license_id = tr.xpath('./td[1]/text()')[0]  # 许可证
            issuance_time = tr.xpath('./td[3]/text()')[0]  # 许可证发布时间
            license_type = tr.xpath('./td[4]/text()')[0]  # 编号
            license_company = tr.xpath('./td[5]/text()')[0]  # 编号
            print(license_id)
            # license: LicenseReport = await license_controller.get(id=license_id)
            # if not license:
            #     print(license_id, issuance_time, license_type, license_company)
        return license_list

    """
      解析详情页数据信息
    """

    async def get_license_detail(self, data: dict) -> dict:
        response = requests.post('https://a.tisi.go.th/l/', headers=self.headers, data=data, timeout=20)
        tree = etree.HTML(response.text, etree.HTMLParser())
        license_category = tree.xpath("//div[@class='panel panel-success']//div[4]/font/text()")
        tax_identification_number = tree.xpath("//div[@class='panel panel-success']//div[6]/font/text()")
        company_address = tree.xpath("//div[@class='panel panel-success']//div[7]/font/text()")
        company_name = tree.xpath("//div[@class='panel panel-success']//div[8]/font/text()")
        factory_registration_number = tree.xpath("//div[@class='panel panel-success']//div[9]/font/text()")
        factory_address = tree.xpath("//div[@class='panel panel-success']//div[10]/font/text()")
        detail = tree.xpath("//div[@class='panel panel-success']//div[13]/font//text()")
        text = []
        if detail is not None:
            for i in detail:
                if i.find("\t") == -1:
                    text.append(i.replace("\r\n", " ").replace("\r", " "))
        licenses_detail = "\n".join(text)
        print(
            f"类别:{license_category},税号:{tax_identification_number},公司名称:{company_name},公司地址:{company_address},注册地址：{factory_registration_number},工厂地址:{factory_address}")
        return None


scraper_report = scraperReport()
