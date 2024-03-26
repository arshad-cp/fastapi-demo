from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from database.database import get_db_default
from models import Tenant


class TenantIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return JSONResponse({"error": "X-Tenant-ID header is required"}, status_code=400)

        db: Session = next(get_db_default())
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            return JSONResponse({"details": "Tenant not found"}, status_code=404)

        response = await call_next(request)
        return response
