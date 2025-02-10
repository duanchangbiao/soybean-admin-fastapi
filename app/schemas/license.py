from typing import Annotated, Optional

from pydantic import BaseModel, Field


class LicenseBase(BaseModel):
    id: Annotated[int | None, Field(title="id")] = None
    license_id: Annotated[str | None, Field(alias="licenseId", title="许可证编号")] = None
    company_name: Annotated[str | None, Field(alias="companyName", title="公司名称")] = None
    company_address: Annotated[str | None, Field(alias="companyAddress", title="公司地址")] = None
    issuance_time: Annotated[str | None, Field(alias="issuanceTime", title="许可时间")] = None
    license_type: Annotated[str | None, Field(alias="licenseType", title="TIS编号")] = None
    factory_address: Annotated[str | None, Field(alias="factoryAddress", title="注册登记编号")] = None
    factory_registration_number: Annotated[
        str | None, Field(alias="factoryRegistrationNumber", title="注册登记编号")] = None
    license_category: Annotated[str | None, Field(alias="licenseCategory", title="类别")] = None
    license_company: Annotated[str | None, Field(alias="licenseCompany", title="持牌公司")] = None
    tax_identification_number: Annotated[
        str | None, Field(alias="taxIdentificationNumber", title="纳税人识别号")] = None
    details: Annotated[str | None, Field(alias="details", title="详细地址")] = None

    class Config:
        populate_by_name = True


class LicenseCreate(LicenseBase):
    ...


class LicenseUpdate(LicenseBase):
    ...
