from __future__ import annotations
from datetime import datetime
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.llm import get_llm
from backend.models import OfflineMessage
from backend.utils.ids import short_id

async def compose(session: AsyncSession, content: str) -> dict:
    user = OfflineMessage(id=short_id(), role="user", content=content.strip(), sync_status="pending")
    session.add(user)
    await session.flush()
    llm = get_llm()
    reply = await llm.complete(content, system="Offline mock assistant — concise helpful replies.")
    assistant = OfflineMessage(id=short_id(), role="assistant", content=reply, sync_status="pending")
    session.add(assistant)
    await session.commit()
    return {"user_id": user.id, "assistant_id": assistant.id, "reply": reply, "sync_status": "pending"}

async def list_messages(session: AsyncSession) -> list[OfflineMessage]:
    return list((await session.execute(select(OfflineMessage).order_by(OfflineMessage.created_at))).scalars())

async def queue_status(session: AsyncSession) -> dict:
    pending = (await session.execute(select(func.count()).select_from(OfflineMessage).where(OfflineMessage.sync_status == "pending"))).scalar() or 0
    synced = (await session.execute(select(func.count()).select_from(OfflineMessage).where(OfflineMessage.sync_status == "synced"))).scalar() or 0
    return {"pending": int(pending), "synced": int(synced)}

async def sync_pending(session: AsyncSession) -> dict:
    rows = list((await session.execute(select(OfflineMessage).where(OfflineMessage.sync_status == "pending"))).scalars())
    now = datetime.utcnow()
    for row in rows:
        row.sync_status = "synced"
        row.synced_at = now
    await session.commit()
    return {"synced": len(rows), "queue": await queue_status(session)}
