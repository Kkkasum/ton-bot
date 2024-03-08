from pydantic_settings import BaseSettings, SettingsConfigDict

from ._constants import BASE_DIR


class Config(BaseSettings):
    BOT_TOKEN: str

    TON_API_KEY: str

    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env', env_file_encoding='utf-8', extra='ignore')


config = Config()
