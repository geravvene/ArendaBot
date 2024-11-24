from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import WebhookInfo, BotCommand
from aiogram.fsm.state import State, StatesGroup
from settings import get_settings, Settings
from db import create_storage

cfg: Settings = get_settings()
telegram_router = Router(name="telegram")
dp = Dispatcher(storage=create_storage())

dp.include_router(telegram_router)
bot = Bot(token=cfg.bot_token, default=DefaultBotProperties(
    parse_mode=ParseMode.HTML))


class Authorization(StatesGroup):
    password = State()


async def set_webhook(my_bot: Bot) -> None:
    async def check_webhook() -> WebhookInfo | None:
        try:
            webhook_info = await my_bot.get_webhook_info()
            return webhook_info
        except Exception:
            return

    current_webhook_info = await check_webhook()

    await my_bot.set_webhook(
        f"{cfg.base_webhook_url}{cfg.webhook_path}",
        secret_token=cfg.telegram_my_token,
        drop_pending_updates=current_webhook_info.pending_update_count > 0,
        max_connections=40 if cfg.debug else 100,
    )


async def set_bot_commands_menu(my_bot: Bot) -> None:
    commands = [
        BotCommand(command="/id", description="👋 Get my ID"),
        BotCommand(command="/start", description="Начать"),
    ]
    await my_bot.set_my_commands(commands)


async def start_telegram():
    await set_webhook(bot)
    await set_bot_commands_menu(bot)
