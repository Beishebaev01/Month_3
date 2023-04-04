# from aiogram import types, Dispatcher
# from time import sleep
# import random
#
#
# async def delete_sticker(message: types.Message):
#     await message.delete()
#     await message.answer("Нельзя отправлять стикеры!")
#
#
# async def bad_words_filter(message: types.Message):
#     bad_words = ['html', 'js', 'css', 'жинди', 'дурак']
#     for word in bad_words:
#         if word in message.text.lower().replace(' ', ''):
#             await message.answer("Не матерись!")
#             await message.delete()
#             break
#
#     if message.text == "game":
#         animated_emojis = ['🎯', '🎳', '⚽️', '🏀', '🎰', '🎲']
#         random_emoji = random.choice(animated_emojis)
#         await message.answer(random_emoji)
#
#     # extra homework
#     if message.text == "dice":
#         await message.answer("Бот")
#         a = await message.answer_dice()
#         await message.answer(f"{message.from_user.full_name}")
#         b = await message.answer_dice()
#         sleep(5)
#         if a.dice.value > b.dice.value:
#             await message.answer("Выиграл Бот")
#         else:
#             await message.answer(f"Выиграл {message.from_user.full_name}")
#
#
# def register_handlers_extra(dp: Dispatcher):
#     dp.register_message_handler(bad_words_filter, content_types=['text'])
#     dp.register_message_handler(delete_sticker, content_types=['sticker'])
from aiogram import types, Dispatcher
import openai
from config import OPENAI_TOKEN


openai.api_key = OPENAI_TOKEN


async def chat_gpt(message: types.Message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6
    )
    await message.answer(response['choices'][0]["text"])


def register_handlers_extra(dp: Dispatcher):
    dp.register_message_handler(chat_gpt)