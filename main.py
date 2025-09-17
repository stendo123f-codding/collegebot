import os

import aiosqlite
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.utils import keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import db_settings
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
import aioschedule

import logging
import asyncio
import datetime
import time
from multiprocessing import Process

ADMIN_IDS = [1374125439]
GROUPS_FOLDER = "raspisanie"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token='7786125648:AAG0qZ17_SQwRCSkcd7FpN1AE5DoK4LYg8U')
dp = Dispatcher()

router = Router(name="example_router")
dp.include_router(router)

scheduler = AsyncIOScheduler()

async def check_lunch_first_group():
    posting_time = ['11:50']

    while True:
        if datetime.datetime.now().strftime('%H:%M') in posting_time:
            users = await db_settings.get_first_group_notifi_on()
            for user in users:
                await bot.send_message(user[0], '<b>⏰ Пора на обед первая смена!</b>', parse_mode='HTML')
        await asyncio.sleep(60)

async def check_lunch_second_group():
    posting_time = ['12:45']

    while True:
        if datetime.datetime.now().strftime('%H:%M') in posting_time:
            users = await db_settings.get_second_group_notifi_on()
            for user in users:
                await bot.send_message(user[0], '<b>⏰ Пора на обед вторая смена!</b>', parse_mode='HTML')
        await asyncio.sleep(60)

async def check_start_lessons():
    posting_time = ['8:00']

    while True:
        if datetime.datetime.now().strftime('%H:%M') in posting_time:
            users = await db_settings.get_users_notifi_on()
            for user in users:
                await bot.send_message(user[0], '<b>⏰ Уроки скоро начнутся, поспеши!</b>', parse_mode='HTML')
        await asyncio.sleep(60)

def start_check_lunc():
    asyncio.run((check_lunch_first_group()))
    asyncio.run((check_lunch_second_group()))
    asyncio.run((check_start_lessons()))


def get_day_filename():
    days = {
        0: "ponedelnik.png",
        1: "vtornik.png",
        2: "sreda.png",
        3: "chetverg.png",
        4: "patnica.png",
        5: "Vihodnoy.png",
        6: "Vihodnoy.png"
    }

    today = datetime.datetime.now().weekday()
    return days.get(today)

def get_day_filename_tomorrow():
    days = {
        0: "ponedelnik.png",
        1: "vtornik.png",
        2: "sreda.png",
        3: "chetverg.png",
        4: "patnica.png",
        5: "Vihodnoy.png",
        6: "Vihodnoy.png"
    }

    today = datetime.datetime.now().weekday()
    tomorrow = today+1
    return days.get(tomorrow)

@router.message(Command('start'))
async def start_command(message: Message):
    try:
        await db_settings.create_tables()
        await db_settings.create_table_zamena()
    except:
        pass
    exists = await db_settings.user_exists(message.from_user.id)
    if str(exists) == '0':
        await db_settings.press_start(message.from_user.id, message.from_user.username)
    else:
        pass

    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text='ПТО', callback_data='pto'))
    keyboard.add(types.InlineKeyboardButton(text='ССО', callback_data='sso'))
    keyboard.adjust(1)
    check_group = await db_settings.check_group(message.from_user.id)
    if str(check_group) == 'None':
        await message.answer('<b>Привет👋\nЯ помогу тебе узнать точное расписание на сегодня или другие дни🗓.\nДля начала выбери на какое образование ты обучаешься👇</b>', parse_mode='html', reply_markup=keyboard.as_markup())
    else:
        kb = [
            [types.KeyboardButton(text='🗓 Расписание')],
            [types.KeyboardButton(text='⚙️ Настройки')]
        ]
        keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer('<b>И снова привет👋</b>', reply_markup=keyboard1, parse_mode='html')

