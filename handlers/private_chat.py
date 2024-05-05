from aiogram import types, F, Router

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.chat_type import ChatTypeFilter
from filters.chat_member import ChatMemberFilter
from loader import dp, bot
from data.config import ADMIN_ID, GROUP_URL, GROUP_ID
from states.state_chat import InfoChat


router = Router()

router.message.filter(ChatTypeFilter(chat_type='private'))
router.message.filter(ChatMemberFilter(chat_member='creator'))


time_lesson = ['02.05', '06.05', '11.05']
photo_ids = []
file_ids = []


@router.message(F.photo)
async def download_photo(message: types.PhotoSize):
    await bot.send_message(chat_id=ADMIN_ID,text='Фото сохранено')
    photo_ids.append(message.photo[-1].file_id)
    photo_chat = message.photo[-1].file_id
    file_ids.append(photo_chat)
    await bot.send_photo(chat_id=GROUP_ID, photo=file_ids[-1])


@router.message(F.text == "Спросить в чате")
async def ask_chat(message: types.Message, state: FSMContext):
    await message.answer("Напишите текст сообщение или нажмите Перейти в чат ")
    await state.set_state(InfoChat.user_text.state)


@router.message(InfoChat.user_text)
async def correspondent_for_to_admin(message: types.Message, state: FSMContext):
    correspondent_with_admin = InlineKeyboardBuilder()
    correspondent_with_admin.add(InlineKeyboardButton(text="Перейти в чата",url=GROUP_URL))
    await state.update_data(user_text=message.text)
    data = await state.get_data()
    user_text = data.get("user_text")
    await bot.send_message(GROUP_ID,f"Сообщение от администратора\n{user_text}")
    await message.answer(f"Сообщение отправлено! Если хотите перейти в чат, нажмите Перейти",reply_markup=correspondent_with_admin.as_markup())
    await state.clear()


@router.message(F.text == "Отправить расписание")
async def to_schedule(message: types.Message):
    await message.answer('Расписание отправлено')
    await bot.send_photo(chat_id=GROUP_ID, photo=file_ids[-1])
    photo_chat = message.photo[-1].file_id
    await bot.pin_chat_message(GROUP_ID, message_id=photo_chat)



