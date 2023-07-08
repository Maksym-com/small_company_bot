import os
import logging

from dotenv import load_dotenv
from aiogram import executor, Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Configure logging
logging.basicConfig(level=logging.INFO)

load_dotenv()
proxy_url = "http://proxy.server:3128"
bot = Bot(token=os.getenv("TOKEN"), proxy=proxy_url)
dp = Dispatcher(bot, storage=MemoryStorage())
ADMINS = [829489904]
worker = ""
del_worker = ""
choice = ""
worker_s = ""
worker_p = ""
worker_i = ""

async def set_default_commands(dp):
    await bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустити бота.'),
            types.BotCommand('add', 'Додати працівника.'),
            types.BotCommand('remove', 'Звільнити працівника.'),
            types.BotCommand('view', 'Показати інформацію про працівників.'),
            types.BotCommand('change_salary', 'Змінити заробітню плату.'),
            types.BotCommand('change_position', 'Змінити посаду.'),
            types.BotCommand('worker_info', 'Переглянути інформацію про працівника.')
        ]
    )

async def on_startup(dp):
    await set_default_commands(dp)

class WorkerStates(StatesGroup):
    name_worker = State() 
    salary_worker = State() 
    position_worker = State() 
    final_add = State()
    remove0_worker = State()  
    change_salary_worker_0 = State()
    change_salary_worker_1 = State()
    change_position_worker_0 = State()
    change_position_worker_1 = State()
    info_worker_0 = State()

employees = {
    "Moraks": {
        "salary": 600,
        "position": "Junior Python Developer",
        "start_date": "2023-06-04"
    },
    "Yaroslav": {
        "salary": 1500,
        "position": "Manager",
        "start_date": "2023-06-04"
    },
    "Jack": {
        "salary": 5000,
        "position": "CEO",
        "start_date": "2023-06-04"
    },
}

# Стартове меню.

@dp.message_handler(commands='start')
async def start(message: types.Message, state:FSMContext):
    await message.answer(text='''Привіт!
\n Я бот який допоможе тобі переглядати інформацію про працівників твоєї компанії.\n 
Обери дію, яку хочеш виконати:\n
/add - Додати працівника;
/remove - Звільнити працівника;
/view - Показати інформацію про працівників;
/change_salary - Змінити заробітню плату;
/change_position - Змінити посаду;
/worker_info - Переглянути інформацію про працівника;
''')
    
# Функція add - додати працівника.

@dp.message_handler(commands='add')
async def add_worker(message: types.Message, state:FSMContext):
        await message.answer(text="Введіть ім'я та прізвище працівника якого хочете додати")
        await WorkerStates.name_worker.set()

@dp.message_handler(state=WorkerStates.name_worker)
async def name_worker(message: types.Message, state:FSMContext):
    worker = message.text
    async with state.proxy() as data:
        data["name"] = worker
    await message.answer("Введіть заробітню плату (USD)")
    await WorkerStates.salary_worker.set()

@dp.message_handler(state=WorkerStates.salary_worker)
async def salary_worker(message: types.Message, state:FSMContext):
    worker_salary = message.text
    async with state.proxy() as data:
        data["salary"] = worker_salary
    await message.answer(text="Введіть посаду працівника")
    await WorkerStates.position_worker.set()

@dp.message_handler(state=WorkerStates.position_worker)
async def position_worker(message: types.Message, state:FSMContext):
    worker_position = message.text
    async with state.proxy() as data:
        data["position"] = worker_position
    await message.answer(text="Коли працівник почав працювати (введіть дату (day-mounth-year))")
    await WorkerStates.final_add.set()

@dp.message_handler(state=WorkerStates.final_add)
async def final_add(message: types.Message, state:FSMContext):
    day_start = message.text
    async with state.proxy() as data:
        data["start_date"] = day_start
        employees[data["name"]] = {
            "salary": data["salary"],
            "position": data["position"],
            "start_date": data["start_date"]}
    await state.finish()
    await message.answer(text="Вітаю, працівника успішно додано")

# Функція remove - звільнити(видалити) працівника.

@dp.message_handler(commands="remove")
async def remove_worker(message: types.Message, state:FSMContext):
    await message.answer(text="Напишіть ім'я працівника якого бажаєте звільнити(видалити)")
    await WorkerStates.remove0_worker.set()

