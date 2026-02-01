from dataclasses import dataclass


@dataclass
class EcoCoefficients:
    plastic_per_disposable_g: float = 15.0
    battery_per_disposable_g: float = 10.0
    co2e_per_disposable_kg: float = 0.02
    karma_per_gram: float = 0.0005
    karma_per_kg_co2e: float = 1.0


class EcoImpactService:
    """
    Computes eco-impact metrics for avoided disposable vapes.
    """

    def __init__(self, coeffs: EcoCoefficients | None = None) -> None:
        self.coeffs = coeffs or EcoCoefficients()

    def disposables_to_eco(
        self,
        avoided_units: float,
    ) -> dict[str, float]:
        plastic_g = avoided_units * self.coeffs.plastic_per_disposable_g
        battery_g = avoided_units * self.coeffs.battery_per_disposable_g
        co2e_kg = avoided_units * self.coeffs.co2e_per_disposable_kg

        karma_mass = (plastic_g + battery_g) * self.coeffs.karma_per_gram
        karma_climate = co2e_kg * self.coeffs.karma_per_kg_co2e
        total_karma = karma_mass + karma_climate

        return {
            "plastic_g": plastic_g,
            "battery_g": battery_g,
            "co2e_kg": co2e_kg,
            "karma": total_karma,
        }
