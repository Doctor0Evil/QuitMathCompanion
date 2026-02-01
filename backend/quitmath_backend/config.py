from functools import lru_cache
from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    app_name: str = "Quit-Math Companion Backend"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "CHANGE_ME_IN_PRODUCTION"
    access_token_expire_minutes: int = 60 * 24 * 7
    algorithm: str = "HS256"

    sql_database_url: AnyUrl | str = "sqlite+aiosqlite:///./quitmath.db"

    # ODE default parameters (can be user-specific in DB)
    alpha_c: float = 0.15
    beta_c: float = 0.35
    gamma_c: float = 0.25
    delta_c: float = 0.05

    lambda_a: float = 0.4
    eta_a: float = 0.5
    kappa_a: float = 0.3

    tau_r: float = 2.0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
