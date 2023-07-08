import os
import logging

from dotenv import load_dotenv
from aiogram import executor, Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from films import films
from films import me


logging.basicConfig(level=logging.INFO)
load_dotenv()
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())

ADMINS = [829489904]


# @dp.message_handler()
# async def echo(message: types.Message):
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)
#     print(message.text)
#     await message.answer(message.text)
async def set_default_commands(dp):
    await bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустити бота.'),
            types.BotCommand('add_film', 'Додати новий фільм.'),
            types.BotCommand('me', 'Про мене.')
        ]
    )

async def on_startup(dp):
    await set_default_commands(dp)

@dp.message_handler(commands="me")
async def get_me_info(message: types.Message):
    frase1 =  f'{me["name"]}'
    frase2 = f'{me["desription"]}'
    await bot.send_photo(message.chat.id, me["photo"])
    await message.answer(text=frase1)
    await message.answer(text=frase2)


    # me_ha = me[callback_query.data]
    # me_neha = me_ha[callback_query.data]
    # message = f'{me_ha("name")}{me_ha("description")}'
    # await bot.send_message(callback_query.chat.id, message, parse_mode='html')
    

@dp.message_handler(commands='start')
async def start(message: types.Message):
    film_choice = InlineKeyboardMarkup()
    for film in films:
        button = InlineKeyboardButton(text=film, callback_data=film)
        film_choice.add(button)
    await message.answer(text="Привіт! Я бот-кіноафіша!\n Обери фільм, про який хочеш дізнатись.", reply_markup=film_choice)


@dp.callback_query_handler()
async def get_film_info(callback_query: types.CallbackQuery):
    if callback_query.data in films.keys():
        film = films[callback_query.data]
        await bot.send_photo(callback_query.message.chat.id, film["photo"])
        message = f"<b>Film url:</b> {film['site_url']}\n\n<b>About:</b> {film['description']}\n\n<b>Rate:</b> {film['rating']}"
        await bot.send_message(callback_query.message.chat.id, message, parse_mode='html')
    else:
        await bot.send_message(callback_query.message.chat.id, "Фільм не знайдено")

    # if callback_query.data is films.get("me"):
    #     me = "me"[callback_query.data]
    #     await bot.send_photo (callback_query.message.chat.id, me("photo"))
    #     message = f"{me['site_url']}{me['description']}"
    #     await bot.send_message(callback_query.message.chat.id, message, parse_mode='html')
    # else:
    #     await bot.send_message(callback_query.message.chat.id, "Мене не знайдено")

# @dp.message_handler1(commands='start')
# async def start(message: types.Message):
#     film_choice = InlineKeyboardMarkup()
#     for me in films:
#         button = InlineKeyboardButton(text=me, callback_data=me)
#         film_choice.add(button)
#     await message.answer(text="Можеш також дізнатись по мене", reply_markup=)

# @dp.callback_query_handler1()
# async def get_me_info(callback_query: types.CallbackQuery):
#     if callback_query.data in me1.keys():
#         me = me1[callback_query.data]
#         await bot.send_photo (callback_query.message.chat.id, me["photo"])
#         message = f"<b>Name:</b> {me['name']}\n\n<b>About:</b> {me['desription']}"
#         await bot.send_message(callback_query.message.chat.id, message, parse_mode='html')
#     else:
#         await bot.send_message(callback_query.message.chat.id, "Мене не знайдено")
    
if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
