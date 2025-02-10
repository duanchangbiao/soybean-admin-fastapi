from app.core.crud import CRUDBase
from app.models.system import LicenseReport
from app.schemas.license import LicenseCreate, LicenseUpdate


class LicenseController(CRUDBase[LicenseReport, LicenseCreate, LicenseUpdate]):

    def __init__(self):
        super().__init__(model=LicenseReport)

    async def get_by_license_key(self, license_id: str) -> LicenseReport | None:
        return await self.model.filter(license_key=license_id).first()


license_controller = LicenseController()
