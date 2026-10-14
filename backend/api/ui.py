from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import offline as svc

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Offline Chat Shell", "messages": await svc.list_messages(db), "queue": await svc.queue_status(db)})

@router.post("/ui/message")
async def ui_message(content: str = Form(...), db: AsyncSession = Depends(get_db)):
    await svc.compose(db, content)
    return RedirectResponse("/", status_code=303)

@router.post("/ui/sync")
async def ui_sync(db: AsyncSession = Depends(get_db)):
    await svc.sync_pending(db)
    return RedirectResponse("/", status_code=303)
