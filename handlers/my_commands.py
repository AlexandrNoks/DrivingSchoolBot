from loader import dp, bot
from aiogram import types, F, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart,Command
from aiogram.fsm.context import FSMContext
from filters.chat_type import ChatTypeFilter
from filters.chat_member import ChatMemberFilter
from data.database import *
from data.config import *
from keyboards.start_bot_btn import start_button_admin
from states.state_chat import *
from handlers.chat import answers

result = []
router = Router()

date_now = datetime.today().date()
reming = datetime.now().weekday()

router.message.filter(ChatTypeFilter(chat_type='private'))
router.message.filter(ChatMemberFilter(chat_member='creator'))
list_lessons = list(lessons.keys())
list_ticher = list(lessons.values())


@router.message(CommandStart())
async def command_start(message: types.Message):
    button_start = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Расписание', callback_data="startSchedule"),
                InlineKeyboardButton(text="Журнал", callback_data="startBook")
            ],
            [
                InlineKeyboardButton(text="Добавить",callback_data="remindAdd"),
                InlineKeyboardButton(text="Удалить",callback_data="remindDel")
            ]
        ]
    )
    await message.answer("Выберете задачу:",reply_markup=button_start)


@dp.callback_query(F.data.startswith('startSchedule'))
async def callback_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f"Введите дату: ")
    await state.set_state(Schedule.date_lesson.state)


@dp.message(Schedule.date_lesson)
async def get_lesson(message: types.Message, state: FSMContext):
    date_lesson = message.text
    await state.update_data(date_lesson=date_lesson)
    await message.answer(f"Введите предмет: ")
    await state.set_state(Schedule.lesson.state)


@dp.message(Schedule.lesson)
async def get_time(message: types.Message, state: FSMContext):
    lesson = message.text
    await state.update_data(lesson=lesson)
    await message.answer(f"Введите время: ")
    await state.set_state(Schedule.time.state)


@dp.message(Schedule.time)
async def ask_bot(message: types.Message, state: FSMContext):
    time = message.text
    await state.update_data(time=time)
    await state.set_state(Schedule.time.state)
    data = await state.get_data()
    data_date = data.get('date_lesson')
    data_lesson = data.get('lesson')
    data_time = data.get('time')
    now_weekday = str(data_date).split('.')
    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    for i in range(len(weekdays)):
        if i == datetime(int(now_weekday[0]), int(now_weekday[1]), int(now_weekday[2])).weekday():
            reming_lesson = reming - i
            weekdays_date = weekdays[i]
            for item in lessons:
                if data_lesson in item:
                    schedule = '/'.join(f"{weekdays_date} / {data_lesson} / {data_time} / {lessons[item]}")
                    result.append(schedule)
                    await bot.send_message(ADMIN_ID,text=f"{weekdays_date} / {data_lesson} / {data_time} / {lessons[item]}\n Занятие через {str(reming_lesson)} дня")
        else:
            pass
    await state.clear()


@dp.callback_query(F.data.startswith('startBook'))
async def callback_start(call: types.CallbackQuery):
   list_students = list(students_help.keys())
   for i in range(len(list_students)):
       try:
           if answers[i] not in list_students:
               await call.message.answer(f"{list_students[i]} Не были на уроки",reply_markup=start_button_admin)
           else:
               pass
       except IndexError:
           break


@dp.callback_query(F.data.startswith('remindAdd'))
async def callback_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите названия предмета: ")
    await state.set_state(Remind.new_lesson.state)


@dp.message(Remind.new_lesson)
async def command_help(message: types.Message, state: FSMContext):
    new_lesson = message.text
    await state.update_data(new_lesson=new_lesson)
    await message.answer("Введите имя преподавателя: ")
    await state.set_state(Remind.new_ticher.state)


@dp.message(Remind.new_ticher)
async def command_help(message: types.Message, state: FSMContext):
    new_ticher = message.text
    await state.update_data(new_ticher=new_ticher)
    data = await state.get_data()
    data_lesson = data.get('new_lesson')
    data_ticher = data.get('new_ticher')
    if data_lesson in lessons:
        await message.answer("Данные предмет уже есть в списке")
    else:
        lessons[data_lesson] = data_ticher

        await message.answer("Данные добавлены!")
        await state.clear()


@dp.callback_query(F.data.startswith('remindDel'))
async def callback_start(call: types.CallbackQuery, state: FSMContext):
   await call.message.answer("Введите название предмета")
   await state.set_state(Remind.del_lesson.state)


@dp.message(Remind.del_lesson)
async def command_help(message: types.Message, state: FSMContext):
    del_lesson = message.text
    await state.update_data(del_lesson=del_lesson)
    data = await state.get_data()
    data_lesson = data.get('del_lesson')
    if data_lesson in lessons:
        del lessons[data_lesson]
        await message.answer("Внимание предмет удален! Данные обновлены!")
    else:
        await message.answer("Предмет не найден!")



@dp.message(Command('help'))
async def command_help(message: types.Message):
        help_button = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=f"Студенты",callback_data=f"helpStudents"),
            InlineKeyboardButton(text=f"Преподаватели",callback_data=f"helpTitchers")
            ]]
        )
        await message.answer("Данные",reply_markup=help_button)


@dp.callback_query(F.data.startswith('help'))
async def callback_start(call: types.CallbackQuery):
    if call.data == 'helpStudents':
        for data in students_help:
            await call.message.answer(f"{data}")
    if call.data == 'helpTitchers':
        for data in lessons:
            await call.message.answer(f"{data} : {lessons[data]}")
