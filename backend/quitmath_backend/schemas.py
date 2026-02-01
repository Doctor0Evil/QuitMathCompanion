from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from .models import TaskType, DailyState


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CravingLogCreate(BaseModel):
    timestamp: Optional[datetime] = None
    score: int = Field(ge=0, le=10)
    attention: Optional[int] = Field(default=None, ge=0, le=10)


class CravingLogRead(BaseModel):
    id: int
    timestamp: datetime
    score: int
    attention: Optional[int]

    class Config:
        from_attributes = True


class TaskLogCreate(BaseModel):
    task_type: TaskType
    difficulty: int = Field(ge=1, le=10)
    success: bool
    reward_delta: float = Field(ge=0.0)


class TaskLogRead(BaseModel):
    id: int
    started_at: datetime
    completed_at: Optional[datetime]
    task_type: TaskType
    difficulty: int
    success: bool
    reward_delta: float

    class Config:
        from_attributes = True


class DailySessionRead(BaseModel):
    date: date
    state: DailyState
    avg_craving: float
    avg_attention: float
    avg_reward: float
    smoked_today: bool
    abstinent_streak: int

    class Config:
        from_attributes = True


class EcoImpactCreate(BaseModel):
    metric: str
    unit: str
    value: float


class EcoImpactRead(BaseModel):
    id: int
    timestamp: datetime
    metric: str
    unit: str
    value: float
    karma: float

    class Config:
        from_attributes = True


class ODESimulateRequest(BaseModel):
    c0: float = Field(ge=0.0, le=1.0)
    a0: float = Field(ge=0.0, le=1.0)
    r0: float = Field(ge=0.0, le=1.0)
    horizon_minutes: int = Field(ge=5, le=1440)
    dt_minutes: float = Field(gt=0.0, le=60.0)


class ODESimulatePoint(BaseModel):
    t_min: float
    c: float
    a: float
    r: float


class ODESimulateResponse(BaseModel):
    points: list[ODESimulatePoint]
