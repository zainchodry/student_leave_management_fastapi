from app.routes.accounts import router as account_router
from app.routes.leave import router as leave_router
from app.routes.attendance import router as attendance_router
from app.routes.notifications import router as notification_router
from app.routes.departments import router as department_router
from app.routes.dashboard import router as dashboard_router
from fastapi import FastAPI
from app.config import settings
from app.database import *

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(account_router)
app.include_router(leave_router)
app.include_router(attendance_router)
app.include_router(notification_router)
app.include_router(department_router)
app.include_router(dashboard_router)