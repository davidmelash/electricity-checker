from fastapi import APIRouter, FastAPI, Request

from app.api.v1.api import api_router

root_router = APIRouter()
app = FastAPI(title="Recipe API", openapi_url=f"/api/v1/openapi.json")


@root_router.get("/", status_code=200)
async def root(
    request: Request
) -> dict:
    return {"result": "Hello!"}

app.include_router(api_router, prefix="/api/v1")
app.include_router(root_router)