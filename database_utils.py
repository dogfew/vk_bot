import os
import re
from json import dump, load

max_id = 9419901116


def dump_db():
    with open("persons.json", "w") as write_database:
        dump(database, write_database, indent=4)


def update_photos(user_id):
    database[user_id] = database.get(user_id)
    name = database[user_id].get("name", None)
    lst = [img for img in os.listdir("images") if img.startswith(name)] if name else []
    database[user_id]["images"] = lst


with open("persons.json") as load_database:
    database = load(open("persons.json"))
    for key in database:
        update_photos(key)


def extract_id(event, num=2):
    args = event.message.text.split(" ")
    if len(args) >= num:
        to_id = "".join(re.findall(r"\[id(\d*)\|.*]", event.message.text))
    else:
        to_id = str(event.message['from_id'])
    database[to_id] = database.get(to_id, {})
    return to_id if to_id.isnumeric() else ""


def change_audio(event):
    to_id = extract_id(event)
    attachments = event.message['attachments']
    audio = None
    for dictionary in attachments:
        if dictionary.get("audio", None):
            audio = "audio{}_{}".format(
                dictionary["audio"]["owner_id"],
                dictionary["audio"]["id"]
            )
            break
    database[to_id]["audio"] = audio
    dump_db()


def add_photos(event):
    photos = []
    attachments = event.message['attachments']
    for photo_dict in attachments:
        if photo_dict.get("photo", None):
            url = photo_dict["photo"]["sizes"][-1]["url"]
            photos.append(url)

    to_id = extract_id(event)
    database[to_id]["links"] = database[to_id].get("links", [])
    database[to_id]["links"].extend(photos)
    dump_db()


def clear_photos(event):
    to_id = extract_id(event)
    database[to_id]["links"] = []
    dump_db()


def ignor(event):
    to_id = extract_id(event)
    database[to_id]["ignor"] = database[to_id].get("ignor", False)
    database[to_id]["ignor"] = not database[to_id]["ignor"]
    dump_db()


def change_name(event):
    to_id = extract_id(event, num=3)
    args = event.message.text.split(" ")
    name = args[-1] if len(args) > 1 else None
    database[to_id]["name"] = name
    update_photos(to_id)
    dump_db()
