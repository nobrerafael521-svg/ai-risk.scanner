import os


class Settings:
    APP_NAME = "AI Risk Scanner"
    APP_VERSION = "0.1.0"

    # Server
    HOST = os.getenv("APP_HOST", "127.0.0.1")
    PORT = int(os.getenv("APP_PORT", 8000))

    # Environment
    ENV = os.getenv("APP_ENV", "development")


settings = Settings()
