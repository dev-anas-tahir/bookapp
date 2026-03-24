from pathlib import Path

from environs import Env


def get_settings_path() -> Path:
    """Get the project root path based on this file's location."""
    # This file is at core/settings.py, so project root is one level up
    return Path(__file__).parent.parent


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self):
        # Initialize environs
        self.env = Env()

        # Load .env from project root (works regardless of where script is run from)
        project_root = get_settings_path()
        env_path = project_root / ".env"
        self.env.read_env(path=str(env_path))

        # Database settings
        self.db_user = self.env.str("DB_USER")
        self.db_password = self.env.str("DB_PASSWORD")
        self.db_host = self.env.str("DB_HOST")
        self.db_port = self.env.int("DB_PORT")
        self.db_name = self.env.str("DB_NAME")

        # Application settings
        self.app_debug = self.env.bool("APP_DEBUG")
        self.app_env = self.env.str("APP_ENV")
        self.host = self.env.str("HOST")
        self.port = self.env.int("PORT")

        # Security settings
        self.secret_key = self.env.str("SECRET_KEY")
        self.algorithm = self.env.str("ALGORITHM")
        self.access_token_expire_minutes = self.env.int("ACCESS_TOKEN_EXPIRE_MINUTES")


# Create a global settings instance
settings = Settings()
