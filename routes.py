from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from fastapi import APIRouter, Header, Request
from aiogram import types

from bot import bot, dp
from settings import get_settings
from db import connect
from bson.objectid import ObjectId
from menues import create_accept

cfg = get_settings()
apartments = connect("Apartments")
reservs = connect("Reservs")
texts = connect("Texts")

templates = Jinja2Templates(directory="templates")


root_router = APIRouter(
    prefix="",
    tags=["root"],
    responses={404: {"description": "Not found"}},
)


@root_router.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@root_router.post(cfg.webhook_path)
async def bot_webhook(update: dict,
                      x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None) -> None | dict:
    """ Register webhook endpoint for telegram bot"""
    if x_telegram_bot_api_secret_token != cfg.telegram_my_token:
        return {"status": "error", "message": "Wrong secret token !"}
    telegram_update = types.Update(**update)
    await dp.feed_webhook_update(bot=bot, update=telegram_update)


@root_router.post("/realtycalendar")
async def webhookRC(request: Request) -> None:
    data = await request.json()
    if (data['action'] == 'create_booking'):
        data['confirm'] = False
        data['_id'] = data['data']['booking']['id']
        data['maid'] = {}
        data['apart_id'] = data['data']['booking']['apartment']['id']
        reservs.insert_one(data)
        await bot.send_message(cfg.admin_chat_id, data['data']['booking']['apartment']['title'], message_thread_id=cfg.admin_topic_id, reply_markup=create_accept(data['_id'], data['apart_id']))
    if (data['action'] == 'update_booking'):
        reservs.update_one(
            {'_id': data['data']['booking']['id']}, {"$set": data})
        await bot.send_message(cfg.admin_chat_id, f'{data['data']['booking']['apartment']['title']} изменена бронь', message_thread_id=cfg.admin_topic_id)
    if (data['action'] == 'delete_booking'):
        item = reservs.find_one({'_id': data['data']['booking']['id']})
        await bot.send_message(cfg.admin_chat_id, f'{item['data']['booking']['apartment']['title']} бронь закончилась', message_thread_id=cfg.admin_topic_id)
        reservs.delete_one({'_id': data['data']['booking']['id']})


@root_router.get("/aparts/create", response_class=HTMLResponse)
async def create_aparts(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@root_router.post("/aparts/save/create")
async def save_aparts(request: Request) -> None:
    apartments.insert_one(await request.json())


@root_router.post("/aparts/save/update")
async def save_update(request: Request) -> None:
    data = await request.json()
    id = ObjectId(data['_id'])
    del data['_id']
    apartments.update_one({"_id": id}, {"$set": data})


@root_router.get("/aparts/update/{id}", response_class=HTMLResponse)
async def getApart(request: Request, id):
    data = apartments.find_one({'_id': ObjectId(id)})
    data['_id'] = id
    return templates.TemplateResponse("update.html", {"request": request, "data": data})


@root_router.get("/aparts/delete", response_class=HTMLResponse)
async def del_aparts(request: Request):
    data = list(apartments.find())
    for item in data:
        item['_id'] = str(item['_id'])
    return templates.TemplateResponse("delete.html", {"request": request, "data": data})


@root_router.get("/texts")
async def del_apart(request: Request) -> None:
    data = texts.find_one()
    data['_id'] = str(data['_id'])
    return templates.TemplateResponse("texts.html", {"request": request, "data": data})


@root_router.post("/texts/update")
async def del_apart(request: Request) -> None:
    data = await request.json()
    id = ObjectId(data['_id'])
    del data['_id']
    texts.update_one({"_id": id}, {"$set": data})
