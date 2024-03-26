from fastapi import APIRouter, Depends
from modules.tenant.service import TenantService

router = APIRouter()


# API endpoint to receive file path and start the conversion
@router.get("/")
def get_all_tenants(tenant_service: TenantService = Depends(TenantService)):
    # models.create_table()
    tenants = tenant_service.get_all()
    print(tenants)

    return {"data": tenants}
