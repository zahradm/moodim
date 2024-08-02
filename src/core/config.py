import os
from dataclasses import dataclass

from dynaconf import Dynaconf

current_directory = os.path.dirname(os.path.realpath(__file__))

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[
        f"{current_directory}/settings.toml",
        f"{current_directory}/.secrets.toml",
    ],
)


@dataclass(frozen=True, slots=True)
class Config:
    username: str
    password: str
    host: str
    port: str
    db_name: str


config = Config(
    username=settings.db.user_name,
    password=settings.db.password,
    host=settings.db.host,
    port=settings.db.port,
    db_name=settings.db.db_name,
)
