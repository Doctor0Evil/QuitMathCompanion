from fastapi import APIRouter, Depends

from ..schemas import ODESimulateRequest, ODESimulateResponse, ODESimulatePoint
from ..services.ode_engine import CravingODEEngine
from ..services.rl_scheduler import RLScheduler
from ..deps import get_current_user

router = APIRouter(prefix="/rl", tags=["rl"])


@router.post("/simulate", response_model=ODESimulateResponse)
async def simulate_ode(
    payload: ODESimulateRequest,
    user=Depends(get_current_user),
):
    engine = CravingODEEngine()
    t, c, a, r = engine.simulate(
        c0=payload.c0,
        a0=payload.a0,
        r0=payload.r0,
        horizon_minutes=payload.horizon_minutes,
        dt_minutes=payload.dt_minutes,
    )
    points = [
        ODESimulatePoint(t_min=float(ti), c=float(ci), a=float(ai), r=float(ri))
        for ti, ci, ai, ri in zip(t, c, a, r)
    ]
    return ODESimulateResponse(points=points)


@router.get("/suggest-tasks")
async def suggest_tasks(
    c: float,
    a: float,
    r: float,
    user=Depends(get_current_user),
):
    scheduler = RLScheduler()
    offsets = scheduler.suggest_task_schedule(c0=c, a0=a, r0=r)
    return {"minute_offsets": offsets}
