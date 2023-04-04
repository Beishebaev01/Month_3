from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import ADMINS, bot
from apscheduler.triggers.cron import CronTrigger


async def my_birth_time(bot: Bot):
    await bot.send_message(ADMINS[0], "С днём рождения!")


async def set_scheduler():
    scheduler = AsyncIOScheduler(timezone='Asia/Bishkek')
    scheduler.add_job(
        my_birth_time,
        trigger=CronTrigger(
            month=9, day=8, hour=11, minute=10
        ),
        kwargs={"bot": bot}
    )
    scheduler.start()
