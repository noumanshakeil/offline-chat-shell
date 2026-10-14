from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import offline as svc

class MessageIn(BaseModel):
    content: str = Field(min_length=1)

router = APIRouter()

@router.get("/messages")
async def messages(db: AsyncSession = Depends(get_db)):
    rows = await svc.list_messages(db)
    return {"messages": [{"id": m.id, "role": m.role, "content": m.content[:300], "sync_status": m.sync_status} for m in rows]}

@router.post("/messages")
async def post_message(payload: MessageIn, db: AsyncSession = Depends(get_db)):
    return await svc.compose(db, payload.content)

@router.get("/queue")
async def queue(db: AsyncSession = Depends(get_db)):
    return await svc.queue_status(db)

@router.post("/sync")
async def sync(db: AsyncSession = Depends(get_db)):
    return await svc.sync_pending(db)