@router.callback_query(F.data == 'pto')
async def pto(call: CallbackQuery):
    await call.message.delete()
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text='ЭС-10', callback_data='es-10'))
    keyboard.add(types.InlineKeyboardButton(text='ЭМ-11', callback_data='em-11'))
    keyboard.add(types.InlineKeyboardButton(text='ЭС-12', callback_data='es-12'))
    keyboard.add(types.InlineKeyboardButton(text='СМ-13', callback_data='sm-13'))
    keyboard.add(types.InlineKeyboardButton(text='ОС-14', callback_data='os-14'))
    keyboard.add(types.InlineKeyboardButton(text='ЭС-22', callback_data='es-22'))
    keyboard.add(types.InlineKeyboardButton(text='НС-23', callback_data='ns-23'))
    keyboard.add(types.InlineKeyboardButton(text='МО-24', callback_data='mo-24'))
    keyboard.add(types.InlineKeyboardButton(text='НМ-33', callback_data='nm-33'))
    keyboard.add(types.InlineKeyboardButton(text='МС-34', callback_data='ms-34'))
    keyboard.adjust(2)
    await call.message.answer('<b>Отлично👌\nТеперь выбери свою группу👇</b>', reply_markup=keyboard.as_markup(), parse_mode='html')

@router.callback_query(F.data == 'sso')
async def sso(call: CallbackQuery):
    await call.message.delete()
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text='ТЭ-11', callback_data='te-11'))
    keyboard.add(types.InlineKeyboardButton(text='ТТ-12', callback_data='tt-12'))
    keyboard.add(types.InlineKeyboardButton(text='Т-13', callback_data='t-13'))
    keyboard.add(types.InlineKeyboardButton(text='ТМ-14', callback_data='tm-14'))
    keyboard.add(types.InlineKeyboardButton(text='ТЭ-21', callback_data='te-21'))
    keyboard.add(types.InlineKeyboardButton(text='ТТ-22', callback_data='tt-22'))
    keyboard.add(types.InlineKeyboardButton(text='Т-23', callback_data='t-23'))
    keyboard.add(types.InlineKeyboardButton(text='ТМ-24', callback_data='tm-24'))
    keyboard.add(types.InlineKeyboardButton(text='Т-33', callback_data='t-33'))
    keyboard.add(types.InlineKeyboardButton(text='ТМ-34', callback_data='tm-34'))
    keyboard.adjust(2)
    await call.message.answer('<b>Отлично👌\nТеперь выбери свою группу👇</b>', reply_markup=keyboard.as_markup(), parse_mode='html')

@router.callback_query(F.data == 'es-10')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу ЭС-10. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('es-10', call.from_user.id)

@router.callback_query(F.data == 'em-11')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу ЭМ-11. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('em-11', call.from_user.id)

@router.callback_query(F.data == 'es-12')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу ЭС-12. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('es-12', call.from_user.id)

@router.callback_query(F.data == 'sm-13')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу СМ-13. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('sm-13', call.from_user.id)

@router.callback_query(F.data == 'os-14')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу ОС-13. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('os-14', call.from_user.id)

@router.callback_query(F.data == 'es-22')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу ЭС-22. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('es-22', call.from_user.id)

@router.callback_query(F.data == 'ns-23')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу НС-23. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('ns-23', call.from_user.id)

@router.callback_query(F.data == 'mo-24')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу МО-24. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('mo-24', call.from_user.id)

@router.callback_query(F.data == 'nm-33')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу НМ-33. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('nm-33', call.from_user.id)

@router.callback_query(F.data == 'ms-34')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу МС-34. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('ms-34', call.from_user.id)

@router.callback_query(F.data == 'te-11')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу ТЭ-11. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('te-11', call.from_user.id)

@router.callback_query(F.data == 'tt-12')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу ТТ-12. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('tt-12', call.from_user.id)

@router.callback_query(F.data == 't-13')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу Т-13. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('t-13', call.from_user.id)

@router.callback_query(F.data == 'tm-14')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу ТМ-14. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('tm-14', call.from_user.id)

@router.callback_query(F.data == 'te-21')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу ТЭ-21. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('te-21', call.from_user.id)

@router.callback_query(F.data == 'tt-22')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу ТТ-22. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('tt-22', call.from_user.id)

@router.callback_query(F.data == 't-23')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу Т-23. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('t-23', call.from_user.id)

