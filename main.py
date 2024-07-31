from authentication.views import auth
from core.views import core_bp
from leaves.views import leave
from timesheet.views import timesheet
from manageprofile.views import manageprofile
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
app = FastAPI(
    title='hrm_app', openapi_url='/openapi.json', docs_url='/docs',
    description='hrm_app'
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth)
app.include_router(core_bp)
app.include_router(leave)
app.include_router(timesheet)
app.include_router(manageprofile)