@dp.message_handler(state=WorkerStates.remove0_worker)
async def remove0_worker(message: types.Message, state:FSMContext):
    del_worker = message.text
    if del_worker in employees:
        async with state.proxy() as data:
            data["name"] = del_worker
        del employees[del_worker]
        await state.finish()
        await message.answer(text="Успішно видалено.")
    else:
        await message.answer(text="Такого працівника немає.")
        await state.finish()

# Функція view - показати інформацію про працівників.

@dp.message_handler(commands="view")
async def view_workers(message: types.Message, state:FSMContext):
    # await message.answer(text=f"{'Name':<15}{'Salary (USD)':<20}{'Position':20}{'Started to work':>20}\n\n")
    for worker in employees:
        await message.answer(text=f'''<b>Name: </b><u>{worker}</u>\n
<b>Salary: </b>{employees[worker]["salary"]}$
<b>Position: </b>{employees[worker]["position"]} 
<b>Start date: </b>{employees[worker]["start_date"]}
''', parse_mode='html')
    
# Функція change_salary - змінити заробітню плату.

@dp.message_handler(commands="change_salary")
async def change_salary_worker(message: types.Message, state:FSMContext):
    await message.answer(text="Напишіть ім'я працівника якому змінимо зарплатню")
    await WorkerStates.change_salary_worker_0.set()

@dp.message_handler(state=WorkerStates.change_salary_worker_0)
async def change_salary_worker_0(message: types.Message, state:FSMContext):
    worker_s = message.text
    if worker_s in employees:
        async with state.proxy() as data:
            data["name"] = worker_s
        await message.answer(text=f'На даний момент {worker_s} заробляє {employees[worker_s]["salary"]}$')
        await message.answer(text="Введіть нову зарплатню")
        await WorkerStates.change_salary_worker_1.set()
    else:
        await message.answer(text="Такого працівника немає.")
        await state.finish()

@dp.message_handler(state=WorkerStates.change_salary_worker_1)
async def change_salary_worker_1(message: types.Message, state:FSMContext):
    worker_s1 = message.text
    async with state.proxy() as data:
        data["salary"] = worker_s1
        employees[data["name"]]["salary"] = worker_s1 
    await state.finish()
    await message.answer(text=f'Успішно змінено! Тепер {data["name"]} заробляє - {worker_s1}$.')

# Функція change_position - змінити посаду.

@dp.message_handler(commands="change_position")
async def change_position_worker(message: types.Message, state:FSMContext):
    await message.answer(text="Напишіть ім'я працівника якому змінимо посаду")
    await WorkerStates.change_position_worker_0.set()

@dp.message_handler(state=WorkerStates.change_position_worker_0)
async def change_position_worker_0(message: types.Message, state:FSMContext):
    worker_p = message.text
    if worker_p in employees:
        async with state.proxy() as data:
            data["name"] = worker_p
        await message.answer(text=f'На даний момент {worker_p} - {employees[worker_p]["position"]}')
        await message.answer(text="Введіть нову посаду")
        await WorkerStates.change_position_worker_1.set()
    else:
        await message.answer(text="Такого працівника немає.")
        await state.finish()

@dp.message_handler(state=WorkerStates.change_position_worker_1)
async def change_position_worker_1(message: types.Message, state:FSMContext):
    worker_p1 = message.text
    async with state.proxy() as data:
            employees[data["name"]]["position"]  = worker_p1
    await state.finish()
    await message.answer(text=f"Успішно змінено! Тепер {worker_p} - {worker_p1}.")

# worker_info - переглянути інформацію про працівника.

@dp.message_handler(commands="worker_info")
async def info_worker(message: types.Message, state:FSMContext):
    await message.answer(text="Введіть ім'я працівника для перегляду інформації про нього")
    await WorkerStates.info_worker_0.set()

@dp.message_handler(state=WorkerStates.info_worker_0)
async def info_worker_0(message: types.Message, state:FSMContext):
    worker_i = message.text
    if worker_i in employees:
        async with state.proxy() as data:
            data["name"] = worker_i
        await message.answer(text=f'''<b>Name: </b><u>{worker_i}</u>\n
<b>Salary: </b>{employees[worker_i]["salary"]}$
<b>Position: </b>{employees[worker_i]["position"]} 
<b>Start date: </b>{employees[worker_i]["start_date"]}
''', parse_mode='html')
        await state.finish()
    else:
        await message.answer(text="Такого працівника немає.")
        await state.finish()


if __name__ == "__main__":
    print()
    executor.start_polling(dp, on_startup=on_startup)

