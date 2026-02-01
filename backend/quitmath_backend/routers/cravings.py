from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from ..models import CravingLog
from ..schemas import CravingLogCreate, CravingLogRead
from ..deps import get_current_user

router = APIRouter(prefix="/cravings", tags=["cravings"])


@router.post("", response_model=CravingLogRead)
async def log_craving(
    payload: CravingLogCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    log = CravingLog(
        user_id=user.id,
        timestamp=payload.timestamp,
        score=payload.score,
        attention=payload.attention,
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@router.get("", response_model=list[CravingLogRead])
async def list_cravings(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    result = await db.execute(
        select(CravingLog).where(CravingLog.user_id == user.id).order_by(CravingLog.timestamp.desc())
    )
    return list(result.scalars().all())
