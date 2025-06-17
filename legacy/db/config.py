import os
from pathlib import Path

from dotenv import load_dotenv

basedir = Path(".")
env_path = basedir / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "libbiblio"
    PROJECT_VERSION: str = "2.0.0a"

    #########################################################
    # DATABASE                                              #
    #########################################################
    DB_ENGINE: str = os.getenv("DB_ENGINE", "postgres")

    if DB_ENGINE == "postgres":
        POSTGRES_USER: str = os.getenv("POSTGRES_USER", "root")
        POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
        POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
        POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
        POSTGRES_DB: str = os.getenv("POSTGRES_DB", "test_db")

        DATABASE_URL = (
            f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
            f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
        )

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if self.DB_ENGINE == "sqlite":
            return "sqlite:///" + os.path.join(basedir, "test.db")
        elif self.DB_ENGINE == "postgres":
            return (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}"
                f"/{self.POSTGRES_DB}"
            )
        else:
            raise ValueError("Unknown db engine: {self.DB_ENGINE}")


settings = Settings()
