import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import BaseStorage
from data.config import BOT_TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
storage = BaseStorage
dp = Dispatcher()
router = Router()



__all__ = ["bot","storage","dp","router"]