"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Environment
    environment: str = "sandbox"
    project_id: str = "tadakayo-qr-connect"
    region: str = "asia-northeast1"

    # API settings
    base_url: str = "http://localhost:8080"
    default_currency: str = "JPY"
    provider_timeout_ms: int = 10000

    # Logging
    log_level: str = "INFO"

    # PayPay settings
    paypay_api_key: str = ""
    paypay_api_secret: str = ""
    paypay_merchant_id: str = ""

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"

    @property
    def paypay_production_mode(self) -> bool:
        """Check if PayPay should use production mode."""
        return self.environment == "production"


settings = Settings()
