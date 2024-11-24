from db import connect
from settings import get_settings
from bson.objectid import ObjectId

cfg = get_settings()

admins = connect("Admins")
maids = connect("Maids")


async def check_user(id, db_name):
    data = globals()[db_name].find_one({"acc": id})
    return True if data else False


async def set_user(id, user_id, name, db_name):
    db = globals()[db_name]
    data = db.find_one({"_id": ObjectId(id)})
    if data:
        db.update_one({'_id': data['_id']}, {
                      "$set": {'acc': user_id, 'name': name}})
        return True
    else:
        return False


async def create_user(db_name):
    id = ObjectId()
    return str(id) if globals()[db_name].insert_one({'_id': id, 'acc': "", 'name': ""}) else False


async def del_user(id, db_name):
    return True if globals()[db_name].delete_one({'_id': ObjectId(id), }) else False
