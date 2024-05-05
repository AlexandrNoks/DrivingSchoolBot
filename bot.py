import asyncio

from handlers import chat,private_chat,my_commands
from keyboards.start_bot_btn import start_button_admin,start_button_user
import logging
from data.config import ADMIN_ID, GROUP_ID
from datetime import datetime


async def on_startup():
    from loader import bot,dp
    from handlers import router
    dp.include_routers(chat.router, private_chat.router, my_commands.router)
    if datetime.now().weekday() == 4 or datetime.now().weekday() == 6:
        await bot.send_message(ADMIN_ID,'Бот Запущен и готов к работе! Не забудь про расписание', reply_markup=start_button_admin)
    else:
        await bot.send_message(ADMIN_ID,'Бот Запущен и готов к работе!', reply_markup=start_button_admin)
    await bot.send_message(GROUP_ID,f"{datetime.today().strftime('%d.%m.%Y')}", reply_markup=start_button_user)
    await dp.start_polling(bot)
    await dp.set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)

    logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    try:
        asyncio.run(on_startup())
        print("Hello")
    except KeyboardInterrupt:
        print("Exit")



# 1721708270:AAGIimt6k-cTuSQmS2pExN9dDwVpIiV7eTY