@router.callback_query(F.data == 'tm-24')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу ТМ-24. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('tm-24', call.from_user.id)

@router.callback_query(F.data == 't-33')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу Т-33. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('t-33', call.from_user.id)

@router.callback_query(F.data == 'tm-34')
async def es10(call: CallbackQuery):
    kb = [
        [types.KeyboardButton(text='🗓 Расписание')],
        [types.KeyboardButton(text='⚙️ Настройки')]
    ]
    keyboard1 = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.delete()
    await call.message.answer('<b>Вы выбрали группу ТМ-34. Теперь вам доступно расписание для этой группы.\n\nЧтобы узнать расписание нажмите кнопку на клавиатуре ниже👇</b>', reply_markup=keyboard1, parse_mode='html')
    await db_settings.add_to_group('tm-34', call.from_user.id)

@router.message(F.text == '🗓 Расписание')
async def raspisanie(message: Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text='Сегодня', callback_data='today'))
    keyboard.add(types.InlineKeyboardButton(text='Завтра', callback_data='tomorrow'))
    keyboard.add(types.InlineKeyboardButton(text='Другие дни', callback_data='other_days'))
    keyboard.adjust(1)
    await message.answer('<b>На какой день вы хотите узнать расписание?🤔</b>', parse_mode='html', reply_markup=keyboard.as_markup())

@router.message(F.text == '⚙️ Настройки')
async def settings(message: Message):
    keyboard = InlineKeyboardBuilder()
    notifi = await db_settings.check_notifi(message.from_user.id)
    if int(notifi) == 1:
        keyboard.add(types.InlineKeyboardButton(text='🔕 Отключить уведомления', callback_data='off_notifi'))
    else:
        keyboard.add(types.InlineKeyboardButton(text='🔔 Включить уведомления', callback_data='on_notifi'))
    keyboard.add(types.InlineKeyboardButton(text='👥 Изменить группу', callback_data='change_group'))
    keyboard.add(types.InlineKeyboardButton(text='📱 Поддержка', url='https://t.me/skillex'))
    keyboard.adjust(1)
    await message.answer('<b>Выберите что вы хотите изменить👇</b>', parse_mode='html', reply_markup=keyboard.as_markup())

@router.callback_query(F.data == 'change_group')
async def change_group(call: CallbackQuery):
    await call.message.delete()
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text='ПТО', callback_data='pto'))
    keyboard.add(types.InlineKeyboardButton(text='ССО', callback_data='sso'))
    keyboard.adjust(1)
    await call.message.answer('<b>Выберите образование на которое вы обучаетесь👇</b>', parse_mode='html', reply_markup=keyboard.as_markup())

@router.callback_query(F.data == 'off_notifi')
async def off_notifi(call: CallbackQuery):
    await call.message.delete()
    await db_settings.off_notifi(call.from_user.id)
    await call.message.answer("<b>🔕 Уведомления выключены!</b>", parse_mode='html')

@router.callback_query(F.data == 'on_notifi')
async def off_notifi(call: CallbackQuery):
    await call.message.delete()
    await db_settings.on_notifi(call.from_user.id)
    await call.message.answer("<b>🔔 Уведомления включены!</b>", parse_mode='html')

@router.callback_query(F.data == 'today')
async def today(call: CallbackQuery):
    await call.message.delete()
    now = datetime.datetime.now()
    formatted_date = now.strftime("%d.%m.%Y")
    zamena_date = await db_settings.check_date_zamena()
    zamena_photo = await db_settings.get_photo_zamena()
    if formatted_date == zamena_date:
        await call.message.answer_photo(zamena_photo, caption='<b>Замена на сегодня</b>', parse_mode='html')
    else:
        pass
    group_name = await db_settings.get_group(call.from_user.id)
    day_filename = get_day_filename()
    file_path = os.path.join(GROUPS_FOLDER, group_name, day_filename)
    photo = FSInputFile(file_path)
    if day_filename != 'Vihodnoy.png':
        await call.message.answer_photo(photo, caption='<b>Вот ваше расписание на сегодня, удачного дня👌</b>', parse_mode='html')
    else:
        await call.message.answer_photo(photo, caption='<b>Сегодня выходной👌</b>', parse_mode='html')

