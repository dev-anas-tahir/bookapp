from typing import Optional
from pathlib import Path
from environs import Env


class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        # Initialize environs
        self.env = Env()
        self.env.read_env()  # This reads the .env file if it exists
        
        # Database settings
        self.db_user = self.env.str("DB_USER", "postgres")
        self.db_password = self.env.str("DB_PASSWORD", "postgres")
        self.db_host = self.env.str("DB_HOST", "localhost")
        self.db_port = self.env.int("DB_PORT", 5432)
        self.db_name = self.env.str("DB_NAME", "bookapp")
        
        # Application settings
        self.app_debug = self.env.bool("APP_DEBUG", False)
        self.app_env = self.env.str("APP_ENV", "development")
        self.host = self.env.str("HOST", "127.0.0.1")
        self.port = self.env.int("PORT", 8000)
        
        # Other settings as needed
        self.secret_key = self.env.str("SECRET_KEY", "your-secret-key-here")


# Create a global settings instance
settings = Settings()