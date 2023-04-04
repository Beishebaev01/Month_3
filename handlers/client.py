from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from config import bot
from keyboards.client_cb import start_markup
from database.bot_db import sql_command_random
from parser.my_git import parser


async def start_command(message: types.Message):
    await message.answer("Hello!", reply_markup=start_markup)


async def send_image(message: types.Message):
    photo = open('media/photo_2023-03-12_20-25-53.jpg', 'rb')
    await message.answer_photo(photo=photo)


async def help_command(message: types.Message):
    await message.answer("/start - Запуск бота"
                         "\n/mem - Фотка"
                         "\n/quiz - Викторина"
                         "\ndice - Игра против бота"
                         "\ngame - Анимированные эмоджи")


async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton("NEXT", callback_data="button_1")
    markup.add(button_1)

    question = "Какое настоящее имя у MiyaGi?"
    answer = [
        "Арген",
        "Рамиш",
        "Азамат",
        "Ати"
    ]
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="MiyaGi - Азамат Кудзаев",
        open_period=5,
        reply_markup=markup
    )


async def get_random_user(message: types.Message):
    random_user = await sql_command_random()
    await message.answer_photo(
        photo=random_user[-1],
        caption=f"Имя: {random_user[1]}"
                f"\nВозраст: {random_user[2]}"
                f"\nПол: {random_user[3]}"
                f"\nНаправление: {random_user[4]}"
                f"\nГруппа: {random_user[5]}")


async def get_repositories(message: types.Message):
    repositories = parser()
    for repos in repositories:
        await message.answer(
            f"<a href='{repos['2. Коды']}'>{repos['1. Репозиторий']}</a>\n\n"
            f"#{repos['3. Язык']}",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    "Перейти", url=repos['2. Коды']
                )
            ),
            parse_mode=ParseMode.HTML
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(send_image, commands=['mem'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(get_random_user, commands=['get'])
    dp.register_message_handler(get_repositories, commands=['repos'])


