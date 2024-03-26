from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.responses import JSONResponse
from fastapi import FastAPI, Request, status

from middlewares.TenantIdMiddleware import TenantIdMiddleware
from modules.tenant import main as tenant_router
from modules.export import main as export_router

app = FastAPI()

app.add_middleware(TenantIdMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        # Extract field name and error message from validation error
        if len(error["loc"]) > 1:
            field_name = error["loc"][1]
        else:
            field_name = error["loc"][0]

        error_msg = error["msg"]
        # Append error message to the list of errors
        errors.append({field_name: error_msg})
    # Construct a custom response with validation errors
    return JSONResponse(status_code=422, content={"errors": errors, "message": "Validation error", "status_code": 422})


app.include_router(tenant_router.router, prefix="/tenant")
app.include_router(export_router.router, prefix="/export")
