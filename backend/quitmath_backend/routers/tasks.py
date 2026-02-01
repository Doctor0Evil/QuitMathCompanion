from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from ..models import TaskLog
from ..schemas import TaskLogCreate, TaskLogRead
from ..deps import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskLogRead)
async def log_task(
    payload: TaskLogCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    now = datetime.utcnow()
    task = TaskLog(
        user_id=user.id,
        started_at=now,
        completed_at=now,
        task_type=payload.task_type,
        difficulty=payload.difficulty,
        success=payload.success,
        reward_delta=payload.reward_delta,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get("", response_model=list[TaskLogRead])
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    result = await db.execute(
        select(TaskLog).where(TaskLog.user_id == user.id).order_by(TaskLog.started_at.desc())
    )
    return list(result.scalars().all())
