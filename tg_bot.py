import asyncio
import datetime
import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from auth_data import token, user_id, user_kuz_id
from main import get_data, get_str


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="123kuz321")
async def get_keyboard(message: types.Message):
    start_button = ['Все закупки', 'Новые закупки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)
    await message.answer("Лови кнопки", reply_markup=keyboard)


@dp.message_handler(Text(equals='Все закупки'))
async def get_all_lots(message: types.Message):
    with open("current_lots.json", encoding='utf-8') as file:
        lots_dict = json.load(file)
    sorted_values = sorted(lots_dict.values(), key=lambda x: x['lot_deadline'],
                           reverse=True)
    for v in sorted_values:
        lot = get_str(v)
        if lot is not None:
            await message.answer(lot)


@dp.message_handler(Text(equals='Новые закупки'))
async def get_fresh_lots(message: types.Message):
    fresh_lots, lot_counter = get_data()

    if len(fresh_lots):
        await message.answer(f"Просмотренных лотов: {lot_counter}")
        for k, v in fresh_lots.items():
            lot = get_str(v)
            if lot is not None:
                await message.answer(lot)
    else:
        await message.answer(
            f"Новых лотов нет...Просмотренных лотов: {lot_counter}")


async def lots_every_1_hours():
    while True:
        try:
            fresh_lots, lot_counter = get_data()
            if len(fresh_lots):
                await bot.send_message(user_id,
                                       f"Просмотренных лотов: {lot_counter}",
                                       disable_notification=True)
                for k, v in fresh_lots.items():
                    lot = get_str(v)
                    await bot.send_message(user_id, lot)
                    await bot.send_message(user_kuz_id, lot)
            else:
                await bot.send_message(user_id,
                                       f"Новых лотов нет...Просмотренных лотов: {lot_counter}",
                                       disable_notification=True)
        except Exception as ex:
            await bot.send_message(user_id, f"lots_every_1_hours{ex}")

        await asyncio.sleep(3600)


async def lots_every_6_hours():
    while True:
        with open("current_lots.json", encoding='utf-8') as file:
            lots_dict = json.load(file)
        for v in lots_dict.values():
            date = datetime.datetime.fromtimestamp(
                v['lot_deadline'])
            difference = date - datetime.datetime.now()
            if difference.days == 0 and difference.seconds // 3600 < 18 and v['flag'] is False:
                lot = get_str(v)
                v['flag'] = True
                if lot is not None:
                    await bot.send_message(user_kuz_id, lot)
                    await bot.send_message(user_id, lot)
        with open('current_lots.json', 'w', encoding='utf-8') as file:
            json.dump(lots_dict, file, indent=4, ensure_ascii=False)
        await asyncio.sleep(21600)


if __name__ == '__main__':
    while True:
        try:
            loop = asyncio.get_event_loop()
        except Exception as e:
            loop = asyncio.get_event_loop()
        try:
            loop.create_task(lots_every_1_hours())
        except Exception as e:
            loop.create_task(lots_every_1_hours())
        try:
            loop.create_task(lots_every_6_hours())
        except Exception as e:
            loop.create_task(lots_every_6_hours())
        try:
            executor.start_polling(dp)
        except Exception as e:
            executor.start_polling(dp)
