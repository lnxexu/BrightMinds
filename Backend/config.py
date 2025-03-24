from datetime import timedelta
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT Settings
    JWT_SECRET_KEY: str = "your-secret-key-here"  # Change this in production!
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_DELTA: timedelta = timedelta(days=7)

    # OAuth Settings
    GOOGLE_CLIENT_ID: str = ""  # Add your Google Client ID
    GOOGLE_CLIENT_SECRET: str = ""  # Add your Google Client Secret
    
    FACEBOOK_APP_ID: str = ""  # Add your Facebook App ID
    FACEBOOK_APP_SECRET: str = ""  # Add your Facebook App Secret

    class Config:
        env_file = ".env"

settings = Settings()
