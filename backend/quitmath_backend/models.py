import enum
from datetime import datetime, date
from typing import Optional

from sqlalchemy import (
    Column,
    DateTime,
    Date,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    cravings: Mapped[list["CravingLog"]] = relationship("CravingLog", back_populates="user")
    tasks: Mapped[list["TaskLog"]] = relationship("TaskLog", back_populates="user")
    eco_impacts: Mapped[list["EcoImpact"]] = relationship("EcoImpact", back_populates="user")


class CravingLog(Base):
    __tablename__ = "craving_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    score: Mapped[int] = mapped_column(Integer)  # 0–10
    attention: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    user: Mapped[User] = relationship("User", back_populates="cravings")


class TaskType(str, enum.Enum):
    MATH = "MATH"
    NBACK = "NBACK"
    MOTOR = "MOTOR"
    BREATH = "BREATH"


class TaskLog(Base):
    __tablename__ = "task_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    task_type: Mapped[TaskType] = mapped_column(Enum(TaskType))
    difficulty: Mapped[int] = mapped_column(Integer)  # 1–10
    success: Mapped[bool] = mapped_column(Boolean, default=False)
    reward_delta: Mapped[float] = mapped_column(Float, default=0.0)

    user: Mapped[User] = relationship("User", back_populates="tasks")


class DailyState(str, enum.Enum):
    S0_SMOKING = "S0"
    S1_WITHDRAWAL = "S1"
    S2_STABLE = "S2"


class DailySession(Base):
    __tablename__ = "daily_sessions"
    __table_args__ = (
        UniqueConstraint("user_id", "date", name="uq_user_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    state: Mapped[DailyState] = mapped_column(Enum(DailyState))
    avg_craving: Mapped[float] = mapped_column(Float)
    avg_attention: Mapped[float] = mapped_column(Float)
    avg_reward: Mapped[float] = mapped_column(Float)
    smoked_today: Mapped[bool] = mapped_column(Boolean, default=False)
    abstinent_streak: Mapped[int] = mapped_column(Integer, default=0)


class EcoImpact(Base):
    __tablename__ = "eco_impacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    metric: Mapped[str] = mapped_column(String(128))  # e.g., "DisposableVapesAvoided"
    unit: Mapped[str] = mapped_column(String(32))     # e.g., "units", "g", "kg"
    value: Mapped[float] = mapped_column(Float)
    karma: Mapped[float] = mapped_column(Float, default=0.0)

    user: Mapped[User] = relationship("User", back_populates="eco_impacts")
