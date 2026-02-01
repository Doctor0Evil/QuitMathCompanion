from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from .ode_engine import CravingODEEngine, ODEParams


@dataclass
class RLSchedulerConfig:
    horizon_minutes: int = 60
    dt_minutes: float = 1.0
    threshold_high: float = 0.6
    threshold_low: float = 0.3
    max_tasks_per_hour: int = 4
    policy: Literal["heuristic"] = "heuristic"


class RLScheduler:
    """
    Placeholder RL scheduler with a robust deterministic heuristic policy
    that is compatible with future RL training.
    """

    def __init__(
        self,
        ode_params: ODEParams | None = None,
        config: RLSchedulerConfig | None = None,
    ) -> None:
        self.engine = CravingODEEngine(ode_params)
        self.config = config or RLSchedulerConfig()

    def suggest_task_schedule(
        self,
        c0: float,
        a0: float,
        r0: float,
    ) -> list[int]:
        """
        Returns integer minute offsets within the horizon at which to propose tasks.
        Simple deterministic heuristic: schedule tasks shortly before predicted
        high craving periods, limited by max_tasks_per_hour.
        """
        t, c, _, _ = self.engine.simulate(
            c0=c0,
            a0=a0,
            r0=r0,
            horizon_minutes=self.config.horizon_minutes,
            dt_minutes=self.config.dt_minutes,
        )
        task_indices: list[int] = []
        last_task_idx = -9999
        step_minutes = self.config.dt_minutes
        min_gap_steps = max(1, int(60.0 / (self.config.max_tasks_per_hour * step_minutes)))

        for idx in range(1, len(t) - 1):
            if c[idx] >= self.config.threshold_high and c[idx] > c[idx - 1]:
                if idx - last_task_idx >= min_gap_steps:
                    task_indices.append(idx)
                    last_task_idx = idx

        return [int(t[i]) for i in task_indices[: self.config.max_tasks_per_hour]]
