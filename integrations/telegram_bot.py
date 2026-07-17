import asyncio
from core.logger import get_logger
from core.config import CONFIG
logger = get_logger("TelegramBot")
class TelegramBot:
    def __init__(self):
        self.token = CONFIG['env']['TELEGRAM_BOT_TOKEN']
    async def poll(self):
        if not self.token:
            logger.warning("No Telegram token. Bot disabled.")
            return
        logger.info("Telegram bot polling (Mocked).")
        while True:
            await asyncio.sleep(60)
