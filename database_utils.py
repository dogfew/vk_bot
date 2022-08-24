import os
from json import dump, load

with open("persons.json") as load_database:
    database = load(open("persons.json"))
    for key in database:
        name = database[key]['name']
        lst = [img for img in os.listdir("images") if img.startswith(name)]
        database[key]["images"] = lst


def dump_db():
    with open("persons.json", "w") as write_database:
        dump(database, write_database, indent=4)


def add_photos(event):
    photos = []
    attachments = event.message['attachments']
    for photo_dict in attachments:
        if photo_dict.get("photo", None):
            url = photo_dict["photo"]["sizes"][-1]["url"]
            photos.append(url)

    args = event.message.text.split(" ")
    to_id = args[1] if len(args) >= 2 else str(event.message['from_id'])
    database[to_id] = database.get(to_id, {})
    database[to_id]["links"] = database[to_id].get("links", [])
    database[to_id]["links"].extend(photos)
    dump_db()


def clear_photos(event):
    args = event.message.text.split(" ")
    to_id = args[1] if len(args) >= 2 else str(event.message['from_id'])
    database[to_id] = database.get(to_id, {})
    database[to_id]["links"] = []
    dump_db()
