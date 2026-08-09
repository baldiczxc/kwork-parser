import asyncio

import aiohttp
from aiogram import Bot
from loguru import logger

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
                    await send_orders(
                        bot=bot,
                        chat_id=TELEGRAM_CHAT_ID,
                        orders=orders,
                    )

            except asyncio.TimeoutError:
                logger.warning(
                    f"Таймаут при проверке заказов {category_id=}, повтор через {POLL_INTERVAL_SECONDS}с"
                )

            except Exception:
                logger.exception(
                    f"При проверке новых заказов {category_id=} произошла ошибка"
                )

            await asyncio.sleep(POLL_INTERVAL_SECONDS)


async def runner() -> None:
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Заполните TELEGRAM_BOT_TOKEN в config.py")
        return

    logger.info("Создаем Telegram Bot...")

    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    try:
        tasks = [
            fetch_worker(
                bot=bot,
                category_id=str(category_id),
            )
            for category_id in KWORK_CATEGORIES
        ]

        await asyncio.gather(*tasks)

    finally:
        logger.warning("Закрываем Telegram session...")
        await bot.session.close()


async def main() -> None:
    logger.add("parser.log", rotation="1 week")

    while True:
        try:
            await runner()

        except KeyboardInterrupt:
            raise

        except Exception:
            logger.exception(
                "Runner crashed. Restarting in 10 seconds..."
            )

        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())