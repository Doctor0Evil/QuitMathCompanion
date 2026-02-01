from dataclasses import dataclass

import numpy as np

from ..models import DailyState


@dataclass
class MarkovParams:
    theta_c_relapse: float = 0.6
    theta_a_protect: float = 0.4
    k_relapse: float = 4.0
    k_recovery: float = 4.0


class DailyMarkovModel:
    """
    Simple three-state daily Markov abstraction:
    S0: Smoking
    S1: Abstinent, high withdrawal
    S2: Stable abstinent
    """

    def __init__(self, params: MarkovParams | None = None) -> None:
        self.params = params or MarkovParams()

    def transition_probabilities(
        self,
        state: DailyState,
        avg_c: float,
        avg_a: float,
        avg_r: float,
    ) -> dict[DailyState, float]:
        p = self.params
        if state == DailyState.S1_WITHDRAWAL:
            x_relapse = avg_c - p.theta_c_relapse - (avg_a - p.theta_a_protect)
            p_s1_s0 = 1.0 / (1.0 + np.exp(-p.k_relapse * x_relapse))

            x_recover = avg_r + avg_a - p.theta_a_protect
            p_s1_s2 = 1.0 / (1.0 + np.exp(-p.k_recovery * x_recover))

            p_s1_s0 = float(np.clip(p_s1_s0, 0.0, 1.0))
            p_s1_s2 = float(np.clip(p_s1_s2, 0.0, 1.0))
            stay = float(np.clip(1.0 - p_s1_s0 - p_s1_s2, 0.0, 1.0))
            return {
                DailyState.S0_SMOKING: p_s1_s0,
                DailyState.S1_WITHDRAWAL: stay,
                DailyState.S2_STABLE: p_s1_s2,
            }

        if state == DailyState.S0_SMOKING:
            p_quit = float(np.clip(0.1 + 0.4 * avg_r, 0.0, 1.0))
            return {
                DailyState.S0_SMOKING: 1.0 - p_quit,
                DailyState.S1_WITHDRAWAL: p_quit,
                DailyState.S2_STABLE: 0.0,
            }

        if state == DailyState.S2_STABLE:
            relapse = float(np.clip(0.05 + 0.4 * (avg_c - avg_a), 0.0, 1.0))
            return {
                DailyState.S0_SMOKING: relapse * 0.2,
                DailyState.S1_WITHDRAWAL: relapse * 0.8,
                DailyState.S2_STABLE: 1.0 - relapse,
            }

        raise ValueError(f"Unknown state: {state}")
