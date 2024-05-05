from aiogram.fsm.context import FSMContext
from aiogram import types, F, Router

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from filters.chat_type import ChatTypeFilter
from datetime import datetime
from loader import dp, bot
from data.config import ADMIN_ID, ADMIN_URL,GROUP_ID
from states.state_chat import InfoChat
from data.database import students_help


router = Router()
router.message.filter(ChatTypeFilter(chat_type='supergroup'))

file_ids = []
users_poll = {}
answer_no = []
answers = []
wisits = []

# https://github.com/AlexandrNoks/DrivingSchoolBot.git

users_log = {
    '@c_const': 'Дарья Вождение',
    '@small5686': 'Александр Вождение',
    '@Sosipisisisi': 'Али Вождение',
    '@Olga_Muss_87': 'Ольга Вождении',
    '+7 986 789 4732': 'Татьяна Вождение',
    '@chket56':'Алексей Вождение',
    '@igorbokarev56': 'Игорь Вождение',
    '+7 922 544 3944': 'Галина Вождение',
    '@anara_ali': 'Анара Вождение',
    '+7 987 782 5486': 'Рауме Вождение',
    '+7 922 895 7305': 'Виктория Вождение',
    '@pagottala': 'Алёна Вождение',
    '@Kempache95': 'Павел Вождение',
    '+7 922 804 4788': 'Дмитрий Вождение',
    '+7 922 839 5548': 'Наталия Вождение',
    '@arsenzy17': 'Арсений Вождение',
    '@KataySuyunchik': 'Катя Вождение',
    '@notsadbutpoeti': 'Дмитрий Вождение'
}

res = [1924126688,
       993482289,
       6284449881]

users = dict(zip(users_log,res))

time_lesson = ['02.05','06.05','11.05']
photo_ids = []


@router.message(F.text == "+")
async def ask_to_chat(message: types.Message, state: FSMContext):
    user_name = message.from_user.username
    await state.update_data(user_name=user_name)
    data = await state.get_data()
    users = data.get('user_name')
    answers.append(users)
    await state.set_state(InfoChat.user_name.state)


@router.message(Command('clear'))
async def clear_poll(message: types.Message):
    await message.answer(f"Написали {str(len(answers))} из {str(len(students_help))}")


@router.message(F.text == "Написать админу")
async def message_admin(message: types.Message, state: FSMContext):
    correspondent_with_admin = InlineKeyboardBuilder()
    correspondent_with_admin.add(InlineKeyboardButton(text="Перейти в чата с админом",url=ADMIN_URL))
    await state.update_data(user_text=message.text)
    data = await state.get_data()
    user_text = data.get("user_text")
    await bot.send_message(ADMIN_ID,f"Сообщение от пользователя {message.from_user.first_name}\n{user_text}")
    await message.answer(f"Если хотите в личную переписку нажмите Перейти",reply_markup=correspondent_with_admin.as_markup())
    await state.clear()


@router.message(F.photo)
async def download_photo(message: types.PhotoSize):
    photo_chat = message.photo[-1].file_id
    file_ids.append(photo_chat)


@router.message(F.text == 'Узнать расписание')
async def get_shedule(message: types.Message):
    try:
        await message.answer('Расписание отправлено')
        await bot.send_photo(chat_id=message.from_user.id, photo=file_ids[-1])
    except IndexError:
        await StopIteration


# Начать опрос
@dp.message(F.text == "Создать опрос")
async def start_poll(message: types.Message):
    await message.answer(f'Сегодня {datetime.today().date()} Завтра в {time_lesson[0]}')
    close_poll = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Закрыть опрос", callback_data="PollClose")]])
    await bot.send_poll(GROUP_ID,
        question=f"Опрос, Выберите 'Да' если приндете на урок или 'Нет' если не сможете",
        correct_option_id=1,
        options=["Да", "Нет"], type="quiz", is_closed=False, is_anonymous=False, reply_markup=close_poll)


# Ответы
@dp.poll_answer()
async def date_answer(poll: types.PollAnswer):
    user_id = poll.user.id
    user_name = poll.user.first_name
    user_answer = poll.option_ids
    for i in user_answer:
        if i == 0:
            i = "Да"
            users_poll[user_name] = i
        elif i == 1:
            i = "Нет"
            answer_no.append(user_id)
            users_poll[user_name] = i



# Опрос
@dp.callback_query(F.data.startswith("Poll"))
async def get_name_contest(call: types.CallbackQuery):
    if call.data == 'PollClose':
        for answer in users_poll:
            if users_poll[answer] == 'Нет'and call.from_user.first_name == answer:
                await bot.send_message(chat_id=ADMIN_ID,text=f"{answer} Не придут на занятие")
                message_choice = InlineKeyboardMarkup(
                    inline_keyboard=[[
                        InlineKeyboardButton(text=f"@{call.from_user.username}", url=f'https://t.me/{call.from_user.username}')
                    ]])
                await bot.send_message(chat_id=ADMIN_ID, text="Написать им в личку?", reply_markup=message_choice)
            else:
                bot.send_message(chat_id=ADMIN_ID,text='Пришли все!')
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


