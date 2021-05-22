import kakieto_funk as fu
import config2
import logging
import asyncio
import keybord_my as kb
from google import proschet
from sqlighter import SQLighter
from aiogram import Bot, Dispatcher, executor, types
from parsing_class import Nibulon
from datetime import datetime
from my_text import Text

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config2.TOKEN)
dp = Dispatcher(bot)
db = SQLighter('db.db')
nb = Nibulon()
text = Text()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if not fu.user_subskribe(message):
        await message.answer(text.start(), reply_markup=kb.markup1)
    else:
        await message.answer(text.start(), reply_markup=kb.markup2)


@dp.message_handler(text=['Ціни на культури'])
async def process_command(message: types.Message):
    prise = fu.read_json()
    data = datetime.today().strftime("%d.%m.%Y")
    await message.answer(text.prise(data,prise), reply_markup=kb.markup1)


@dp.message_handler(content_types=['location'])
async def handle_loc(message):
    km = float(proschet(message.location))
    prise = round(km * 1.1)

    await message.answer(text.location(km, prise),
        reply_markup=kb.markup1)


@dp.message_handler(content_types=['contact'])
async def handle_loc(message: types.Message):
    phone = message['contact']['phone_number']
    name = message['contact']['first_name']
    if not (db.subscriber_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id, False)
        db.add_phone(message.from_user.id, phone)
    else:
        db.add_phone(message.from_user.id, phone)
    if fu.vremya():
        await message.answer(text.contakt1(), reply_markup=kb.markup1)
    else:
        await message.answer(text.contakt2(), reply_markup=kb.markup1)

    admin = db.get_admin()
    for admin_user in admin:
        await bot.send_message(admin_user[1], (name, phone), disable_notification=True)


@dp.message_handler(text=['Підписатися на розсилку'])
async def subscribe(massage: types.Message):
    if not (db.subscriber_exists(massage.from_user.id)):
        db.add_subscriber(massage.from_user.id)
        await massage.answer(text.podpiska(), reply_markup=kb.markup2)
    else:
        db.update_subscription(massage.from_user.id, True)
        await massage.answer(text.podpiska(), reply_markup=kb.markup2)


@dp.message_handler(text=['Відписатись від розсилки'])
async def subscribe(massage: types.Message):
    db.update_subscription(massage.from_user.id, False)
    await massage.answer(f'{text.otpiska()}', reply_markup=kb.markup1)


@dp.message_handler(commands=['tellall'])
async def mailing(message: types.Message):
    if fu.admin_validate(message):
        await fu.send_all()


@dp.message_handler(commands=['new_admin'])
async def new_admin(message: types.Message):
    if fu.admin_validate(message):
        db.add_admin(str(message["text"].split()[1]))


# @dp.message_handler(commands=['new_admin1'])
# async def new_admin(message: types.Message):
#     db.add_admin(str(message["text"].split()[1]))

async def my_parsing(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        nb.update_content()
        await fu.send_all()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(my_parsing(10000))
    executor.start_polling(dp, skip_updates=True)
