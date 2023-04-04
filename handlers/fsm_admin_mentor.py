from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import client_cb
from config import ADMINS
from database.bot_db import sql_command_insert


class FSMAdmin(StatesGroup):
    name = State()
    age = State()
    gender = State()
    direction = State()
    group = State()
    photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == "private" and message.chat.id in ADMINS:
        await FSMAdmin.name.set()
        await message.answer("Как тебя зовут?", reply_markup=client_cb.cancel_markup)
    else:
        await message.answer("Пиши в группу!")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Сколько тебе лет?", reply_markup=client_cb.cancel_markup)


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пиши числами!")
    elif int(message.text) < 16 or int(message.text) > 40:
        await message.answer("Возростное ограничение!")
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.answer("Пол?", reply_markup=client_cb.gender_markup)


async def load_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await FSMAdmin.next()
    await message.answer("Направление?", reply_markup=client_cb.cancel_markup)


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
    await FSMAdmin.next()
    await message.answer("Какая группа?", reply_markup=client_cb.cancel_markup)


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await FSMAdmin.next()
    await message.answer("Твоё фото", reply_markup=client_cb.cancel_markup)


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await message.answer_photo(
            photo=data['photo'],
            caption=f"Имя: {data['name']}"
                    f"\nВозраст: {data['age']}"
                    f"\nПол: {data['gender']}"
                    f"\nНаправление: {data['direction']}"
                    f"\nГруппа: {data['group']}")
    await FSMAdmin.next()
    await message.answer("Всё верно?", reply_markup=client_cb.submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text == "ДА":
        await sql_command_insert(state)
        await state.finish()
        await message.answer("Ты зареган!")
    elif message.text == "НЕТ":
        await state.finish()
        await message.answer("Пока!")
    else:
        await message.answer("Нормально пиши!")


async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
        await message.answer("Отменено!")


def register_handlers_fsm_anketa(dp: Dispatcher):
    dp.register_message_handler(cancel, Text(equals="cancel", ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_gender, state=FSMAdmin.gender)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(load_photo, state=FSMAdmin.photo,
                                content_types=['photo'])
    dp.register_message_handler(submit, state=FSMAdmin.submit)
