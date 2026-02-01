from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..database import get_db
from ..models import EcoImpact
from ..schemas import EcoImpactCreate, EcoImpactRead
from ..services.eco_impact import EcoImpactService
from ..deps import get_current_user

router = APIRouter(prefix="/eco", tags=["eco"])


@router.post("/manual", response_model=EcoImpactRead)
async def log_manual_eco(
    payload: EcoImpactCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    eco = EcoImpact(
        user_id=user.id,
        metric=payload.metric,
        unit=payload.unit,
        value=payload.value,
        karma=0.0,
    )
    db.add(eco)
    await db.commit()
    await db.refresh(eco)
    return eco


@router.post("/disposables", response_model=list[EcoImpactRead])
async def log_disposable_avoidance(
    avoided_units: float,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    service = EcoImpactService()
    metrics = service.disposables_to_eco(avoided_units)
    records: list[EcoImpact] = []

    eco_units = EcoImpact(
        user_id=user.id,
        metric="DisposableVapesAvoided",
        unit="units",
        value=avoided_units,
        karma=0.0,
    )
    db.add(eco_units)
    records.append(eco_units)

    eco_mass = EcoImpact(
        user_id=user.id,
        metric="PlasticPlusBatteryMass",
        unit="g",
        value=metrics["plastic_g"] + metrics["battery_g"],
        karma=metrics["karma"],
    )
    db.add(eco_mass)
    records.append(eco_mass)

    eco_co2 = EcoImpact(
        user_id=user.id,
        metric="CO2eAvoided",
        unit="kg",
        value=metrics["co2e_kg"],
        karma=0.0,
    )
    db.add(eco_co2)
    records.append(eco_co2)

    await db.commit()
    for rec in records:
        await db.refresh(rec)
    return records


@router.get("/summary")
async def eco_summary(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    result = await db.execute(
        select(
            EcoImpact.metric,
            func.sum(EcoImpact.value),
            func.sum(EcoImpact.karma),
        ).where(EcoImpact.user_id == user.id).group_by(EcoImpact.metric)
    )
    rows = result.all()
    return [
        {"metric": m, "total_value": float(v or 0.0), "total_karma": float(k or 0.0)}
        for m, v, k in rows
    ]
