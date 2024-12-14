# Third-Party Libraries
from pydantic_settings import BaseSettings, SettingsConfigDict


class ClientSettings(BaseSettings):
    max_concurrent_requests: int = 185
    max_retry_attempts: int = 3
    max_connections: int = 100
    interval: int | float = 0
    timeout: int | None = None
    follow_redirects: bool = True

default_settings: ClientSettings = ClientSettings()


class BaseConfig(SettingsConfigDict):
    env_file: str = '../env'
    env_file_encoding: str = 'utf-8'
