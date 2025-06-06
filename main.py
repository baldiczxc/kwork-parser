import aiohttp
import asyncio

from aiogram import Bot
from loguru import logger

# Заменяем импорт Settings на импорт config
from config import (
    KWORK_CATEGORIES,
    POLL_INTERVAL_SECONDS,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
)

from src.parser import fetch_new_orders
from src.telegram_notifier import send_orders


async def fetch_worker(bot: Bot, category_id: str) -> None:
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                orders: list[dict] = await fetch_new_orders(
                    session=session,
                    category_id=category_id,
                )
                if orders:
                    await send_orders(bot=bot, chat_id=TELEGRAM_CHAT_ID, orders=orders)
            except Exception:
                logger.exception(f"При проверке новых заказов {category_id=} произошла ошибка")

            await asyncio.sleep(POLL_INTERVAL_SECONDS)

async def runner() -> None:
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Заполните TELEGRAM_BOT_TOKEN в config.py")
        return

    logger.add("parser.log", rotation="1 week")  # файл-лог

    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    # KWORK_CATEGORIES теперь список, если нужно - преобразуем к строкам
    fetch_worker_tasks = [
        fetch_worker(bot=bot, category_id=str(category_id))
        for category_id in KWORK_CATEGORIES
    ]

    await asyncio.gather(*fetch_worker_tasks)

if __name__ == "__main__":
    asyncio.run(runner())
