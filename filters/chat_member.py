from aiogram.filters import BaseFilter
from aiogram import types
from typing import Union
from loader import bot
from data.config import GROUP_ID, ADMIN_ID

class ChatMemberFilter(BaseFilter):
    def __init__(self, chat_member: Union[str,list]):
        self.chat_member = chat_member

    async def __call__(self, message: types.Message) -> bool:
        user_data = await bot.get_chat_member(chat_id=GROUP_ID,user_id=message.from_user.id)
        user_status = user_data.status
        if isinstance(self.chat_member, str):
            if user_status == 'creator':
                return user_status.value == self.chat_member
            elif message.from_user.id != ADMIN_ID:
                await bot.send_message(chat_id=message.from_user.id, text=f'Пожалуйста не пишите сюда, я отвечаю на сообщения от администратора чата')
        else:
            return user_status.value in self.chat_member


