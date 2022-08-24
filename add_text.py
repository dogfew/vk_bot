import textwrap
import requests

from PIL import Image, ImageFont
from pilmoji import Pilmoji
from json import dump
from config import default_photo_dict


def make_image(text, in_image, out_image):
    image = Image.open("images/" + in_image)
    font = ImageFont.truetype("fonts/Ubuntu-B.ttf", 42)
    margin = offset = 20
    with Pilmoji(image) as pilmoji:
        for line in textwrap.wrap(text, width=20):
            pilmoji.text((margin, offset), line, font=font, fill='black')
            offset += font.getsize(line)[1]
    image.save("temp_images/" + out_image)


def make_image_web(text, url, out_image):
    image = Image.open(requests.get(url, stream=True).raw)
    font = ImageFont.truetype("fonts/Ubuntu-B.ttf", 42)
    margin = offset = 20
    with Pilmoji(image) as pilmoji:
        for line in textwrap.wrap(text, width=20):
            pilmoji.text((margin, offset), line, font=font, fill='black')
            offset += font.getsize(line)[1]
    image.save("temp_images/" + out_image)


def add_photos(event, database):
    photos = []
    attachments = event.message['attachments']
    for photo_dict in attachments:
        if photo_dict.get("photo", None):
            url = photo_dict["photo"]["sizes"][-1]["url"]
            photos.append(url)
    args = event.message.text.split(" ")
    # !фото to_id вложение
    match len(args):
        case 1:
            to_id = str(event.message['from_id'])
            database[to_id] = database.get(to_id, {})
            database[to_id]["links"] = database[to_id].get("links", [])
            database[to_id]["links"].extend(photos)
        case 2:
            to_id = args[1]
            database[to_id] = database.get(to_id, {})
            database[to_id]["links"] = database[to_id].get("links", [])
            database[to_id]["links"].extend(photos)
    with open("persons.json", "w") as write_database:
        dump(database, write_database, indent=4)
    return database


def clear_photos(event, database):
    args = event.message.text.split(" ")
    match len(args):
        case 1:
            to_id = str(event.message['from_id'])
            database[to_id] = database.get(to_id, {})
            database[to_id]["links"] = []
        case 2:
            to_id = args[1]
            database[to_id] = database.get(to_id, {})
            database[to_id]["links"] = []
    with open("persons.json", "w") as write_database:
        dump(database, write_database, indent=4)
    return database