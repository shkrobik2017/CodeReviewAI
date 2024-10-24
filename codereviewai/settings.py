from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        frozen = True

    OPENAI_API_KEY: str = Field(
        ...,
        description="Your OpenAI API key"
    )

    GITHUB_API_TOKEN: str = Field(
        ...,
        description="Your GitHub token"
    )

    REDIS_HOST: str = Field(
        default="localhost",
        description="Your Redis host"
    )

    REDIS_PORT: int = Field(
        default=6379,
        description="Your Redis port"
    )

    BASE_URL: str = Field(
        ...,
        description="Base URL for your FastAPI app"
    )


settings = Settings()
