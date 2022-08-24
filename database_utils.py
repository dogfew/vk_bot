import os
import re
from json import dump, load


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
    for user_id in database:
        update_photos(user_id)


def extract_id(event, num=2):
    args = event.message.text.split(" ")
    if len(args) >= num:
        regexp = r"\[id(\d*)\|.*]"
        to_id = "".join(re.findall(regexp, event.message.text))
    else:
        to_id = str(event.message['from_id'])
    database[to_id] = database.get(to_id, {})
    return to_id if to_id.isnumeric() else ""


def add_audio(event):
    attachments = event.message['attachments']
    audio = None
    for dictionary in attachments:
        if dictionary.get("audio", None):
            audio = "audio{}_{}".format(dictionary["audio"]["owner_id"], dictionary["audio"]["id"])
            break
            
    to_id = extract_id(event)
    database[to_id]["audio"] = audio
    dump_db()


def add_photos(event):
    attachments = event.message['attachments']
    photos = []
    for dictionary in attachments:
        if dictionary.get("photo", None):
            url = dictionary["photo"]["sizes"][-1]["url"]
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
    database[to_id]["ignor"] = not database[to_id].get("ignor", False)
    dump_db()


def change_name(event):
    to_id = extract_id(event, num=3)
    args = event.message.text.split(" ")
    name = args[-1] if len(args) > 1 else None
    database[to_id]["name"] = name
    update_photos(to_id)
    dump_db()


def check_status(event):
    from main import vk, get_random_id
    to_id = extract_id(event)
    out = f"User id: {to_id}\n"
    out += "\n".join(f"{k}: {v}".capitalize() for k, v in database[to_id].items())
    vk.messages.send(
        random_id=get_random_id(),
        message=out,
        chat_id=event.chat_id,
    )