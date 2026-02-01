from dataclasses import dataclass
from typing import Iterable

import numpy as np

from ..config import get_settings

settings = get_settings()


@dataclass
class ODEParams:
    alpha_c: float = settings.alpha_c
    beta_c: float = settings.beta_c
    gamma_c: float = settings.gamma_c
    delta_c: float = settings.delta_c
    lambda_a: float = settings.lambda_a
    eta_a: float = settings.eta_a
    kappa_a: float = settings.kappa_a
    tau_r: float = settings.tau_r


class CravingODEEngine:
    """
    Implements the craving-attention-reward ODE system with task input u(t)
    and discrete reward events approximated over a fixed time grid.
    """

    def __init__(self, params: ODEParams | None = None) -> None:
        self.params = params or ODEParams()

    def simulate(
        self,
        c0: float,
        a0: float,
        r0: float,
        horizon_minutes: float,
        dt_minutes: float,
        u_schedule: Iterable[float] | None = None,
        reward_pulses: Iterable[float] | None = None,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        n_steps = int(horizon_minutes / dt_minutes) + 1
        t = np.linspace(0.0, horizon_minutes, n_steps, dtype=float)
        c = np.empty_like(t)
        a = np.empty_like(t)
        r = np.empty_like(t)

        c[0] = c0
        a[0] = a0
        r[0] = r0

        if u_schedule is None:
            u_arr = np.zeros_like(t)
        else:
            u_arr = np.array(list(u_schedule), dtype=float)
            if u_arr.shape != t.shape:
                raise ValueError("u_schedule length must equal number of time steps.")

        if reward_pulses is None:
            reward_arr = np.zeros_like(t)
        else:
            reward_arr = np.array(list(reward_pulses), dtype=float)
            if reward_arr.shape != t.shape:
                raise ValueError("reward_pulses length must equal number of time steps.")

        p = self.params
        dt = dt_minutes

        for i in range(1, n_steps):
            u_t = u_arr[i - 1]

            dC = (
                p.alpha_c
                - p.beta_c * a[i - 1]
                - p.gamma_c * r[i - 1]
                - p.delta_c * c[i - 1]
            )
            dA = (
                -p.lambda_a * a[i - 1]
                + p.eta_a * u_t
                - p.kappa_a * c[i - 1]
            )
            dR = -r[i - 1] / p.tau_r

            c[i] = np.clip(c[i - 1] + dt * dC, 0.0, 1.0)
            a[i] = np.clip(a[i - 1] + dt * dA, 0.0, 1.0)
            base_r = np.clip(r[i - 1] + dt * dR, 0.0, 1.0)
            r[i] = np.clip(base_r + reward_arr[i - 1], 0.0, 1.0)

        return t, c, a, r
