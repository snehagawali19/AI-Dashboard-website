from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ainews"
    REDIS_URL: str = "redis://localhost:6379/0"
    OPENAI_API_KEY: str = ""
    NEWSAPI_KEY: str = ""  # optional: newsapi.org free key
    SECRET_KEY: str = "change-me-in-production"
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "https://your-app.onrender.com"]
    AI_ENABLED: bool = True
    FETCH_INTERVAL_MINUTES: int = 15
    MAX_FEED_ITEMS: int = 50

settings = Settings()