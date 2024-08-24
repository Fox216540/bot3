from aiogram import types, Bot, executor
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

bot = Bot(token="")
# Диспетчер
dp = Dispatcher(bot,storage=MemoryStorage())

def check_sub_channel(chat_member):
    if chat_member.status != 'left':
        return True
    else:
        return False


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    channels = cursor.execute(f"SELECT * FROM url").fetchall()
    greeting = cursor.execute(f"SELECT * FROM text_greetings").fetchall()[0][0]
    if all([check_sub_channel(await bot.get_chat_member(chat_id=int(x[1]), user_id=message.chat.id)) for x in channels]):
        text = cursor.execute(f"SELECT * FROM text").fetchall()[0][0]
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            KeyboardButton(text="Отправить фото"),
        ]
        markup.add(*buttons)
        await message.answer(text, reply_markup=markup)
        conn.commit()
        conn.close()
    else:
        markup = InlineKeyboardMarkup()
        for channel in channels:
            item = KeyboardButton(text="Подписаться",
                                url=f"https://t.me/{channel[0].replace('@','')}")

            markup.add(item)
        item2 = InlineKeyboardButton('Подписался!', callback_data='button1')
        markup.add(item2)
        await message.answer(greeting,reply_markup=markup)
        conn.commit()
        conn.close()



@dp.message_handler(commands=['7%oecf*h'])
async def number(message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO admin (id) VALUES(?)", (message.chat.id,))
        conn.commit()
        conn.close()
    except:
        conn.commit()
        conn.close()
    await message.answer('Добро пожаловать в админ панель!\nЧто вы хотите сделать\n\nВМЕСТО СКОБОК НАПИСАТЬ ТО ЧТО ТРЕБУЕТСЯ\n\nУдалить канал:/delete (channel_id)\n\nДобавить канал:/add (ссылка на канал) (channel_id)\n\nИзменить приветствие:/gree (text)\n\nИзменить текст:/text (text)')



@dp.message_handler(commands=['delete'])
async def start(message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    admin = cursor.execute(f"SELECT id FROM admin").fetchall()
    if any([int(message.chat.id) == int(x[0]) for x in admin]):
        try:
            cursor.execute(f"DELETE FROM url WHERE id = '{(message.text).split()[1]}'")
            conn.commit()
            conn.close()
            await message.answer('Канал удален')
        except:
            await message.answer('Что-то не так.Попробуйте еще раз!')
            conn.commit()
            conn.close()
    else:
        await message.answer('Вы не админ')
        conn.commit()
        conn.close()

@dp.message_handler(commands=['add'])
async def start(message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    admin = cursor.execute(f"SELECT id FROM admin").fetchall()
    if any([int(message.chat.id) == int(x[0]) for x in admin]):
        try:
            cursor.execute("INSERT INTO url (url,id) VALUES(?,?)", ((message.text).split()[1],(message.text).split()[2],))
            conn.commit()
            conn.close()
            await message.answer('Список каналов обновлен')
        except:
            await message.answer('Что-то не так.Попробуйте еще раз!')
            conn.commit()
            conn.close()
    else:
        await message.answer('Вы не админ')
        conn.commit()
        conn.close()

@dp.message_handler(commands=['gree'])
async def start(message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    admin = cursor.execute(f"SELECT id FROM admin").fetchall()
    if any([int(message.chat.id) == int(x[0]) for x in admin]):
        try:
            cursor.execute(f"UPDATE text_greetings SET text = '{(message.text).split(' ',1)[1]}'")
            conn.commit()
            conn.close()
            await message.answer('Текст обновлен')
        except:
            await message.answer('Что-то не так.Попробуйте еще раз!')
            conn.commit()
            conn.close()
    else:
        await message.answer(message.chat.id,'Вы не админ')
        conn.commit()
        conn.close()



@dp.message_handler(commands=['text'])
async def start(message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    admin = cursor.execute(f"SELECT id FROM admin").fetchall()
    if any([int(message.chat.id) == int(x[0]) for x in admin]):
        try:
            cursor.execute(f"UPDATE text SET text_text = '{(message.text).split(' ',1)[1]}'")
            await message.answer('Текст обновлен')
            conn.commit()
            conn.close()
        except:
            await message.answer('Что-то не так.Попробуйте еще раз!')
            conn.commit()
            conn.close()
    else:
        await message.answer(message.chat.id,'Вы не админ')
        conn.commit()
        conn.close()

@dp.message_handler()
async def start(message: types.Message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    channels = cursor.execute(f"SELECT * FROM url").fetchall()
    if all([check_sub_channel(await bot.get_chat_member(chat_id=int(x[1]), user_id=message.chat.id)) for x in
            channels]):
        if message.text == 'Отправить фото':
            await message.answer('Отправьте фото боту')
    else:
        await message.answer('Подпишитесь на канал!')
    conn.commit()
    conn.close()

@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    text = cursor.execute(f"SELECT * FROM text").fetchall()[0][0]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton(text="Отправить фото"),
    ]
    markup.add(*buttons)
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    channels = cursor.execute(f"SELECT * FROM url").fetchall()
    if all([check_sub_channel(await bot.get_chat_member(chat_id=int(x[1]), user_id=callback_query.message.chat.id)) for x in
            channels]):
        await bot.send_message(callback_query.message.chat.id, text, reply_markup=markup)
    else:
        await bot.send_message(callback_query.message.chat.id,'Ты не подписался на канал!')
    conn.commit()
    conn.close()

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def process_photo(message):
    await message.answer('Фото принято\nОбрабатываться будет 24 часа')
while True:
    try:
        executor.start_polling(dp,skip_updates=True)
    except:
        pass
