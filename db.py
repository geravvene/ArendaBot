from pymongo import MongoClient
from aiogram.fsm.storage.mongo import MongoStorage

url = "mongodb+srv://geravvene:NJxN8XPdTKMe84YF@wordigma.rmxf6nd.mongodb.net/"

database = MongoClient(url)['ArendaBot']


def create_storage():
    return MongoStorage.from_url(url)


def connect(name):
    return database[name]
