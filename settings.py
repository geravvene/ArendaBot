from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import final


@final
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.prod.env', '.dev.env'),
        env_file_encoding='utf-8')

    debug: bool = True
    bot_token: str = '8094916643:AAF93MkXE_BWCTv6FBXTqNrJ2bUHjdELGKI'
    base_webhook_url: str = 'https://arenda-bot.vercel.app'
    webhook_path: str = '/webhook'
    admin_chat_id: int = -1002374845535
    admin_topic_id: int = 2
    maid_chat_id: int = -1002385562114
    maid_topic_id: int = 2
    # Additional security token for webhook
    telegram_my_token: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


@lru_cache()
def get_settings() -> Settings:
    return Settings()
