from decouple import config
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

TOKEN = config("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

ADMINS = (524696368, )
OPENAI_TOKEN = "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"