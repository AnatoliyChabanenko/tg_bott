from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton





button_hi = KeyboardButton('Привет! 👋')

button_1 =KeyboardButton('Ціни на культури')
button_2 =KeyboardButton('Розрахувати достаку',request_location=True)
button_3 =KeyboardButton('Звя\'затися зі мною', request_contact=True)



button21= KeyboardButton('Підписатися на розсилку')
button22 = KeyboardButton('Відписатись від розсилки')




markup1 = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2).add(button_1,button_2,button_3,button21)
markup2 = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2).add(button_1,button_2,button_3,button22)


