from datetime import datetime
from aiogram import types
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder
from bson.objectid import ObjectId

from bot import telegram_router, Authorization, bot
from menues import start_menu, AdminConfirmCallback, MaidConfirmCallback, ObjectMenuCallback, UserConfirmCallback
from db import connect
from settings import get_settings
from menues import create_accept_maid, create_object_menu, start_menu_admin, create_users_menu, start_menu_maid
from utils import check_user, create_user, del_user

cfg = get_settings()


apartments = connect("Apartments")
reservs = connect("Reservs")
admins = connect("Admins")
maids = connect("Maids")
texts = connect("Texts").find_one()


@telegram_router.message(CommandStart())
async def message(msg: Message) -> None:
    await msg.answer('Добро пожаловать!', reply_markup=start_menu_admin) if check_user(msg.from_user.id, 'admins') else await msg.answer('Добро пожаловать!', reply_markup=start_menu_maid) if check_user(msg.from_user.id, 'maids') else await msg.answer('Привет!', reply_markup=start_menu)


@telegram_router.callback_query(F.data == "signin")
async def callback_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Authorization.password)
    await callback_query.message.answer('Введите код')


@telegram_router.callback_query(F.data == "add_admin")
async def callback_handler(callback_query: CallbackQuery, state: FSMContext):
    result = create_user('admins')
    await callback_query.message.answer(result if result else 'ошибка')


@telegram_router.callback_query(F.data == "del_admin")
async def callback_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(reply_markup=create_users_menu(admins.find(), 'admins'))


@telegram_router.callback_query(F.data == "add_maid")
async def callback_handler(callback_query: CallbackQuery, state: FSMContext):
    result = create_user('maids')
    await callback_query.message.answer(result if result else 'ошибка')


@telegram_router.callback_query(F.data == "del_maid")
async def callback_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(reply_markup=create_users_menu(maids.find(), 'maids'))


@telegram_router.message(Command("id"))
async def message(msg: Message) -> None:
    await msg.answer(f'{msg.message_thread_id} / {msg.chat.id} / {msg.from_user.id}', reply_markup=start_menu)


@telegram_router.message(Authorization.password)
async def message(msg: Message, state: FSMContext) -> None:
    await state.clear()
    item = apartments.find_one({"id": 185366})
    # if item['confirm'] else await msg.answer('У вас нет брони.')
    await msg.answer('Добро пожаловать', reply_markup=create_object_menu(item['id']))


@telegram_router.callback_query(ObjectMenuCallback.filter(F.action == "info"))
async def callback_handler(callback_query: CallbackQuery, callback_data: ObjectMenuCallback):
    callback_query.answer(apartments.find_one(
        {'id': callback_data.apart_id})['description'])


@telegram_router.callback_query(ObjectMenuCallback.filter(F.action == "wifi"))
async def callback_handler(callback_query: CallbackQuery, callback_data: ObjectMenuCallback):
    callback_query.answer(apartments.find_one(
        {'id': callback_data.apart_id})['wifiPassword'])


@telegram_router.callback_query(ObjectMenuCallback.filter(F.action == "photo"))
async def callback_handler(callback_query: CallbackQuery, callback_data: ObjectMenuCallback):
    item = apartments.find_one({'id': callback_data.apart_id})
    media = MediaGroupBuilder()
    i = 0
    for photo in item['photos']:
        media.add_photo(media=photo)
        i += 1
        if (i == 10):
            i = 0
            await bot.send_media_group(callback_query.message.chat.id, media=media.build())
            media = MediaGroupBuilder()
    else:
        if media:
            await bot.send_media_group(callback_query.message.chat.id, media=media.build())


@telegram_router.callback_query(AdminConfirmCallback.filter())
async def callback_handler(callback_query: CallbackQuery, callback_data: AdminConfirmCallback):
    reservs.update_one({"_id": callback_data.book_id}, {
        "$set": {'confirm': True}})
    data = reservs.find_one({"_id": callback_data.book_id})
    await bot.send_message(cfg.maid_chat_id, data['data']['booking']['apartment']['title'], message_thread_id=cfg.maid_topic_id, reply_markup=create_accept_maid(callback_data.book_id, callback_data.apart_id))


@telegram_router.callback_query(MaidConfirmCallback.filter())
async def callback_handler(callback_query: CallbackQuery, callback_data: MaidConfirmCallback):
    reservs.update_one({"_id": callback_data.book_id}, {
        "$set": {"maid": {'time': datetime.now(), 'name': callback_query.from_user.first_name}}})
    data = reservs.find_one({"_id": callback_data.book_id})
    await bot.send_message(cfg.admin_chat_id, f"{data['maid']['time'].strftime("%H:%M")} {data['maid']['name']}", message_thread_id=cfg.admin_topic_id)


@telegram_router.callback_query(UserConfirmCallback.filter())
async def callback_handler(callback_query: CallbackQuery, callback_data: AdminConfirmCallback):
    await callback_query.message.answer('успешно' if del_user(callback_data.user_id, callback_data.db) else 'ошибка')