@router.callback_query(F.data == 'tomorrow')
async def tomorrow(call: CallbackQuery):
    await call.message.delete()
    group_name = await db_settings.get_group(call.from_user.id)
    day_filename = get_day_filename_tomorrow()
    file_path = os.path.join(GROUPS_FOLDER, group_name, day_filename)
    photo = FSInputFile(file_path)
    if day_filename != 'Vihodnoy.png':
        await call.message.answer_photo(photo, caption='<b>Вот ваше расписание на завтра, удачного дня👌</b>', parse_mode='html')
    else:
        await call.message.answer_photo(photo, caption='<b>Завтра выходной👌</b>', parse_mode='html')

@router.callback_query(F.data == 'other_days')
async def other_days(call: CallbackQuery):
    await call.message.delete()
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text='Понедельник', callback_data='get_ponedelnik'))
    keyboard.add(types.InlineKeyboardButton(text='Вторник', callback_data='get_vtornik'))
    keyboard.add(types.InlineKeyboardButton(text='Среда', callback_data='get_sreda'))
    keyboard.add(types.InlineKeyboardButton(text='Четверг', callback_data='get_chetverg'))
    keyboard.add(types.InlineKeyboardButton(text='Пятница', callback_data='get_patnica'))
    keyboard.add(types.InlineKeyboardButton(text='Вернуться ↩️', callback_data='back'))
    keyboard.adjust(1)
    await call.message.answer('<b>Выберите на какой день хотите узнать расписание:</b>', parse_mode='html', reply_markup=keyboard.as_markup())

@router.callback_query(F.data == 'get_ponedelnik')
async def ponedelnik(call: CallbackQuery):
    await call.message.delete()
    group_name = await db_settings.get_group(call.from_user.id)
    file_path = os.path.join(GROUPS_FOLDER, group_name, 'ponedelnik.png')
    photo = FSInputFile(file_path)
    await call.message.answer_photo(photo, 'Вот ваше расписание уроков на понедельник!👌')

@router.callback_query(F.data == 'get_vtornik')
async def vtornik(call: CallbackQuery):
    await call.message.delete()
    group_name = await db_settings.get_group(call.from_user.id)
    file_path = os.path.join(GROUPS_FOLDER, group_name, 'vtornik.png')
    photo = FSInputFile(file_path)
    await call.message.answer_photo(photo, 'Вот ваше расписание уроков на вторник!👌')

@router.callback_query(F.data == 'get_sreda')
async def sreda(call: CallbackQuery):
    await call.message.delete()
    group_name = await db_settings.get_group(call.from_user.id)
    file_path = os.path.join(GROUPS_FOLDER, group_name, 'sreda.png')
    photo = FSInputFile(file_path)
    await call.message.answer_photo(photo, 'Вот ваше расписание уроков на среду!👌')

@router.callback_query(F.data == 'get_chetverg')
async def chetverg(call: CallbackQuery):
    await call.message.delete()
    group_name = await db_settings.get_group(call.from_user.id)
    file_path = os.path.join(GROUPS_FOLDER, group_name, 'chetverg.png')
    photo = FSInputFile(file_path)
    await call.message.answer_photo(photo, 'Вот ваше расписание уроков на четверг!👌')

@router.callback_query(F.data == 'get_patnica')
async def patnica(call: CallbackQuery):
    await call.message.delete()
    group_name = await db_settings.get_group(call.from_user.id)
    file_path = os.path.join(GROUPS_FOLDER, group_name, 'patnica.png')
    photo = FSInputFile(file_path)
    await call.message.answer_photo(photo, 'Вот ваше расписание уроков на пятницу!👌')


