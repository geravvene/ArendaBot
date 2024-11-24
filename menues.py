from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from settings import get_settings
from bson.objectid import ObjectId


cfg = get_settings()


class AdminConfirmCallback(CallbackData, prefix="admin_confirm"):
    book_id: int
    apart_id: int


class ObjectMenuCallback(CallbackData, prefix="object_menu"):
    action: str
    apart_id: int


class MaidConfirmCallback(CallbackData, prefix="maid_confirm"):
    book_id: int
    apart_id: int


class UserConfirmCallback(CallbackData, prefix="user_confirm"):
    user_id: str
    db: str


start_menu = [
    [InlineKeyboardButton(text="Забронировать 🏠", callback_data="rent")],
    [InlineKeyboardButton(text="Войти ✅", callback_data="signin")],
    [InlineKeyboardButton(text="Частые вопросы ❓", callback_data="quest")],
    [InlineKeyboardButton(text="Тех. поддержка 💬", callback_data="supp")],
]
start_menu = InlineKeyboardMarkup(inline_keyboard=start_menu)


def create_accept(book_id, apart_id):
    accept_menu = InlineKeyboardMarkup(inline_keyboard=[
                                       [InlineKeyboardButton(text="Подтвердить ✅", callback_data=AdminConfirmCallback(
                                           book_id=book_id,
                                           apart_id=apart_id
                                       ).pack())]])
    return accept_menu


def create_accept_maid(book_id, apart_id):
    accept_menu = InlineKeyboardMarkup(inline_keyboard=[
                                       [InlineKeyboardButton(text="Подтвердить ✅", callback_data=MaidConfirmCallback(
                                           book_id=book_id,
                                           apart_id=apart_id
                                       ).pack())]])
    return accept_menu


def create_object_menu(apart_id):
    object_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Информация 🏠", callback_data=ObjectMenuCallback(
            action="info", apart_id=apart_id).pack())],
        [InlineKeyboardButton(text="Фото ✅", callback_data=ObjectMenuCallback(
            action="photo", apart_id=apart_id).pack())],
        [InlineKeyboardButton(
            text="Wi-Fi ✅", callback_data=ObjectMenuCallback(action="wifi", apart_id=apart_id).pack())],
        [InlineKeyboardButton(text="Частые вопросы ❓", callback_data='faq')],
        [InlineKeyboardButton(text="Тех. поддержка 💬", callback_data="supp")],
    ])
    return object_menu


start_menu_admin = [
    [InlineKeyboardButton(text="Посмотреть объекты",
                          callback_data="view_objects")],
    [InlineKeyboardButton(text="Добавить объект", callback_data="add_object", url=f"{
                          cfg.base_webhook_url}/aparts/create")],
    [InlineKeyboardButton(text="Удалить объект", callback_data="del_object", url=f"{
                          cfg.base_webhook_url}/aparts/delete")],
    [InlineKeyboardButton(text="Добавить админа", callback_data="add_admin")],
    [InlineKeyboardButton(text="Удалить админа", callback_data="del_admin")],
    [InlineKeyboardButton(text="Добавить уборщицу", callback_data="add_maid")],
    [InlineKeyboardButton(text="Удалить уборщицу", callback_data="del_maid")],
    [InlineKeyboardButton(text="Редактировать сообщения",
                          callback_data="custom_text")],
]
start_menu_admin = InlineKeyboardMarkup(inline_keyboard=start_menu_admin)


def create_apart_menu(aparts):
    menu = []
    for apart in aparts:
        menu.append([InlineKeyboardButton(text=apart['adress'], url=f"{
                    cfg.base_webhook_url}/aparts/update/{apart['_id']}")])
    return InlineKeyboardMarkup(inline_keyboard=menu)


def create_users_menu(data, db):
    menu = []
    for user in data:
        menu.append([InlineKeyboardButton(text=user['name'],
                    callback_data=ObjectMenuCallback(db=db, user_id=str(user['_id'])).pack())])
    return InlineKeyboardMarkup(inline_keyboard=menu)


start_menu_maid = [
    [InlineKeyboardButton(text="Об уборке",
                          callback_data="clean_info")],
    [InlineKeyboardButton(text="Частые вопросы", callback_data="maid_faq")],
    [InlineKeyboardButton(text="Правила уборки", callback_data="clean_rules")],
    [InlineKeyboardButton(text="Расходники", callback_data="clean_items")],
    [InlineKeyboardButton(text="Конфликт", callback_data="maid_conflict")],
    [InlineKeyboardButton(text="Отчёт об уборке",
                          callback_data="maid_result")],
]
start_menu_maid = InlineKeyboardMarkup(inline_keyboard=start_menu_maid)
