from fastapi import FastAPI

from routes.auth import router as auth_router
from routes.scans import router as scans_router
from routes.assets import router as assets_router
from routes.findings import router as findings_router
app = FastAPI()

app.include_router(auth_router)
app.include_router(scans_router)
app.include_router(assets_router)
app.include_router(findings_router)