@router.callback_query(F.data == 'back')
async def back(call: CallbackQuery):
    await call.message.delete()
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text='Сегодня', callback_data='today'))
    keyboard.add(types.InlineKeyboardButton(text='Завтра', callback_data='tomorrow'))
    keyboard.add(types.InlineKeyboardButton(text='Другие дни', callback_data='other_days'))
    keyboard.adjust(1)
    await call.message.answer('<b>На какой день вы хотите узнать расписание?🤔</b>', parse_mode='html',
                         reply_markup=keyboard.as_markup())

class AddSpam(StatesGroup):
    message = State()
    photo = State()

@router.message(Command('spam'), StateFilter(None))
async def spam(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        pass
    else:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(types.InlineKeyboardButton(text='Отменить', callback_data='cancel'))
        await message.answer('<b>Введите сообщение для рассылки:</b>', parse_mode='html', reply_markup=keyboard.as_markup())
        await state.set_state(AddSpam.message)

@router.message(AddSpam.message)
async def spam(message: Message, state: FSMContext):
    await state.update_data(message=message.text)
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='spam_photo_yes'))
    keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data='spam_photo_no'))
    keyboard.add(types.InlineKeyboardButton(text='Отменить', callback_data='cancel'))
    await message.answer('<b>Отлично, хотите ли вы добавить фото в рассылку?</b>', parse_mode='html', reply_markup=keyboard.as_markup())

@router.callback_query(F.data == 'spam_photo_yes')
async def spam_photo_yes(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отлично, тогда пришлите фото для рассылки:')
    await state.set_state(AddSpam.photo)

@router.message(AddSpam.photo)
async def spam(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer('Отлично, начинаю рассылку!')
    data = await state.get_data()
    message = data['message']
    photo = data['photo']
    suc_users = 0
    fail_users = 0
    users = await db_settings.get_all_users()
    for user in users:
        try:
            await bot.send_photo(user[0], photo, caption=f'{message}')
            suc_users += 1
        except:
            fail_users += 1
    await bot.send_message(ADMIN_IDS[0], f'Успешно отправлено {suc_users} пользователям')
    await bot.send_message(ADMIN_IDS[0], f'Неуспешно отправлено {fail_users} пользователям')
    await state.clear()


@router.callback_query(F.data == 'spam_photo_no')
async def spam_photo_no(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data['message']
    users = await db_settings.get_all_users()
    suc_users = 0
    fail_users = 0
    for user in users:
        try:
            await bot.send_message(user[0], f'{message}')
            suc_users += 1
        except:
            fail_users += 1
    await bot.send_message(ADMIN_IDS[0], f'Успешно отправлено {suc_users} пользователям')
    await bot.send_message(ADMIN_IDS[0], f'Неуспешно отправлено {fail_users} пользователям')
    await state.clear()

class Zamena(StatesGroup):
    date = State()
    photo = State()

@router.message(Command('add_zamena'), StateFilter(None))
async def add_zamena(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        pass
    else:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(types.InlineKeyboardButton(text='Отменить', callback_data='cancel'))
        await message.answer('<b>Введите дату замены в формате ДД.ММ.ГГГГ:</b>', reply_markup=keyboard.as_markup(), parse_mode='html')
        await state.set_state(Zamena.date)

@router.message(Zamena.date)
async def zamena(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text='Отменить', callback_data='cancel'))
    await message.answer('<b>Отлично, теперь скинь фото замены:</b>', reply_markup=keyboard.as_markup(), parse_mode='html')
    await state.set_state(Zamena.photo)

@router.message(Zamena.photo)
async def zamena(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()
    date = data['date']
    photo = data['photo']
    await db_settings.add_zamena(photo, date)
    await bot.send_photo(ADMIN_IDS[0], photo, caption=f'Добавлена новая замена на {date}')
    users = await db_settings.get_all_users()
    for user in users:
        try:
            await bot.send_photo(user[0], photo, caption=f'Замена на {date}')
        except:
            pass
    await state.clear()


@router.callback_query(F.data == 'cancel')
async def cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer('Вы отменили действие')


async def main():
    process = Process(target=start_check_lunc)
    process.start()
    await dp.start_polling(bot)
    process.join()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())